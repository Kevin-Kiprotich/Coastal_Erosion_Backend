from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('userStats/',views.userStatistics,name='Stats'),
    path('login/', views.LoginView.as_view()),
    path('signup/',views.SignUpView.as_view(),name='Sign Up'),
    path('getuser/', views.GetUser.as_view(),name='Get User'),
    path('logout/',views.LogoutView.as_view()),
    path('passwordupdate/',views.UpdatePassword.as_view()),
    path('resetpassword/',views.changePassword.as_view()),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('update/<uidb64>/<token>', views.update, name='update'),
]

