"""bookstore URL Configuration"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger / OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Bookstore API",
        default_version="v1",
        description="API for bookstore backend",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Redirect root URL to Swagger UI
def redirect_to_swagger(request):
    return redirect('schema-swagger-ui')

urlpatterns = [
    # Root redirects to Swagger
    path('', redirect_to_swagger),

    # Admin
    path('admin/', admin.site.urls),

    # App URLs
    path('api/books/', include('books.urls')),
    path('api/users/', include('users.urls')),
    path('api/orders/', include('orders.urls')),

    # JWT Authentication
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger / OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
