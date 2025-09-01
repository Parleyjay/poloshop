from django.contrib import admin
from .models import *

from backend.models import User

from frontend.models import Country, Region



class AddressTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type")


class APIAdmin(admin.ModelAdmin):
    list_display = ("id", "name","key")

class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class CategoryTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "category")


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name","country","currency_code")


class DeliveryModeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class GeneralSetupAdmin(admin.ModelAdmin):
    list_display = ("id", "name","value","description",)



class InventoryActionTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "code","name")

class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name","country_code")

class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name","region_code")



class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "method","api_key")


admin.site.register(User)
admin.site.register(CategoryType,CategoryTypeAdmin)
admin.site.register(Product)
admin.site.register(Status)
admin.site.register(GeneralSetup,GeneralSetupAdmin)

admin.site.register(API,APIAdmin)
admin.site.register(UserType)
admin.site.register(UserStatus)
admin.site.register(Currency,CurrencyAdmin)
admin.site.register(Users)
admin.site.register(PaymentMethod,PaymentMethodAdmin)
admin.site.register(AddressType,AddressTypeAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(DeliveryMode)
admin.site.register(Warehouse)
admin.site.register(InventoryActionType,InventoryActionTypeAdmin)
admin.site.register(Reason)
admin.site.register(NotificationType)
admin.site.register(NotificationTemplate)
admin.site.register(PickupStation)
admin.site.register(Country,CountryAdmin)
admin.site.register(Region,RegionAdmin)
