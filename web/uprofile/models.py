from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField


class UProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_image = models.ImageField(
        upload_to='profileImages/',
        blank=True,
        max_length=40,
    )

    def __str__(self):
        return f'Profile of {self.user.username}'

    class Meta:
        verbose_name_plural = 'UProfiles'
        verbose_name = 'UProfiles'


class Seller(models.Model):
    created_by = models.OneToOneField(User, related_name='created_by', on_delete=models.CASCADE, primary_key=True)
    creation_date = models.DateTimeField(default=timezone.now)

    OPTIONS = (
        ('0', 'pending'),
        ('1', 'approved'),
        ('2', 'rejected'),
        ('3', 'undefined'),
    )
    status = models.CharField(default='0', choices=OPTIONS, max_length=20, blank=False)
    approved_by = models.ForeignKey(User, related_name='approved_by', on_delete=models.CASCADE, blank=True, null=True)
    seller_name = models.CharField(max_length=255,blank=False)
    country = CountryField()
    legal_seller_address = models.CharField(max_length=255,blank=False)
    contact_phone = models.PositiveSmallIntegerField(blank=False)
    seller_email = models.EmailField(max_length=50, blank=False)
    description = models.TextField(max_length=300, blank=False)

    class Meta:
        verbose_name_plural = 'Sellers'
        verbose_name = 'Seller'
        ordering = ('-creation_date',)
