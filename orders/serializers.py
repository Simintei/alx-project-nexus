# orders/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from books.models import Book
from .models import CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source="book.title")
    price = serializers.ReadOnlyField(source="book.price")

    class Meta:
        model = CartItem
        fields = ["id", "book", "book_title", "price", "quantity", "added_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source="book.title")

    class Meta:
        model = OrderItem
        fields = ["id", "book", "book_title", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)


    class Meta:
        model = Order
        fields = ["id", "total_amount", "status", "created_at", "items"]
