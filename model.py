from django.db import models
from django.contrib.postgres.fields import JSONField  # or use models.JSONField for Django 3.1+

# -REFERENCE TABLES -

class UserType(models.Model):
    user_type = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'UserType'

    def __str__(self):
        return self.user_type


class UserStatus(models.Model):
    status = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'UserStatus'

    def __str__(self):
        return self.status


class Country(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Country'

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True, blank=True)
    currency_code = models.CharField(max_length=10, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Currency'

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)
    region_code = models.CharField(max_length=10, unique=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Region'

    def __str__(self):
        return self.name


class AddressType(models.Model):
    type = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'AddressType'

    def __str__(self):
        return self.type


class CategoryType(models.Model):
    category = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'CategoryType'

    def __str__(self):
        return self.category


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Brand'

    def __str__(self):
        return self.name


class DeliveryMode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'DeliveryMode'

    def __str__(self):
        return self.name


class Status(models.Model):
    status = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Status'

    def __str__(self):
        return self.status


class API(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'API'

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    method = models.CharField(max_length=100)
    api_key = models.ForeignKey(API, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'PaymentMethod'

    def __str__(self):
        return self.method


class Sender(models.Model):
    sender_address = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Sender'

    def __str__(self):
        return self.sender_address


class NotificationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'NotificationType'

    def __str__(self):
        return self.name


class NotificationTemplate(models.Model):
    message = models.TextField()
    subject = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'NotificationTemplate'

    def __str__(self):
        return f"{self.subject or 'Template'}"


class GeneralSetup(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'GeneralSetup'

    def __str__(self):
        return self.name




# ------------------ MAIN ENTITY TABLES ------------------

class Users(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20, unique=True, null=True, blank=True)
    user_type = models.ForeignKey(UserType, on_delete=models.DO_NOTHING)
    user_status = models.ForeignKey(UserStatus, on_delete=models.DO_NOTHING)
    password_hash = models.BinaryField()
    last_login_date = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    city = models.CharField(max_length=200, null=True, blank=True)
    address_type = models.ForeignKey(AddressType, on_delete=models.DO_NOTHING)
    digital_address = models.CharField(max_length=100, null=True, blank=True)
    street_name = models.CharField(max_length=200, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Address'

    def __str__(self):
        return f"{self.street_name or 'Address'} - {self.city or ''}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(CategoryType, on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Product'

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    sku = models.CharField(max_length=100, unique=True)
    attributes = models.JSONField(null=True, blank=True)  # Django >= 3.1
    price = models.DecimalField(max_digits=18, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'ProductVariant'

    def __str__(self):
        return self.sku or f"Variant of {self.product}"


class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Cart'

    def __str__(self):
        return f"Cart {self.id} - User {self.user_id}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    quantity = models.BigIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'CartItem'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, null=True, blank=True)
    amount = models.DecimalField(max_digits=18, decimal_places=3)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Orders'

    def __str__(self):
        return f"Order {self.id} - User {self.user_id}"


class Transactions(models.Model):
    payment_mode = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Orders, on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, null=True, blank=True)
    amount = models.DecimalField(max_digits=18, decimal_places=3, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Transactions'

    def __str__(self):
        return f"Transaction {self.id} - Amount {self.amount}"



# ------------------ WAREHOUSE & INVENTORY ------------------

class Warehouse(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Warehouse'

    def __str__(self):
        return self.name or f"Warehouse {self.id}"


class WarehouseStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'WarehouseStock'

    def __str__(self):
        return f"{self.product_variant} in {self.warehouse}"


class InventoryActionType(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'InventoryActionType'

    def __str__(self):
        return self.name


class Reason(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    action_type = models.ForeignKey(InventoryActionType, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Reason'

    def __str__(self):
        return self.description


class InventoryTransaction(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.DO_NOTHING)
    quantity_change = models.IntegerField()
    reason = models.ForeignKey(Reason, on_delete=models.DO_NOTHING)
    reference_id = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'InventoryTransaction'
        constraints = [
            models.CheckConstraint(check=~models.Q(quantity_change=0), name='quantity_change_non_zero')
        ]

    def __str__(self):
        return f"{self.quantity_change} - {self.product_variant}"


# ------------------ DELIVERY ------------------

class DeliveryMode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'DeliveryMode'

    def __str__(self):
        return self.name


class Delivery(models.Model):
    tracking_number = models.CharField(max_length=50)
    delivery_mode = models.ForeignKey(DeliveryMode, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Orders, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    dispatch_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Delivery'

    def __str__(self):
        return self.tracking_number


class PickupStation(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    is_warehouse = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'PickupStation'

    def __str__(self):
        return self.name or f"PickupStation {self.id}"


# ------------------ NOTIFICATIONS ------------------

class NotificationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'NotificationType'

    def __str__(self):
        return self.name


class NotificationTemplate(models.Model):
    message = models.TextField()
    subject = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'NotificationTemplate'

    def __str__(self):
        return self.subject or f"Template {self.id}"


class Sender(models.Model):
    sender_address = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Sender'

    def __str__(self):
        return self.sender_address


class Notification(models.Model):
    notification_type = models.ForeignKey(NotificationType, on_delete=models.DO_NOTHING)
    notification_template = models.ForeignKey(NotificationTemplate, on_delete=models.DO_NOTHING)
    message = models.TextField(null=True, blank=True)
    subject = models.CharField(max_length=300, null=True, blank=True)
    sender = models.ForeignKey(Sender, on_delete=models.DO_NOTHING)
    recipient = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Notification'

    def __str__(self):
        return self.subject or f"Notification {self.id}"

# ------------------ ORDER HISTORY & USER INTERACTIONS ------------------

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    changed_date = models.DateTimeField(auto_now_add=True)
    changed_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'OrderStatusHistory'

    def __str__(self):
        return f"Order {self.order.id} - Status {self.status}"


class SavedItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'SavedItem'

    def __str__(self):
        return f"{self.user} saved {self.product}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    rating = models.IntegerField()
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Review'
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                                   name='rating_range_1_5')
        ]

    def __str__(self):
        return f"{self.user} - {self.product} ({self.rating})"
