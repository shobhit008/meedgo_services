from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe

# Create your models here.

class user_type_option(models.TextChoices):
    Chemist = 'chemist', ('chemist')
    User = 'user', ('user')
    Other = 'other', ('other')

class gender_option(models.TextChoices):
    Female = 'F', ('Female')
    Male = 'M', ('Male')
    Other = 'O', ('Other')


# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, mobile_number, password, **extra_fields):
        """
        Create and save a User with the given mobile_number and password.
        """
        if not mobile_number:
            raise ValueError(_('The mobile_number must be set'))
        mobile_number = self.normalize_email(mobile_number)
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile_number, password, **extra_fields):
        """
        Create and save a SuperUser with the given mobile_number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(mobile_number, password, **extra_fields)




class CustomeUser(AbstractUser):
    username = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(('email address'), unique=True,null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)   # For HOTP Verification
    user_type = models.CharField(
                max_length=10,
                choices=user_type_option.choices,
                default=user_type_option.User,
            )
    gender = models.CharField(
                max_length=10,
                choices=gender_option.choices,
                default=gender_option.Male,
        )

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class Profile(models.Model):
   user = models.OneToOneField(CustomeUser, on_delete=models.CASCADE, null=True, blank=True)
   image = models.FileField(default='default.jpg', upload_to='profile_pics', null=True, blank=True )
   
   @property
   def profile_pic_preview(self):
      if self.image:
         return mark_safe('<img src="{}" width="300" height="300" />'.format(self.image.url))
      return ""

   @property
   def profile_pic_preview_table(self):
      if self.image:
         return mark_safe('<img src="{}" width="40" height="40" />'.format(self.image.url))
      return ""


   def __str__(self):
      return f'{self.user.username} Profile'