from django import forms
from .models import Product, CategoryType, Brand, WarehouseStock

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryType
        fields = '__all__'

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

class InventoryForm(forms.ModelForm):
    class Meta:
        model = WarehouseStock
        fields = '__all__'

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['rating', 'title', 'message']
