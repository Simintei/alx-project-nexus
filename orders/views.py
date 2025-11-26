# orders/views.py

from rest_framework import viewsets, status              
from rest_framework.response import Response             
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django_filters.rest_framework import FilterSet
from books.models import Book
from .models import CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderSerializer


# Filter — compatible with viewsets
class CartItemFilter(FilterSet):
    class Meta:
        model = CartItem
        fields = ["book", "quantity"]



class CartViewSet(viewsets.ModelViewSet):                 
    """
    Handles listing, adding, and removing cart items.
    Emulates- CartView, AddToCartView, RemoveFromCartView
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CartItemFilter

    def get_queryset(self):                                
        return CartItem.objects.filter(user=self.request.user)

    
    def create(self, request, *args, **kwargs):            
        book_id = request.data.get("book")
        quantity = int(request.data.get("quantity", 1))

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=201)

   
    def destroy(self, request, *args, **kwargs):           
        pk = kwargs.get("pk")

        try:
            item = CartItem.objects.get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=404)

        item.delete()
        return Response({"message": "Item removed"}, status=200)



class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lists orders for the authenticated user.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)



class CheckoutView(viewsets.ViewSet):                     
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request):                             
        cart_items = CartItem.objects.filter(user=request.user).select_related("book")
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total_amount = sum(item.book.price * item.quantity for item in cart_items)

        order = Order.objects.create(user=request.user, total_amount=total_amount)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=201)
