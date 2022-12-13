from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.admin import UserAdmin


class pharmacistDetailsAdmin(admin.ModelAdmin):
    """
    This class is used to display the pharmacistDetailsAdmin model in the admin page.
    """
    list_display = ('user', 'licence_image', 'registration_image', 'id_image', 'tan_number')

admin.site.register(pharmacistDetails, pharmacistDetailsAdmin)