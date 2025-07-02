from django.db import models
from django.contrib.auth.models import User





class Customer(models.Model):
    USER_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')  # Add user_type field 
    

    def __str__(self):
        return self.name




#!!!!!!!!! PRODUCT MODELS !!!!!!!!!!!!


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
     
    
    def __str__(self):
        return f"{self.name} (created by {self.creator.username})" if self.creator else f"{self.name} (no creator)"


    
    


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    #product_status = models.ForeignKey(ProductStatus, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    #brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    #product_document = models.ForeignKey(ProductDocument, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    


    def __str__(self):
        return self.name
    





#!!!!!!!!!!! CART MODELS !!!!!!!!!!!!!!!

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def cart_total_price(self):
        return sum(item.item_total_price for item in self.cartitem_set.all())

    
    @property
    def cart_total_items(self):
        return sum(item.quantity for item in self.cartitem_set.all())

    def __str__(self):
        return f'Cart {self.id} - Customer: {self.customer.name if self.customer else "No Customer"}'
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True)

    @property
    def item_total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f'CartItem for {self.cart}'
    


class ShippingAddress(models.Model):
    customer= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    region = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     db_table = 'ShippingAddress'

    def __str__(self):
        return f'{self.customer} address is  {self.address}'

