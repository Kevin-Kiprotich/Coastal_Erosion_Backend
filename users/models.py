from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from .managers import CustomUserManager


# Create your models here.
class AppUser(AbstractUser):
    username=None
    email=models.EmailField(_("email address"),unique=True,null=False)
    institution=models.CharField(max_length=255,null=True)
    sector=models.CharField(max_length=40,null=True)
    role=models.CharField(max_length=255,null=True)
    country=models.CharField(max_length=100,null=True, default='Kenya')
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=CustomUserManager()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    # def delete(self, *args,**kwargs):
    #     user_country=self.country
    #     super.delete(*args,**kwargs)
    #     try:
    #         country=countryStats.objects.get(country=user_country)
    #         country.users-=1
    #         country.save()
    #     except countryStats.DoesNotExist:
    #         pass
    class Meta:
        app_label="users"
        verbose_name_plural="Users"

class countryStats(models.Model):
    country=models.CharField(max_length=100,null=False)
    users=models.IntegerField(null=False,default=0)
    def __str__(self):
        return f"{self.country}"
    
    # class Meta:
    #     verbose_name_plural="Country Statistics"

class CountryCount(models.Model):
    country = models.CharField(max_length=100, unique=True)
    user_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.country.capitalize()}"
    
    class Meta:
        verbose_name_plural = "Country Statistics"


class SectorCount(models.Model):
    sector = models.CharField(max_length=40, unique=True)
    user_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.sector}"
    
    class Meta:
        verbose_name_plural = "Sector Statistics"


class InstitutionCount(models.Model):
    institution = models.CharField(max_length=255, unique=True)
    user_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.institution}"
    
    class Meta:
        verbose_name_plural = "Institution Statistics"


class RoleCount(models.Model):
    role = models.CharField(max_length=255, unique=True)
    user_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.role}"
    
    class Meta:
        verbose_name_plural = "Role Statistics"
    
class MonthlyUserRegistration(models.Model):
    month = models.CharField(max_length=20)  # Store month as a number from 1 (January) to 12 (December)
    year = models.IntegerField()
    registration_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('month', 'year')
        verbose_name_plural = "Registration per Month"

    def __str__(self):
        return f"{self.month}/{self.year}"