from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import CustomeUser, Profile, AddressBook, Order, Medicine, orderMedicineData, Cart, userIssue, orderCartData
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# Register your models here.
admin.site.site_header  =  "Meedgo admin" 
admin.site.site_title  =  "Meedgo admin site"
admin.site.index_title  =  "Meedgo Admin"


class UserAdmin(BaseUserAdmin):
  fieldsets = (
      (None, {'fields': ('mobile_number', 'password', )}),
      (('Personal info'), {'fields': ('first_name', 'last_name')}),
      (('Permissions'), {'fields': ('is_active', 'is_staff',
                                     'groups', 'user_permissions')}),
  )
  add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('mobile_number', 'password1', 'password2'),
      }),
  )
  list_display = ['mobile_number', 'first_name', 'last_name', 'is_active', 'is_admin','is_superuser']
  search_fields = ('mobile_number', 'first_name', 'last_name')
  ordering = ('mobile_number', )


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('profile_pic_preview',)

    def profile_pic_preview(self, obj):
        return obj.profile_pic_preview

    profile_pic_preview.short_description = 'Image preview'
    profile_pic_preview.allow_tags = True

    list_display = ('user', 'profile_pic_preview_table')

class AddressBookAdmin(admin.ModelAdmin):
    """
    This class is used to display the AddressBook model in the admin page.
    """
    list_display = ('user', 'house_number', 'landmark', 'locality', 'pincode', 'city', 'state', 'is_default', 'country')

class OrderAdmin(admin.ModelAdmin):
    """
    This class is used to display the Order model in the admin page.
    """
    list_display = ('user', 'order_number', 'total', 'stickers_price', 'discount', 'shipping_cost', 'status', 'created')

class MedicineAdmin(admin.ModelAdmin):
    """
    This class is used to display the Order model in the admin page.
    """
    list_display = ('name', 'manufracturing_date', 'expiry_date', 'category', 'price', 'brand')

class OrderMedicineDataAdmin(admin.ModelAdmin):
    """
    This class is used to display the OrderMedicineData model in the admin page.
    """
    list_display = ('id', 'order', 'medicine')
    search_fields = ('order',)

class CartDataAdmin(admin.ModelAdmin):
    """
    This class is used to display the OrderMedicineData model in the admin page.
    """
    list_display = ('id', 'user', 'medicine', 'quantity')

class userIssueAdmin(admin.ModelAdmin):
    """
    This class is used to display the OrderMedicineData model in the admin page.
    """
    list_display = ('issue_number' ,'user', 'category', 'status', 'created', 'updated')

class OrderCartDataAdmin(admin.ModelAdmin):
    """
    This class is used to display the OrderCartDataAdmin model in the admin page.
    """
    list_display = ('id', 'order', 'cart')
    search_fields = ('order',)


admin.site.register(orderCartData, OrderCartDataAdmin)
admin.site.register(userIssue, userIssueAdmin)
admin.site.register(Cart, CartDataAdmin)
admin.site.register(orderMedicineData, OrderMedicineDataAdmin)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(AddressBook, AddressBookAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomeUser)