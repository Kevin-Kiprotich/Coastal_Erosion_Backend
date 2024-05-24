from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

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
    class Meta:
        verbose_name_plural="Country Statistics"
