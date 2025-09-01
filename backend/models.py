from django.db import models
# from frontend.models import Orders
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import JSONField  # or use models.JSONField for Django 3.1+
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# ==
# REFERENCE TABLES
# ==

# User = get_user_model()

class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES)


class UserType(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    user_type = models.CharField(max_length=50, db_column='UserType')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UserType'

    def __str__(self):
        return self.user_type or f"UserType {self.id}"


class UserStatus(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    status = models.CharField(max_length=10, db_column='Status')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UserStatus'

    def __str__(self):
        return self.status or f"UserStatus {self.id}"





class Currency(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=10, db_column='Name')
    country = models.ForeignKey('frontend.Country', models.DO_NOTHING, db_column='CountryId', blank=True, null=True)
    currency_code = models.CharField(max_length=10, db_column='CurrencyCode', unique=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Currency'

    def __str__(self):
        return self.currency_code





class AddressType(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    type = models.CharField(max_length=100, db_column='Type', unique=True, blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AddressType'

    def __str__(self):
        return self.type or f"AddressType {self.id}"


class CategoryType(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    category = models.CharField(max_length=100, db_column='Category')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CategoryType'
        constraints = [
            models.UniqueConstraint(fields=['category'], name='uq_categorytype_category'),
        ]

    def __str__(self):
        return self.category


class Brand(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', unique=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Brand'

    def __str__(self):
        return self.name


class DeliveryMode(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', unique=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DeliveryMode'

    def __str__(self):
        return self.name


class Status(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    status = models.CharField(max_length=50, db_column='Status')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Status'

    def __str__(self):
        return self.status


class API(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name')
    key = models.CharField(max_length=500, db_column='Key')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'API'

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    method = models.CharField(max_length=100, db_column='Method')
    api_key = models.ForeignKey(API, models.DO_NOTHING, db_column='APIKeyId', blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PaymentMethod'
        constraints = [
            models.UniqueConstraint(fields=['method'], name='uq_paymentmethod_method'),
        ]

    def __str__(self):
        return self.method


class Sender(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    sender_address = models.CharField(max_length=255, db_column='SenderAddress')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sender'

    def __str__(self):
        return self.sender_address


class NotificationType(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', unique=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'NotificationType'

    def __str__(self):
        return self.name


class NotificationTemplate(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    message = models.TextField(db_column='Message')
    subject = models.CharField(max_length=200, db_column='Subject', blank=True, null=True)
    is_active = models.BooleanField(db_column='IsActive', blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'NotificationTemplate'

    def __str__(self):
        return self.subject or f"Template {self.id}"


class GeneralSetup(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name')
    value = models.IntegerField(db_column='Value', blank=True, null=True)
    description = models.CharField(max_length=50, db_column='Description', blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GeneralSetup'

    def __str__(self):
        return self.name


# =========================
# MAIN ENTITY TABLES
# =========================

class Users(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    first_name = models.CharField(max_length=100, db_column='FirstName')
    last_name = models.CharField(max_length=100, db_column='LastName')
    other_name = models.CharField(max_length=100, db_column='OtherName', blank=True, null=True)
    email = models.EmailField(max_length=255, db_column='Email', unique=True)
    phone_no = models.CharField(max_length=20, db_column='PhoneNo', unique=True, blank=True, null=True)
    user_type = models.ForeignKey(UserType, models.DO_NOTHING, db_column='UserTypeId')
    user_status = models.ForeignKey(UserStatus, models.DO_NOTHING, db_column='UserStatusId')
    password_hash = models.BinaryField(db_column='PasswordHash')
    last_login_date = models.DateTimeField(db_column='LastLoginDate', blank=True, null=True)
    failed_login_attempts = models.IntegerField(db_column='FailedLoginAttempts', default=0)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'
        indexes = [
            models.Index(fields=['user_type'], name='idx_users_usertype'),
            models.Index(fields=['user_status'], name='idx_users_userstatus'),
        ]

    def __str__(self):
        # use user id when name not provided; rely on fields only (avoid joining FKs)
        return f"{self.first_name} {self.last_name} (#{self.id})"





class Product(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=200, db_column='Name')
    description = models.TextField(db_column='Description', blank=True, null=True)
    status = models.ForeignKey(Status, models.DO_NOTHING, db_column='StatusId')
    category = models.ForeignKey(CategoryType, models.DO_NOTHING, db_column='CategoryId')
    brand = models.ForeignKey(Brand, models.DO_NOTHING, db_column='BrandId')
    price = models.DecimalField(max_digits=18, decimal_places=2, db_column='Price')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Product'
        indexes = [
            models.Index(fields=['status'], name='idx_product_status'),
            models.Index(fields=['category'], name='idx_product_category'),
            models.Index(fields=['brand'], name='idx_product_brand'),
        ]

    def __str__(self):
        return self.name


class ProductDocument(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    product = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductId', blank=True, null=True)
    file_path = models.CharField(max_length=500, db_column='FilePath')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ProductDocument'

    def __str__(self):
        return self.file_path


class ProductVariant(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    product = models.ForeignKey(Product, models.DO_NOTHING, db_column='ProductId')
    sku = models.CharField(max_length=100, db_column='SKU', unique=True, blank=True, null=True)
    attributes = models.JSONField(db_column='Attributes', blank=True, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=3, db_column='Price')

    class Meta:
        managed = False
        db_table = 'ProductVariant'
        indexes = [
            models.Index(fields=['product'], name='idx_productvariant_product'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['sku'], name='uq_productvariant_sku'),
        ]

    def __str__(self):
        return self.sku or f"Variant {self.id} of Product #{self.product_id}"








class Transactions(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    payment_mode = models.ForeignKey(PaymentMethod, models.DO_NOTHING, db_column='PaymentModeId')
    order = models.ForeignKey('frontend.Orders', models.DO_NOTHING, db_column='OrderId', blank=True, null=True)
    status = models.ForeignKey(Status, models.DO_NOTHING, db_column='StatusId', blank=True, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=3, db_column='Amount', blank=True, null=True)
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='CurrencyId', blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Transactions'
        indexes = [
            models.Index(fields=['order'], name='idx_transactions_ord'),
            models.Index(fields=['payment_mode'], name='idx_transactions_payment'),
            models.Index(fields=['status'], name='idx_transactions_status'),
            models.Index(fields=['currency'], name='idx_transactions_currency'),
            models.Index(fields=['order', 'status'], name='idx_transactions_order_status'),
        ]

    def __str__(self):
        return f"Transaction {self.id} - Order {self.order_id} - Amount {self.amount}"


class OrderStatusHistory(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    order = models.ForeignKey('frontend.Orders', models.DO_NOTHING, db_column='OrderId')
    status = models.ForeignKey(Status, models.DO_NOTHING, db_column='StatusId')
    changed_date = models.DateTimeField(db_column='ChangedDate', blank=True, null=True)
    changed_by = models.BigIntegerField(db_column='ChangedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OrderStatusHistory'

    def __str__(self):
        return f"OrderHistory #{self.id} - Order {self.order_id} -> Status {self.status_id}"






class Warehouse(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', blank=True, null=True)
    address = models.ForeignKey('frontend.Address', models.DO_NOTHING, db_column='AddressId')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Warehouse'

    def __str__(self):
        return self.name or f"Warehouse {self.id}"


class WarehouseStock(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    warehouse = models.ForeignKey(Warehouse, models.DO_NOTHING, db_column='WarehouseId')
    product_variant = models.ForeignKey(ProductVariant, models.DO_NOTHING, db_column='ProductVariantId')
    quantity = models.IntegerField(db_column='Quantity')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'WarehouseStock'
        indexes = [
            models.Index(fields=['warehouse'], name='idx_warehousestock_wh'),
            models.Index(fields=['product_variant'], name='idx_warehousestock_variant'),
        ]

    def __str__(self):
        return f"Stock: Variant {self.product_variant_id} @ Warehouse {self.warehouse_id} = {self.quantity}"


class InventoryActionType(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    code = models.CharField(max_length=5, db_column='Code', unique=True)
    name = models.CharField(max_length=50, db_column='Name')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'InventoryActionType'

    def __str__(self):
        return self.name


class Reason(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    code = models.CharField(max_length=50, db_column='Code', unique=True)
    description = models.CharField(max_length=255, db_column='Description')
    action_type = models.ForeignKey(InventoryActionType, models.DO_NOTHING, db_column='ActionTypeId')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Reason'
        indexes = [
            models.Index(fields=['action_type'], name='idx_inventorytransxn_reason'),
        ]

    def __str__(self):
        return self.description


class InventoryTransaction(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    warehouse = models.ForeignKey(Warehouse, models.DO_NOTHING, db_column='WarehouseId')
    product_variant = models.ForeignKey(ProductVariant, models.DO_NOTHING, db_column='ProductVariantId')
    quantity_change = models.IntegerField(db_column='QuantityChange')
    reason = models.ForeignKey(Reason, models.DO_NOTHING, db_column='ReasonId')
    reference_id = models.BigIntegerField(db_column='ReferenceId', blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'InventoryTransaction'
        indexes = [
            models.Index(fields=['warehouse'], name='idx_inventorytransaction_wh'),
            models.Index(fields=['product_variant'], name='idx_invtorytransxn_variant'),
            models.Index(fields=['warehouse', 'product_variant'], name='idx_inventory_wh_variant'),
        ]
        constraints = [
            models.CheckConstraint(check=~models.Q(quantity_change=0), name='ck_inventory_qty_change_nonzero'),
        ]

    def __str__(self):
        return f"InvTx #{self.id}: Variant {self.product_variant_id} @ Wh {self.warehouse_id} -> {self.quantity_change}"




class PickupStation(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', blank=True, null=True)
    address = models.ForeignKey('frontend.Address', models.DO_NOTHING, db_column='AddressId')
    is_warehouse = models.BooleanField(db_column='IsWarehouse', blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PickupStation'

    def __str__(self):
        return self.name or f"PickupStation {self.id}"


class Notification(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    notification_type = models.ForeignKey(NotificationType, models.DO_NOTHING, db_column='NotificationTypeId')
    notification_template = models.ForeignKey(NotificationTemplate, models.DO_NOTHING, db_column='NotificationTemplateId')
    message = models.TextField(db_column='Message', blank=True, null=True)
    subject = models.CharField(max_length=300, db_column='Subject', blank=True, null=True)
    sender = models.ForeignKey(Sender, models.DO_NOTHING, db_column='SenderId')
    recipient = models.ForeignKey(Users, models.DO_NOTHING, db_column='Recipient')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Notification'

    def __str__(self):
        return self.subject or f"Notification #{self.id}"
