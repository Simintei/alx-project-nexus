# orders/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django_filters.rest_framework import FilterSet
from books.models import Book
from .models import CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderSerializer


# Define a FilterSet for CartItem
class CartItemFilter(FilterSet):
    class Meta:
        model = CartItem
        fields = ["book", "quantity"]  # fields users can filter by


class CartView(generics.ListAPIView):
    """
    List all items in the authenticated user's cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CartItemFilter  

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related("book")


class AddToCartView(generics.CreateAPIView):
    """
    Add a book to the authenticated user's cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
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


# Define a FilterSet for RemoveFromCartView (optional, mainly for schema)
class RemoveCartItemFilter(FilterSet):
    class Meta:
        model = CartItem
        fields = ["id"]


class RemoveFromCartView(generics.DestroyAPIView):
    """
    Remove an item from the authenticated user's cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = RemoveCartItemFilter  

    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=404)

        item.delete()
        return Response({"message": "Item removed"}, status=200)


class CheckoutView(generics.CreateAPIView):
    """
    Checkout the authenticated user's cart and create an order.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
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

        cart_items.delete()  # clear cart

        return Response(OrderSerializer(order).data, status=201)
