from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from .models import (AppUser,countryStats, CountryCount,
                     SectorCount, InstitutionCount, RoleCount,
                     MonthlyUserRegistration)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import admin
from django.http import HttpResponse
import csv

# Register your models here.
@admin.action(description='Export all items as CSV')
def export_as_csv(modeladmin, request, queryset=None):
    # Fetch all records for the model
    queryset = modeladmin.get_queryset(request)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{queryset.model.__name__}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([field.name for field in queryset.model._meta.fields])  # Write headers

    for obj in queryset:
        writer.writerow([getattr(obj, field.name) for field in queryset.model._meta.fields])  # Write data rows

    return response

class AppUserAdmin(admin.ModelAdmin):
    list_display=("email","institution",)
    
    def delete_view(self,request,object_id, extra_context=None):
        user=AppUser.objects.get(id=object_id)
        if request.method=='POST':
            user_country=user.country
            print(user.first_name)
            
            #response=super().delete_view(request, object_id, extra_context=extra_context)
            # print('Delete view response',response)
            try:
                country=countryStats.objects.get(country=user_country)
                country.users-=1
                country.save()
                print(f'No of users in {country.country} is currently {country.users}')
            except countryStats.DoesNotExist:
                pass
            
            user.delete()
            return HttpResponseRedirect(reverse('admin:users_appuser_changelist'))
        return self._delete_view(request,object_id,extra_context=extra_context)

class CountryCountAdmin(admin.ModelAdmin):
    list_display=('country','user_count')
    actions = [export_as_csv]

class SectorCountAdmin(admin.ModelAdmin):
    list_display =('sector','user_count')
    actions = [export_as_csv]

class InstitutionCountAdmin(admin.ModelAdmin):
    list_display = ('institution','user_count')
    actions = [export_as_csv]

class RoleCountAdmin(admin.ModelAdmin):
    list_display = ('role', 'user_count')
    actions = [export_as_csv]

class MonthlyUserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('month','year', 'registration_count')
    actions = [export_as_csv]

# admin.site.register(countryStats,countryStatsAdmin)
admin.site.register(AppUser,AppUserAdmin)
admin.site.register(CountryCount, CountryCountAdmin)
admin.site.register(SectorCount, SectorCountAdmin)
admin.site.register(InstitutionCount, InstitutionCountAdmin)
admin.site.register(RoleCount, RoleCountAdmin)
admin.site.register(MonthlyUserRegistration, MonthlyUserRegistrationAdmin)