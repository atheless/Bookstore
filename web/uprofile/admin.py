from django.contrib import admin

from uprofile.models import UProfile, Seller


# Register your models here.

@admin.register(UProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_image']
    raw_id_fields = ['user']

@admin.register(Seller)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['created_by',
                    'creation_date',
                    'status',
                    'approved_by',
                    'seller_name',
                    'legal_seller_address',
                    'contact_phone',
                    'seller_email',
                    'description',
                    ]
    raw_id_fields = ['created_by']



