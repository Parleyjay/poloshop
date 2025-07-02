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


    #PRODUCT URLS
    path('create_product/', views.create_product, name='create_product'),
    path('product_detail/<int:id>', views.product_detail, name='product_detail'),
    path('edit/<int:id>/', views.edit_product, name='edit_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),

    #CART URLS
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('shipping_address/', views.shipping_address, name='shipping_address'),
    
    



    #CUSTOMER URLS
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('customers/', views.all_customer, name='all_customer'),
    path('customer_detail/<int:id>/', views.customer_detail, name='customer_detail'),
    path('logout/', views.user_logout, name='logout'),







    

]