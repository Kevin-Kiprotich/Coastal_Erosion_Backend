import json
import uuid
from django.contrib.auth import authenticate,get_user_model
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
import os
from .models import AppUser

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
                    'institution':user.institution
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
        except User.DoesNotExist:
            return Response({'Success':False,'Message':"The email is not registered"})

class SignUpView(APIView):
    def post(self,request):
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        email=request.data.get('email')
        institution=request.data.get('institution')
        password=request.data.get('password')
        try:
            user=User.objects.get(email=email)
            return Response({'Success':False,'Message':"The email is already taken"})
        except User.DoesNotExist:
            user=AppUser.objects.create_user(username=username,email=email, password=password,
                                          first_name=first_name,last_name=last_name,institution=institution)
            
            return Response({'Success': True,'Message': "Account Created Successfully"})
