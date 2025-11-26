# orders/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet, CheckoutView

router = DefaultRouter()

# CartViewSet handles:
#   GET /cart/         → list cart items
#   POST /cart/        → add to cart
#   DELETE /cart/{id}/ → remove from cart
router.register(r'cart', CartViewSet, basename='cart')

# List user orders
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),

    # Checkout endpoint
    path('checkout/', CheckoutView.as_view({'post': 'create'}), name='checkout'),
]
