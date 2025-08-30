from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
#
#
# class Customer(models.Model):
#     USER_TYPE_CHOICES = [
#         ('buyer', 'Buyer'),
#         ('seller', 'Seller'),
#     ]
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200)
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')
#
#     def __str__(self):
#         return self.name
#
#
# class SavedProducts(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey("backend.Product", on_delete=models.CASCADE)
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('user', 'product')
#         indexes = [
#             models.Index(fields=['user', 'product']),
#         ]
#
#     def __str__(self):
#         return f"{self.user.username} saved {self.product.name}"
#
#
# class Review(models.Model):
#     product = models.ForeignKey("backend.Product", on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     title = models.CharField(max_length=255)
#     message = models.TextField()
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.product.name} ({self.rating} stars)"
#
#
# # ---------------- CART & ORDERS ----------------
#
# class Cart(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False)
#     customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)
#
#     @property
#     def cart_total_price(self):
#         return sum(item.item_total_price for item in self.cartitem_set.all())
#
#     @property
#     def cart_total_items(self):
#         return sum(item.quantity for item in self.cartitem_set.all())
#
#     def __str__(self):
#         return f'Cart {self.id} - Customer: {self.customer.name if self.customer else "No Customer"}'
#
#
# class CartItem(models.Model):
#     product = models.ForeignKey("backend.Product", on_delete=models.CASCADE, null=True)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
#     quantity = models.IntegerField(default=0, null=True)
#
#     @property
#     def item_total_price(self):
#         return self.product.price * self.quantity
#
#     def __str__(self):
#         return f'CartItem for {self.cart}'
#
#
# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
#     address = models.CharField(max_length=200)
#     city = models.CharField(max_length=200)
#     region = models.CharField(max_length=200)
#     phone = models.CharField(max_length=200)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.customer} address is {self.address}'
#
#
# class API(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)
#     key = models.CharField(max_length=200, null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name
#
#
# class PaymentMethod(models.Model):
#     method = models.CharField(max_length=100, null=True)
#     APIkey = models.ForeignKey(API, on_delete=models.SET_NULL, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.method
#
#
# class Transaction(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.IntegerField()  # in pesewas
#     reference = models.CharField(max_length=100, unique=True)
#     verified = models.BooleanField(default=False)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.customer} - {self.amount / 100} GHS"
#
#
# class OrderStatus(models.Model):
#     status = models.CharField(max_length=50, unique=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.status
#
#
# class Order(models.Model):
#     cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     payment = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True)
#     shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
#     status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     @property
#     def total_price(self):
#         return self.cart.cart_total_price
#
#     @property
#     def total_items(self):
#         return self.cart.cart_total_items
#
#     def __str__(self):
#         return f"Order {self.id} - {self.customer.username} ({self.status})"
#
#
# # ---------------- DELIVERY ----------------
#
# class DeliveryMethod(models.Model):
#     mode = models.CharField(max_length=100, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class DeliveryStatus(models.Model):
#     status = models.CharField(max_length=100, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class Delivery(models.Model):
#     delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.SET_NULL, null=True, blank=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
#     status = models.ForeignKey(DeliveryStatus, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
