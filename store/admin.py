from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductStatus)
admin.site.register(ProductDocument)
admin.site.register(Product)
admin.site.register(InventoryStatus)
admin.site.register(Inventory)
admin.site.register(SavedProducts)
admin.site.register(Review)


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Customer)
admin.site.register(ShippingAddress)

#

# 
# admin.site.register(Inventory)
# admin.site.register(Review)
# admin.site.register(SavedProducts)
