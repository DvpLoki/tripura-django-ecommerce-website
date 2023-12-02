from django.contrib import admin
from .models import Category,Product,SubProduct,Attribute,AttributeValue,Image,StockControl

admin.site.register(Attribute)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['slug','is_active']
    prepopulated_fields={'slug':('name',)}
    list_editable=['is_active']
    list_filter=['is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['slug','description']
    prepopulated_fields={'slug':('name',)}


class ProductImageInline(admin.TabularInline):
    model=Image

class AttributeValueinline(admin.TabularInline):
    model=AttributeValue

class stockcontrolInline(admin.TabularInline):
    model=StockControl

@admin.register(SubProduct)
class SubproductAdmin(admin.ModelAdmin):
    inlines=[AttributeValueinline,ProductImageInline,stockcontrolInline]
    list_display=['product','name','is_active','cost_price','selling_price','is_default','created_at','updated_at']
    list_editable=['cost_price','selling_price','is_active']
    list_filter=['is_active','cost_price','selling_price','created_at','is_default','attributevalue']

    