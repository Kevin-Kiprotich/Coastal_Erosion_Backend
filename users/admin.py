from django.contrib import admin
from .models import AppUser



# Register your models here.
class AppUserAdmin(admin.ModelAdmin):
    list_display=("email","institution",)

admin.site.register(AppUser,AppUserAdmin)