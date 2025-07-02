from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, CustomerViewSet,
    CartViewSet, ShippingAddressViewSet, register, login_api, logout
)

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')
router.register('customers', CustomerViewSet, basename='customer')
router.register('carts', CartViewSet, basename='cart')
router.register('shipping-addresses', ShippingAddressViewSet, basename='shipping')

urlpatterns = [
    path('', include(router.urls)),
    # Additional API endpoints can be added here
    path('login/', login_api, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
]
