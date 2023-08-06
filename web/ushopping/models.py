from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(null=False, max_length=60, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='productsImage/', blank=True, max_length=200)
    name = models.CharField(max_length=60)
    publisher = models.CharField(max_length=60, blank=False)
    year = models.IntegerField(blank=False)
    author = models.CharField(max_length=50, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CONDITIONSP = (
        ('0', 'New'),
        ('1', 'Used as new'),
        ('2', 'Heavily used'),
        ('3', 'Bad'),
    )

    condition = models.CharField(default='0', max_length=30, choices=CONDITIONSP, blank=False)
    short_description = models.TextField(max_length=600, blank=False)
    description = models.TextField(max_length=2000, blank=True, )
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Products'
        verbose_name = 'Product'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Product {self.name} of user {self.user}'


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='userto', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(blank=True)
    item = models.ForeignKey(Product, related_name='productto', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.item.name
