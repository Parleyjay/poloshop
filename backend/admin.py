from django.contrib import admin
from .models import *

from backend.models import User

from frontend.models import Country, Region, Orders, Review




class AddressTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type","created_date","created_by")


class APIAdmin(admin.ModelAdmin):
    list_display = ("id", "name","key","created_date","created_by")

class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name","created_date","created_by")

class CategoryTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "category","created_date","created_by")


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name","country","currency_code","created_date","created_by")


class DeliveryModeAdmin(admin.ModelAdmin):
    list_display = ("id", "name","created_date","created_by")

class GeneralSetupAdmin(admin.ModelAdmin):
    list_display = ("id", "name","value","description","created_date","created_by")



class InventoryActionTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "code","name","created_date","created_by")

class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name","country_code","created_date","created_by")

class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name","region_code","created_date","created_by")



class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "method","api_key","created_date","created_by")

class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name","created_date","created_by")

# FRONT END MODELS


class OrdersAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id","amount","status","created_date","created_by")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id","product","rating","subject","message","created_date","created_by")




admin.site.register(User)
admin.site.register(CategoryType,CategoryTypeAdmin)
admin.site.register(Product)
admin.site.register(Status)
admin.site.register(GeneralSetup,GeneralSetupAdmin)
admin.site.register(NotificationType,NotificationTypeAdmin)

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

admin.site.register(NotificationTemplate)
admin.site.register(PickupStation)
admin.site.register(Country,CountryAdmin)
admin.site.register(Region,RegionAdmin)
admin.site.register(Orders,OrdersAdmin)
admin.site.register(Review,ReviewAdmin)
