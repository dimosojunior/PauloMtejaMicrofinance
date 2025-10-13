from django.shortcuts import render,redirect


# Create your views here.
from django.shortcuts import render,get_object_or_404
from App.serializers import *
from App.models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#REST FRAMEWORK
from rest_framework import status
from rest_framework.response import Response

#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView


#------------------------GENERIC VIEWs-------------------
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


#------------------------ VIEW SETS-------------------
from rest_framework.viewsets import ModelViewSet


#------FILTERS, SEARCH AND ORDERING
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter

#------PAGINATION-------------
from rest_framework.pagination import PageNumberPagination




#----------------CREATING A CART------------------------
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from App.serializers import *
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view

# Create your views here.

# class UserView(APIView):

#   def get(self,request, format=None):
#       return Response("User Account View", status=200)

#   def post(self,request, format=None):

#       return Response("Creating User", status=200)


from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# class RegistrationView(generics.CreateAPIView):
#     queryset = MyUser.objects.all()
#     serializer_class = DjangoReactUserSerializer
#     permission_classes = (permissions.AllowAny,)

# class ReactLoginView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = DjangoReactUserSerializer
    
#     def create(self, request, *args, **kwargs):
#         user = self.get_object()
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.models import Token






import os







class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            username = serializer.validated_data.get('username')
            phone = serializer.validated_data.get('phone')
            Location = serializer.validated_data.get('Location')
            is_admin = serializer.validated_data.get('is_admin', False)
            is_staff = serializer.validated_data.get('is_staff', False)
            is_cashier = serializer.validated_data.get('is_cashier', False)

            JinaLaKituo_id = request.data.get('JinaLaKituo')

            # if MyUser.objects.filter(email=email).exists():
            #     return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            # if MyUser.objects.filter(username=username).exists():
            #     return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)


            JinaLaKituo = None
            if JinaLaKituo_id:
                try:
                    JinaLaKituo = VituoVyote.objects.get(id=JinaLaKituo_id)
                except VituoVyote.DoesNotExist:
                    return Response({'error': 'Invalid JinaLaKituo ID'}, status=status.HTTP_400_BAD_REQUEST)


            user = MyUser.objects.create_user(
                email=email, 
                password=password, 
                username=username, 
                phone=phone, 
                is_admin=is_admin,
                is_staff=is_staff,
                is_cashier=is_cashier,
                JinaLaKituo=JinaLaKituo,
                Location=Location
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):

        #kupata informations za user anayejaribu kuaupdate informations zake ili
        #kuziatach kwenye email kwenda kwa admin
        user = request.user
        username = request.user.username
        email = request.user.email
        phone = request.user.phone
        link = "https://mfugajismart.net/MfugajiSmart/"
        myemail = "juniordimoso8@gmail.com"

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            

            subject = "Micro Finance"
            message = f"Umefanikiwa kubadilisha taarifa"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [myemail]

            

            send_mail(subject, message, from_email, recipient_list, fail_silently=True)


            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class ReactLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)





class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            Token.objects.filter(user=user).delete()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)





class UserDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # Assuming you have a serializer for User data
        serializer = UserDataSerializer(user)
        return Response(serializer.data)






class SendOTPView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = MyUser.objects.get(email=email)
            except MyUser.DoesNotExist:
                return Response({'error': 'Mtumiaji mwenye email hii teyari yupo.'}, status=status.HTTP_400_BAD_REQUEST)

            otp_instance = OTP.objects.create(user=user)

            subject = "Mfugaji Smart"
            message = f"OTP codes zako kutoka Mfugaji Smart \n \n {otp_instance.otp}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            

            print(f"OTP : {otp_instance.otp}")

            return Response({'message': 'OTP codes zimetumwa kwenye email yako.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Umefanikiwa kubadilisha password yako kikamilifu'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)