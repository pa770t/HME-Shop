from django.contrib import admin
from .models import ContactInfo, News, Category, SubCategory, Product, Order, OrderItem, Brand, Cart, CartItem, ShippingAddress, Payment, PromoCode

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    ordering = ['-created_at']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    ordering = ['-created_at']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    ordering = ['-created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['slug', 'created_at', 'updated_at']
    ordering = ('-created_at', )
    fieldsets = (
        (None, {'fields': ('name', 'model_name', 'description', 'image', 'price', 'stock_quantity', 'brand', 'category', 'subcategory', 'slug', 'created_at', 'updated_at', )}),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ['-created_at']

admin.site.register(OrderItem)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    ordering = ['-created_at']

@admin.register(Cart)
class BrandAdmin(admin.ModelAdmin):
    ordering = ['-created_at']

@admin.register(CartItem)
class BrandAdmin(admin.ModelAdmin):
    ordering = ['-created_at']

@admin.register(ShippingAddress)
class BrandAdmin(admin.ModelAdmin):
    ordering = ['-created_at']

@admin.register(Payment)
class BrandAdmin(admin.ModelAdmin):
    ordering = ['-created_at']

admin.site.register(ContactInfo)
admin.site.register(PromoCode)
