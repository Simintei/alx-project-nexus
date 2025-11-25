from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from books.models import Book
from .models import CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderSerializer


# List all cart items for the logged-in user
class CartView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related("book")


# Add an item to the cart
class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")
        quantity = int(request.data.get("quantity", 1))

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Remove an item from the cart
class RemoveFromCartView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


# Checkout cart items and create an order
class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user).select_related("book")
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.book.price * item.quantity for item in cart_items)

        order = Order.objects.create(user=request.user, total_amount=total_amount)

        order_items = [
            OrderItem(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            ) for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        cart_items.delete()  # clear cart

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
