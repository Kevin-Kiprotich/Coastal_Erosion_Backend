import json
import uuid
from django.contrib.auth import authenticate,get_user_model
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from verify_email.email_handler import send_verification_email
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
import os
from .models import AppUser

userEmail=''
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = AppUser.objects.get(email=email)
            if user.check_password(password):
                # login(user)
                # serializer = UserSerializer(user)
                refresh=RefreshToken.for_user(user)
                # access_token=str(refresh.access_token)
                payload={
                    'email':user.email,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'institution':user.institution,
                    'sector':user.sector,
                    'role':user.role,
                }
                access_token = refresh.access_token
                access_token.payload.update(payload)
                # return Response({'Success':True,'Message':"Login Successfull",'first_name':user.first_name,'last_name':user.last_name,'email':user.email})
                return Response({
                    'Success': True,
                    'Message': 'Login successful',
                    'access_token': str(access_token),
                })
            else:
                return Response({'Success':False,'Message': 'Email and Password do not match'})
        except AppUser.DoesNotExist:
            return Response({'Success':False,'Message':"The email is not registered"})
def activate(request,uidb64,token):
    User=get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(email=uid)
        print(user)
    except:
        user=None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('https://www.google.com')
def update(request,uidb64,token):
    User=get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(email=uid)
        print(user)
    except:
        user=None
    if user is not None and account_activation_token.check_token(user, token):
        return redirect('https://www.google.com')


class SignUpView(APIView):
    def post(self,request):
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        email=request.data.get('email')
        institution=request.data.get('institution')
        sector=request.data.get('sector')
        role=request.data.get('role')
        password=request.data.get('password')
        try:
            user=AppUser.objects.get(email=email)
            return Response({'Success':False,'Message':"The email is already taken"})
        except AppUser.DoesNotExist:
            user=AppUser.objects.create_user(email=email, password=password,
                                          first_name=first_name,last_name=last_name,institution=institution,sector=sector,role=role)
            user.is_active=False
            user.save()
            appUser=AppUser.objects.get(email=email)
            mail_subject = "Activate your user account."
            message = render_to_string("template_activate_account.html", {
                'first_name': first_name,
                'last_name':last_name, 
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(email)),
                'token': account_activation_token.make_token(user),
                "protocol": 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(mail_subject, message, to=[email])
            if email.send():
                print("Email sent")
            else:
                print('Email not sent')
            return Response({'Success': True,'Message': "Account Created Successfully"})
      
class UpdatePassword(APIView):
    def post(self,request):
        email=request.data.get('email')
        try:
            user=AppUser.objects.get(email=email)
            mail_subject = "Reset Your Password." 
            message = render_to_string("template_change_password.html", {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(email)),
                'token': account_activation_token.make_token(user),
                "protocol": 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(mail_subject, message, to=[email])
            if email.send():
                print(f"Email sent for {email}")
                return Response({'Success':True,'Message':'Check your email for a verification alert'})
            else:
                print(f'Email not sent for {email}')
                return Response({'Success':False,'Message':'Trouble sending email. Make sure you have entered a valid email.'})
            
        except AppUser.DoesNotExist:
            return Response({'Success':False,'Message':'Email is not registered'})

class changePassword(APIView):
    def post(self,request):
        User=get_user_model()
        email=request.data.get('email')
        password=request.data.get('password')
        try:
            user=User.objects.get(email=email)
            user.set_password(password)
            return Response({'Success':True,'Message':'Password Changed Successfully'})
        except User.DoesNotExist:
            return Response({'Success':False,'Message':'Email not recognized'})
