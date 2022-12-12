from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from decimal import *

# Create your models here.

class user_type_option(models.TextChoices):
    Customer = 'Customer', ('customer')
    Pharmacists = 'Pharmacists', ('pharmacists')
    Doctor = 'Doctor', ('doctor')
    Hospitals = 'Hospitals', ('hospitals')

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
    whatapp_mobile_number = models.CharField(max_length=10,null=True, blank=True)
    email = models.EmailField(('email address'), unique=True,null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)   # For HOTP Verification
    user_type = models.CharField(
                max_length=15,
                choices=user_type_option.choices,
                default=user_type_option.Customer,
            )
    gender = models.CharField(
                max_length=10,
                choices=gender_option.choices,
                default=gender_option.Male,
        )

    age = models.IntegerField(default=0, blank=True)

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


class AddressBook(models.Model):
    user = models.ForeignKey('CustomeUser', on_delete=models.CASCADE, blank=True, null=True)
    house_number =  models.CharField(max_length=30, blank=True, null=True)
    landmark =  models.CharField(max_length=300, blank=True, null=True)
    locality =  models.CharField(max_length=300, blank=True, null=True)
    pincode =  models.CharField(max_length=6, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state =  models.CharField(max_length=30, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    country =  models.CharField(max_length=30, blank=True, null=True)


class Order(models.Model):
    ORDER_STATUS = (
        ('initiated', 'Initiated'),
        ('in transition', 'In transition'),
        ('out for delivery', 'Out for delivery'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey('CustomeUser',on_delete=models.DO_NOTHING, blank=True, null=True)
    order_number = models.CharField(max_length=50, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    stickers_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='initiated')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_options = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=100, blank=True, null=True)
    comments = models.CharField(max_length=400, blank=True, null=True, default='')

    class Meta:
        db_table = 'Order'
        ordering = ['-created']
    
    def __str__(self):
        return str(self.order_number)

class Medicine(models.Model):
    name = models.CharField(max_length=300,blank=True, null=True, unique=True)
    description = models.CharField(max_length=300,blank=True, null=True)
    manufracturing_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    category = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=200, blank=True, null=True)
    price = models.IntegerField(default=0)
    offer_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    discount_type = models.CharField(max_length=50, blank=True, null=True)
    flavour = models.CharField(max_length=50, blank=True, null=True)
    consume_type = models.CharField(max_length=50, blank=True, null=True)
    storage = models.CharField(max_length=50, blank=True, null=True)
    precautions = models.CharField(max_length=300, blank=True, null=True)
    prescription_required = models.BooleanField(default=False)
    directions_for_use = models.CharField(max_length=300, blank=True, null=True)
    special_advice = models.CharField(max_length=300, blank=True, null=True)
    product_image = models.FileField(default='default.jpg', upload_to='medicine_pics', null=True, blank=True )

    def __str__(self):
        return str(self.name)

class orderMedicineData(models.Model):
    order = models.ForeignKey('Order',on_delete=models.CASCADE, blank=True, null=True)
    medicine = models.ForeignKey('Medicine',on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey('CustomeUser',on_delete=models.DO_NOTHING, blank=True, null=True)
    medicine = models.ForeignKey('Medicine',on_delete=models.DO_NOTHING, blank=True, null=True)
    quantity = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return str(self.user.mobile_number)


