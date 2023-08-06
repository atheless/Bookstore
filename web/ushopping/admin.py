from django.contrib import admin

from ushopping.models import Cart, Product, Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    def __str__(self):
        return self.name



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    raw_id_fields = ['item', 'user']

    def __str__(self):
        return self.item


