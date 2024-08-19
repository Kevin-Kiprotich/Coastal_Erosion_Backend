import json
import uuid
from django.contrib.auth import authenticate,get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import login
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.models import auth
from django.http import JsonResponse,HttpResponse, HttpResponseBadRequest,HttpResponseForbidden
import os
from .models import AppUser,countryStats

userEmail=''
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email)
        try:
            user = AppUser.objects.get(email=email)
            if user.check_password(password):
                # login(user)
                # serializer = UserSerializer(user)
                access_token = AccessToken.for_user(user)
                refresh_token=RefreshToken.for_user(user)
                # access_token=str(refresh.access_token)
                payload={
                    'email':user.email,
                    'user_metadata':{
                        'firstName':user.first_name,
                        'lastName':user.last_name,
                        'institution':user.institution,
                        'sector':user.sector,
                        'role':user.role,
                        'country':user.country 
                    } 
                }
                # refresh_token = refresh.access_token
                # refresh_token.payload.update(payload)
                # return Response({'Success':True,'Message':"Login Successfull",'first_name':user.first_name,'last_name':user.last_name,'email':user.email})
                if user.is_active:
                    auth.login(request,user)
                    response = Response({
                        'Success': True,
                        'token': str(access_token),
                        'user_metadata':payload
                    })

                    

                    return response
                else:
                    mail_subject = "Activate your user account."
                    message = render_to_string("template_activate_account.html", {
                        'first_name': user.first_name,
                        'last_name':user.last_name,
                        'domain': get_current_site(request).domain,
                        'uid': urlsafe_base64_encode(force_bytes(email)),
                        'token': account_activation_token.make_token(user),
                        "protocol": 'https' if request.is_secure() else 'http'
                    })
                    mail = EmailMessage(mail_subject, message, to=[email])
                    mail.content_subtype = 'html'  # Set the content type to HTML
                    # email.attach_alternative(message, 'text/html')
                    if mail.send():
                        print("Email sent")
                        return HttpResponseBadRequest(JsonResponse({'message':'Your email is not verified. Check your email to activate your account'}))
                    else:
                        print('Email not sent')
                        return HttpResponseBadRequest(JsonResponse({'message':'Email is not valid'}))
                    
            else:
                return HttpResponseBadRequest(JsonResponse({'message':'Email and Password do not match'}))
        except AppUser.DoesNotExist:
            return HttpResponseBadRequest((JsonResponse({'message':'Email is not registered. Register an account to proceed.'})))
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
        return redirect('http://coastalerosion.rcmrd.org/#/login')
    

def update(request,uidb64,token):
    User=get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(email=uid)
        print(user)
        
        userEmail=user.email
        print(userEmail)
    except:
        user=None
    if user is not None and account_activation_token.check_token(user, token):
        return redirect(f'http://217.21.122.249/#/update-password?access_token={token}&uid={uidb64}')


class SignUpView(APIView):
    def post(self,request):
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        email=request.data.get('email')
        institution=request.data.get('institution')
        sector=request.data.get('sector')
        role=request.data.get('role')
        otherroles=request.data.get('other_roles')
        country=request.data.get('country')
        password=request.data.get('password')
        userobject={
            'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'institution':institution,
            'sector':sector,
            'role':role,
            'otherroles':otherroles,
            'country':country,
            'password':password
        }
        print(userobject)
        try:
            user=AppUser.objects.get(email=email)
            return HttpResponseBadRequest(JsonResponse({'Success':False,'message':"The email is already taken",'email':email}))
        except AppUser.DoesNotExist:
            user=""
            if not otherroles:
                user=AppUser.objects.create_user(email=email, password=password,
                                          first_name=first_name,last_name=last_name,institution=institution,sector=sector,role=role,country=country)
                
            else:
                user=AppUser.objects.create_user(email=email, password=password,
                                          first_name=first_name,last_name=last_name,institution=institution,sector=sector,role=otherroles,country=country)
            user.is_active=False
            user.save()
            print(user.email)
            # try:
            #     country=countryStats.objects.get(country=user.country)
            #     country.users+=1
            #     country.save()
            # except countryStats.DoesNotExist:
            #     country=countryStats(country=user.country,users=1)
            #     country.save()

            mail_subject = "Activate your user account."
            message = render_to_string("template_activate_account.html", {
                'first_name': first_name,
                'last_name':last_name, 
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(email)),
                'token': account_activation_token.make_token(user),
                "protocol": 'https' if request.is_secure() else 'http'
            })
            mail = EmailMessage(mail_subject, message, to=[email])
            mail.content_subtype = 'html'  # Set the content type to HTML
            # email.attach_alternative(message, 'text/html')
            print('sending message')
            if mail.send():
                print("Email sent")
                return Response({'Success': True,'message': "Account Created Successfully",'user':userobject})
            else:
                print('Email not sent')
                return HttpResponseBadRequest(JsonResponse({'message':'Could not send a verification email. Make sure you entered a valid email'}))
      
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
            mail = EmailMessage(mail_subject, message, to=[email])
            mail.content_subtype = 'html'  # Set the content type to HTML
            # email.attach_alternative(message, 'text/html')
            # email = EmailMultiAlternatives(mail_subject, message, to=[email])
            if mail.send():
                print(f"Email sent for {email}")
                return Response({'Success':True,'Message':'Check your email for a verification alert'})
            else:
                print(f'Email not sent for {email}')
                return HttpResponseBadRequest(JsonResponse({'Success':False,'Message':'Trouble sending email. Make sure you have entered a valid email.'}))
            
        except AppUser.DoesNotExist:
            return HttpResponseBadRequest(JsonResponse({'Success':False,'Message':'Email is not registered'}))

class changePassword(APIView):
    def post(self,request):
        User=get_user_model()
        # email=request.data.get('email')
        token=request.data.get('token')
        uidb64=request.data.get('uid')
        password=request.data.get('password')
        uid=force_str(urlsafe_base64_decode(uidb64))
        
        print(uid)
        print(password)
        
        try:
            user=User.objects.get(email=uid)
            user.set_password(password)
            user.save()
            payload={
                    'email':user.email,
                    'user_metadata':{
                        'firstName':user.first_name,
                        'lastName':user.last_name,
                        'institution':user.institution,
                        'sector':user.sector,
                        'role':user.role,
                        'country':user.country
                    }
                }
            print('passoword changed')
            return Response({'Success':True,'Message':'Password Changed Successfully','metadata':payload })
        except User.DoesNotExist:
            return HttpResponseBadRequest(JsonResponse({'Success':False,'Message':'Email not recognized'}))


def userStatistics(request):
    template=loader.get_template('userStats.html')
    return HttpResponse(template.render())


class GetUser(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        payload={
                    'email':user.email,
                    'user_metadata':{
                        'firstName':user.first_name,
                        'lastName':user.last_name,
                        'institution':user.institution,
                        'sector':user.sector,
                        'role':user.role,
                        'country':user.country 
                    } 
                }
        return Response({'Success':True,'metadata':payload})


class LogoutView(APIView):
    def post(self,request):
        email=request.data.get('email')
        auth.logout(request)
        return Response({
                        'Success': True,
                        'Message': 'Login successful',
                        'metadata': {},
                    })
