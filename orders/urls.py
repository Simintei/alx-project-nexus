from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartView, AddToCartView, RemoveFromCartView, CheckoutView

router = DefaultRouter()
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
  path("cart/", CartView.as_view(), name="cart"),
  path("cart/add/", AddToCartView.as_view(), name="add_to_cart"),
  path("cart/remove/<int:pk>/", RemoveFromCartView.as_view(), name="remove_from_cart"),
  path("checkout/", CheckoutView.as_view(), name="checkout"),
]
