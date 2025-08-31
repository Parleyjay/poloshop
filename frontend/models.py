from django.db import models


# ==
# REFERENCE TABLES
# ==





class Country(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name')
    country_code = models.CharField(max_length=5, db_column='CountryCode', unique=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Country'

    def __str__(self):
        return f"{self.name} ({self.country_code})"




class Region(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name')
    region_code = models.CharField(max_length=10, db_column='RegionCode', unique=True, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='CountryId')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Region'

    def __str__(self):
        return f"{self.name} ({self.region_code})" if self.region_code else self.name



# =========================
# MAIN ENTITY TABLES
# =========================



class Address(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    user = models.ForeignKey('backend.Users', models.DO_NOTHING, db_column='UserId')
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='CountryId')
    region = models.ForeignKey(Region, models.DO_NOTHING, db_column='RegionId')
    city = models.CharField(max_length=200, db_column='City', blank=True, null=True)
    address_type = models.ForeignKey('backend.AddressType', models.DO_NOTHING, db_column='AddressTypeId')
    digital_address = models.CharField(max_length=100, db_column='DigitalAddress', blank=True, null=True)
    street_name = models.CharField(max_length=200, db_column='StreetName', blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)
    is_default = models.BooleanField(db_column='IsDefault', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Address'
        indexes = [
            models.Index(fields=['user'], name='idx_address_user'),
            models.Index(fields=['country'], name='idx_address_country'),
            models.Index(fields=['region'], name='idx_address_region'),
            models.Index(fields=['address_type'], name='idx_address_addresstype'),
        ]

    def __str__(self):
        if self.street_name:
            return f"{self.street_name}, {self.city or ''} (User #{self.user_id})"
        return f"Address #{self.id} (User #{self.user_id})"








class Cart(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    user = models.ForeignKey('backend.Users', models.DO_NOTHING, db_column='UserId')
    status = models.ForeignKey('backend.Status', models.DO_NOTHING, db_column='StatusId')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Cart'
        indexes = [
            models.Index(fields=['user'], name='idx_cart_user'),
            models.Index(fields=['status'], name='idx_cart_status'),
        ]

    def __str__(self):
        return f"Cart #{self.id} (User #{self.user_id})"


class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    product = models.ForeignKey('backend.Product', models.DO_NOTHING, db_column='ProductId')
    cart = models.ForeignKey(Cart, models.DO_NOTHING, db_column='CartId')
    quantity = models.BigIntegerField(db_column='Quantity', default=1)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CartItem'
        indexes = [
            models.Index(fields=['cart'], name='idx_cartitem_cart'),
            models.Index(fields=['product'], name='idx_cartitem_product'),
            models.Index(fields=['cart', 'product'], name='idx_cartitem_cart_product'),
        ]

    def __str__(self):
        # use product name if available but avoid extra DB join by using product_id when necessary
        try:
            return f"{self.product.name} x {self.quantity} (Cart #{self.cart_id})"
        except Exception:
            return f"Product #{self.product_id} x {self.quantity} (Cart #{self.cart_id})"


class Orders(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    user = models.ForeignKey('backend.Users', models.DO_NOTHING, db_column='UserId')
    status = models.ForeignKey('backend.Status', models.DO_NOTHING, db_column='StatusId')
    cart = models.ForeignKey(Cart, models.DO_NOTHING, db_column='CartId', blank=True, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=3, db_column='Amount')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Orders'
        indexes = [
            models.Index(fields=['user'], name='idx_orders_user'),
            models.Index(fields=['status'], name='idx_orders_status'),
            models.Index(fields=['cart'], name='idx_orders_cart'),
            models.Index(fields=['user', 'status'], name='idx_orders_user_status'),
        ]

    def __str__(self):
        return f"Order {self.id} - User {self.user_id} - Amount {self.amount}"






class SavedItem(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    product = models.ForeignKey('backend.Product', models.DO_NOTHING, db_column='ProductId')
    user = models.ForeignKey('backend.Users', models.DO_NOTHING, db_column='UserId')
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SavedItem'

    def __str__(self):
        return f"SavedItem #{self.id} - User {self.user_id} saved Product {self.product_id}"


class Review(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    product = models.ForeignKey('backend.Product', models.DO_NOTHING, db_column='ProductId')
    user = models.ForeignKey('backend.Users', models.DO_NOTHING, db_column='UserId')
    rating = models.IntegerField(db_column='Rating', blank=True, null=True)
    subject = models.CharField(max_length=200, db_column='Subject', blank=True, null=True)
    message = models.TextField(db_column='Message', blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Review'
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5), name='ck_review_rating_1_5'),
        ]

    def __str__(self):
        return f"Review #{self.id} - Product {self.product_id} - Rating {self.rating}"




class Delivery(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    tracking_number = models.CharField(max_length=50, db_column='TrackingNumber')
    delivery_mode = models.ForeignKey('backend.DeliveryMode', models.DO_NOTHING, db_column='DeliveryModeId')
    order = models.ForeignKey(Orders, models.DO_NOTHING, db_column='OrderId')
    status = models.ForeignKey('backend.Status', models.DO_NOTHING, db_column='StatusId')
    address = models.ForeignKey(Address, models.DO_NOTHING, db_column='AddressId')
    dispatch_date = models.DateTimeField(db_column='DispatchDate', blank=True, null=True)
    delivery_date = models.DateTimeField(db_column='DeliveryDate', blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    created_by = models.BigIntegerField(db_column='CreatedBy', blank=True, null=True)
    updated_date = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)
    updated_by = models.BigIntegerField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Delivery'
        indexes = [
            models.Index(fields=['order'], name='idx_delivery_order'),
            models.Index(fields=['status'], name='idx_delivery_status'),
            models.Index(fields=['delivery_mode'], name='idx_delivery_mode'),
            models.Index(fields=['address'], name='idx_delivery_address'),
        ]

    def __str__(self):
        return f"Delivery {self.tracking_number} (Order #{self.order_id})"


