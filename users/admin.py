from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import CustomeUser, Profile
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
  list_display = ['mobile_number', 'first_name', 'last_name', 'is_active','is_superuser']
  search_fields = ('mobile_number', 'first_name', 'last_name')
  ordering = ('mobile_number', )


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('profile_pic_preview',)

    def profile_pic_preview(self, obj):
        return obj.profile_pic_preview

    profile_pic_preview.short_description = 'Image preview'
    profile_pic_preview.allow_tags = True

    list_display = ('user', 'profile_pic_preview_table')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomeUser)