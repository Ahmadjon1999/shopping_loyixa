from django.db import models
from uuid import uuid4
from django.contrib.auth.models import  AbstractUser,AbstractBaseUser, PermissionsMixin
from app_one.managers import UserManager

from phonenumber_field.modelfields import PhoneNumberField


# class CustomUser(AbstractUser):
#     phone_number  = PhoneNumberField(verbose_name="Telefon raqam", null=True , blank=True)
#     profile_image = models.ImageField(verbose_name="Profil rasimi", upload_to="profiles/", null=True, blank=True)
#     address       = models.CharField(verbose_name="Yashash manzili", max_length=255)
#
#     class Meta:
#         verbose_name = 'Foydalanuvchi'                            {% empty  %}
#         verbose_name_plural = 'Foydalanuvchilar'



class User(AbstractBaseUser, PermissionsMixin):
    first_name =    models.CharField(verbose_name="Ism", max_length=120, null=True, blank=True)
    last_name =     models.CharField(verbose_name="Familya", max_length=120, null=True, blank=True)
    email         = models.EmailField(verbose_name="Email/Gmail", null=True, blank=True)
    phone_number  = PhoneNumberField(verbose_name="Telefon raqam", unique=True, null=True, blank=True)
    profile_image = models.ImageField(verbose_name="Profil rasimi", upload_to="profiles/", null=True, blank=True)
    address       = models.CharField(verbose_name="Yashash manzili", max_length=255, null=True, blank=True)
    is_superuser  = models.BooleanField(verbose_name="Superadmin statusi", default=False)
    is_staff      = models.BooleanField(verbose_name="Xodimlik statusi", default=False)
    is_active     = models.BooleanField(verbose_name="Profil aktivligi", default=True)
    objects       = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f"{self.first_name}"




class Category(models.Model):
    name = models.CharField(verbose_name="Kategoriya nomi",max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural= 'Kategoriyalar'





class Product(models.Model):
    id          = models.UUIDField(verbose_name="ID", primary_key=True, unique=True, editable=False, default=uuid4)
    name        = models.CharField(verbose_name="Maxsulot nomi", max_length=100)
    price       = models.DecimalField(verbose_name="Maxsulot narxi", max_digits=12, decimal_places=2)
    image       = models.ImageField(verbose_name="Maxsulot Surati", upload_to="products/")
    in_stock    = models.IntegerField(verbose_name="Ombordagi soni", default=1)
    category    = models.ForeignKey(verbose_name="Maxsulot Kategoryasi", to=Category, on_delete=models.PROTECT)
    description = models.TextField(verbose_name="Maxsulot Tavsifi", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Maxsulot'
        verbose_name_plural= 'Maxsulotlar'




class Cart(models.Model):
    user = models.ForeignKey(verbose_name="Foydalanuvchini", to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(verbose_name="Maxsulot nomini", to=Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name="maxsulot soni", default=1)
    created = models.DateTimeField(verbose_name="Xarid vaqti", auto_now_add=True)

    class Meta:
        verbose_name = "Savatchadagi maxsulot"
        verbose_name_plural = "Savatchadagi maxsulotlar"

    def __str__(self):
        return f"{self.user.first_name}   {self.product.name}  {self.count} dona  {self.created.strftime('%Y-%m-%d %H:%M')}"

    @property
    def total_price(self):
        return self.product.price * self.count



class Transaction(models.Model):
    id = models.UUIDField(verbose_name="ID", primary_key=True, unique=True, editable=False, default=uuid4)
    user = models.ForeignKey(verbose_name="Foydalanuvchi", to=User, on_delete=models.CASCADE)
    product_name = models.CharField(verbose_name="Maxsulot nomi", max_length=255)
    amount = models.DecimalField(verbose_name="Sariflangan pul miqdori", max_digits=12, decimal_places=2)
    created = models.DateTimeField(verbose_name="Xarid vaqti",auto_now_add=True)

    class Meta:
        verbose_name = "Tranzaksiya"
        verbose_name_plural = "Tranzaksiyalar-(O'tkazmalar)"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.first_name} -- {self.product_name} -- {self.amount} -- {self.created.strftime('%Y-%m-%d %H:%M')}"

# -- {self.product_name.price}
