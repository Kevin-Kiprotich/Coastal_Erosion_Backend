from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from .models import AppUser,countryStats
from django.http import HttpResponseRedirect
from django.urls import reverse


# Register your models here.

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
class countryStatsAdmin(admin.ModelAdmin):
    list_display=('country','users')

admin.site.register(countryStats,countryStatsAdmin)
admin.site.register(AppUser,AppUserAdmin)