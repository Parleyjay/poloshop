from django.urls import path
from . import views


urlpatterns = [
    #path('', views.test, name='test'),
    path('', views.home, name='home'),
    
    
    #CATEGORY URLS
    path('create_category/', views.create_category, name='create_category'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('all_category/', views.all_category, name='all_category'),
    path('category_detail/<int:id>/', views.category_detail, name='category_detail'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),

    #BRAND URLS
    path('create_brand', views.create_brand, name='create_brand'),


    #PRODUCT URLS
    path('create_product/', views.create_product, name='create_product'),
    path('product_detail/<int:id>', views.product_detail, name='product_detail'),
    path('edit/<int:id>/', views.edit_product, name='edit_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),

    #INVENTORY URLS
    path('create_inventory/', views.create_inventory, name='create_inventory'),

    #SAVEDPRODUCT URLS
    path('save_product/<int:id>/', views.add_savedproduct, name='add_saved_product'),
    path('saved_products/', views.saved_products_list, name='saved_products'),
    path('remove_savedproduct/<int:product_id>/', views.remove_savedproduct, name='remove_saved_product'),


    #REVIEW URLS
    path('add_review/<int:id>/', views.add_review, name='add_review'),
    path('remove_review/<int:id>/', views.remove_review, name='remove_review'),


    #CART URLS
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('shipping_address/', views.shipping_address, name='shipping_address'),
    
    
    path('orders/', views.all_orders, name='orders'),
    path('order_detail/<int:id>/', views.order_detail, name='order_detail'),

    # STRIPE URLS
    # path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancelled/', views.payment_cancelled, name='payment_cancelled'),


    path('order/complete/', views.completed_order_view, name='orders_complete'),


    #CUSTOMER URLS
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('customers/', views.all_customer, name='all_customer'),
    path('customer_detail/<int:id>/', views.customer_detail, name='customer_detail'),
    path('logout/', views.user_logout, name='logout'),
    path('account_detail/', views.account_detail, name='account_detail'),
    
    
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    







    

]