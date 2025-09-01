# frontend/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # PRODUCT DISPLAY
    path('products/<int:id>/', views.product_detail, name='product_detail'),

    # SAVED PRODUCTS
    path('saved/', views.saved_products_list, name='saved_products'),
    path('save/<int:id>/', views.add_savedproduct, name='add_saved_product'),
    path('remove_saved/<int:product_id>/', views.remove_savedproduct, name='remove_saved_product'),

    # REVIEWS
    path('review/add/<int:id>/', views.add_review, name='add_review'),
    path('review/remove/<int:id>/', views.remove_review, name='remove_review'),

    # CART
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('shipping/', views.shipping_address, name='shipping_address'),
    path('shipping/<int:id>/edit/', views.edit_address, name='edit_address'),

    # ORDER STATUS
    path('all-orders/', views.all_orders, name='user_orders'),
    path('all-orders/<int:id>/', views.order_detail, name='user_order_detail'),

    # PAYMENTS
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancelled/', views.payment_cancelled, name='payment_cancelled'),

    # AUTH
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account_detail, name='account_detail'),


    # path('customer/dashboard/', customerviews.dashboard, name='customer_dashboard'),

    # FOR VENDORS
    # path('vendor/dashboard/', vendorviews.dashboard, name='vendor_dashboard'),





]
