from django.contrib import admin
from .models import AppUser,countryStats



# Register your models here.
class AppUserAdmin(admin.ModelAdmin):
    list_display=("email","institution",)

class countryStatsAdmin(admin.ModelAdmin):
    list_display=('country','users')
    
admin.site.register(countryStats,countryStatsAdmin)
admin.site.register(AppUser,AppUserAdmin)