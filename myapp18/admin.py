from django.contrib import admin
from .models import Product, Category, Client, Order
from django.db.models import F


def increase_stock(modeladmin, request, queryset):
    print(queryset)
    queryset.update(stock=F('stock')+50)
    increase_stock.short_description = "Increase stock of selected by 50"

class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'category', 'price', 'available','stock')
    actions = [increase_stock]



# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)


