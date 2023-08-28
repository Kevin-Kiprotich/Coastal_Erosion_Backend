from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


# Create your models here.
class AppUser(AbstractUser):
    username=None
    email=models.EmailField(_("email address"),unique=True)
    institution=models.CharField(max_length=255,null=False)
    sector=models.CharField(max_length=40,null=False)
    role=models.CharField(max_length=255)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=CustomUserManager()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        app_label="users"
        verbose_name_plural="Users"

class countryStats(models.Model):
    country=models.CharField(max_length=100,null=False)
    country_code=models.CharField(max_length=100,null=False)
    users=models.CharField(max_length=100,null=False)

    def __str__(self):
        return f"{self.country}"
    class Meta:
        verbose_name_plural="Stats By Country"
