#GetTransactionSummaryView
#AddWatejaWoteView
#AddRipotiView
#RejeshoKwaSiku
#CountAllWatejaWoteView

from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import *
#import numpy as np
#from scipy.optimize import linprog
from django.http import HttpResponse
from datetime import datetime, timedelta
#import pyotp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import os
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
import requests

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from App.serializers import *


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

from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import send_mail
from django.conf import settings
#----------------CREATING A CART------------------------
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from App.serializers import *

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view
from django.db.models import Sum
from django.db import transaction
from django.utils.timezone import now, timedelta
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


import requests
from requests.auth import HTTPBasicAuth  
import requests
from django.http import JsonResponse
#from beem.sms import BeemSms  # Correct import

#from BeemAfrica import Authorize, AirTime, OTP, SMS
from django.utils.timezone import now

#------------FOR TWILIO
from twilio.rest import Client
from dotenv import load_dotenv
import os

import requests

import base64
import requests

# Load environment variables
load_dotenv()




def send_sms(phone_number, message):
    """
    Sends an SMS using Beem Africa API.
    
    :param phone_number: The recipient's phone number in international format (e.g., +255XXXXXXXXX)
    :param message: The message to send
    """
    url = os.getenv("BEEM_ACCOUNT_URL")
    api_key = os.getenv("BEEM_ACCOUNT_API_KEY")  # Replace with your Beem Africa API key
    secret_key = os.getenv("BEEM_ACCOUNT_SECRET_KEY")  # Replace with your Beem Africa secret key
    sender_id = os.getenv("BEEM_ACCOUNT_SENDER_ID")  # Replace with your approved Sender Name

    # Encode API key and secret key in base64
    auth_string = f"{api_key}:{secret_key}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_base64}"
    }
    
    payload = {
        "source_addr": sender_id,
        "encoding": 0,
        "schedule_time": "",
        "recipients": [{"recipient_id": 1, "dest_addr": phone_number}],
        "message": message
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP codes 4XX/5XX
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None




def send_sms_nextsms(phone_number, message):
    url = "https://messaging-service.co.tz/api/sms/v1/text/single"  # Test endpoint
    username = "dimoso"  # Replace with your actual username
    password = "Dimoso@9898"  # Replace with your actual password
    
    # Construct the Base64 authorization header
    auth_string = f"{username}:{password}"
    auth_header = f"Basic {base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": auth_header,
    }

    payload = {
        "from": "GGJ MKOPO",  # Replace with your approved sender ID
        "to": phone_number,  # Single phone number as a string
        "text": message,  # Message text
        "reference": "your-reference"  # Optional: Add a unique reference
    }

    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Debugging: Print response details
        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse and return JSON response
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS via NextSMS: {e}")
        return None




def send_sms_beem(phone_number, message):
    """
    Sends an SMS using Beem Africa API.

    :param phone_number: The recipient's phone number in international format (e.g., +255XXXXXXXXX)
    :param message: The message to send
    """
    url = os.getenv("BEEM_ACCOUNT_URL")
    api_key = os.getenv("BEEM_ACCOUNT_API_KEY")
    secret_key = os.getenv("BEEM_ACCOUNT_SECRET_KEY")
    sender_id = os.getenv("BEEM_ACCOUNT_SENDER_ID")

    # Encode API key and secret key in base64
    auth_string = f"{api_key}:{secret_key}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_base64}"
    }

    payload = {
        "source_addr": sender_id,
        "encoding": 0,
        "schedule_time": "",
        "recipients": [{"recipient_id": 1, "dest_addr": phone_number}],
        "message": message
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS via Beem Africa: {e}")
        return None





class SendSMSNextSMSView(View):
    def get(self, request):
        """
        Sends SMS to all users in the MyUser model using NextSMS.
        """
        users = MyUser.objects.all()
        message = "Hello! This is a test message from NextSMS."

        for user in users:
            if user.phone:
                phone_number = f"255{user.phone}"
                send_sms_nextsms(phone_number, message)

        return JsonResponse({"status": "success", "message": "SMS sent to all users via NextSMS."})

class SendSMSBeemView(View):
    def get(self, request):
        """
        Sends SMS to all users in the MyUser model using Beem Africa.
        """
        users = MyUser.objects.all()
        message = "Hello! This is a test message from Beem Africa."

        for user in users:
            if user.phone:
                send_sms_beem(user.phone, message)

        return JsonResponse({"status": "success", "message": "SMS sent to all users via Beem Africa."})














class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Update the password
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LatestVersionView(APIView):
    def get(self, request):
        latest_version = "7"
        return JsonResponse({"latest_version": latest_version})




class CountAllWatejaWoteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Count all wateja
            wateja_wote = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).count()

            # Count active wateja (wateja_hai)
            wateja_hai = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Ni_Mteja_Hai=True  # Adjust this filter based on your model's field for active status
            ).count()

            # Serialize the queryset if needed
            queryset_serializer = WatejaWoteSerializer(
                WatejaWote.objects.filter(
                    JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
                ), many=True
            )

            response_data = {
                'wateja_wote': wateja_wote,
                'wateja_hai': wateja_hai,
                'queryset_data': queryset_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except WatejaWote.DoesNotExist:
            return Response(
                {"error": "Failed to count wateja"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CountAllWatejaWoteNjeYaMikataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Count all wateja
            wateja_wote = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Nje_Ya_Mkata_Wote=True,
                JumlaYaDeni__gt=0
            ).count()

            # Count active wateja (wateja_hai)
            wateja_hai = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Nje_Ya_Mkata_Leo=True,  # Adjust this filter based on your model's field for active status
                JumlaYaDeni__gt=0
            ).count()

            # Serialize the queryset if needed
            queryset_serializer = WatejaWoteSerializer(
                WatejaWote.objects.filter(
                    JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
                ), many=True
            )

            response_data = {
                'wateja_wote': wateja_wote,
                'wateja_hai': wateja_hai,
                'queryset_data': queryset_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except WatejaWote.DoesNotExist:
            return Response(
                {"error": "Failed to count wateja"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class CountAllWamemalizaHawajakopaTenaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Count all wateja
            wateja_wote = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,   

                Nje_Ya_Mkata_Wote=False,
                Ni_Mteja_Hai=False,
                Wamemaliza_Hawajakopa_Tena=True,
                JumlaYaDeni__lte=0
            ).count()

            

            # Serialize the queryset if needed
            queryset_serializer = WatejaWoteSerializer(
                WatejaWote.objects.filter(
                    JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
                ), many=True
            )

            response_data = {
                'wateja_wote': wateja_wote,
                #'wateja_hai': wateja_hai,
                'queryset_data': queryset_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except WatejaWote.DoesNotExist:
            return Response(
                {"error": "Failed to count wateja"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class CountHawajarejeshaJanaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            today = now().date()
            yesterday = today - timedelta(days=1)
            # Count all wateja
            jumla_hawajarejesha_jana = MarejeshoCopies.objects.filter(
                JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=yesterday,
                FainiKwaSiku__gt=0
            ).count()

            

            # Serialize the queryset if needed
            queryset_serializer = MarejeshoCopiesSerializer(
                MarejeshoCopies.objects.filter(
                    JinaLaKituo__icontains=login_user_JinaLaKituo
                ), many=True
            )

            response_data = {
                'jumla_hawajarejesha_jana': jumla_hawajarejesha_jana,
                #'wateja_hai': wateja_hai,
                'queryset_data': queryset_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except WatejaWote.DoesNotExist:
            return Response(
                {"error": "Failed to count wateja"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class AddWatejaWoteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()

        # Automatically fill in fields from the user
        data['AmesajiliwaNa'] = user.username

        Interval_ya_malipo_yote = data.get('Interval', None)
        Interval_ya_malipo_yote = int(Interval_ya_malipo_yote)

        kiasi_cha_riba_iliyojazwa = data.get('Kiasicha_Riba_Kwa_Muda_Wa_Mkopo', 0)
        kiasi_cha_riba_iliyojazwa = int(kiasi_cha_riba_iliyojazwa)

        kiasi_cha_riba_iliyojazwa_in_asilimia = int(kiasi_cha_riba_iliyojazwa / 100)

        # Ensure 'KiasiAnachokopa' is provided
        kiasi_anachokopa = data.get('KiasiAnachokopa', None)
        if not kiasi_anachokopa:
            return Response({"error": "KiasiAnachokopa is required"}, status=400)

        kiasi_anachokopa = int(kiasi_anachokopa)
        # riba_kwa_mkopo = int((kiasi_anachokopa * 20) / 100)
        # deni_plus_riba = kiasi_anachokopa + riba_kwa_mkopo

        # # Perform calculations
        # rejesho_kwa_siku = round((deni_plus_riba) / 30, 0)

        # Get the value of 'Aina' for the new mteja
        aina_id = data.get('Aina', None)
        aina_instance = None
        if aina_id:
            try:
                aina_instance = AinaZaMarejesho.objects.get(id=aina_id)
            except AinaZaMarejesho.DoesNotExist:
                return Response({"error": "Invalid Aina ID"}, status=400)

        # Perform calculations based on the 'Aina' value
        if aina_instance and aina_instance.Aina == 'Muajiriwa':
            riba_kwa_mkopo = int((kiasi_anachokopa * kiasi_cha_riba_iliyojazwa) / 100)
            deni_plus_riba = kiasi_anachokopa + riba_kwa_mkopo
            rejesho_kwa_siku = 0

        elif aina_instance and aina_instance.Aina == 'Mfanya Kazi Wa Kituo':
            riba_kwa_mkopo = int((kiasi_anachokopa * kiasi_cha_riba_iliyojazwa) / 100)
            deni_plus_riba = kiasi_anachokopa + riba_kwa_mkopo
            rejesho_kwa_siku = 0

        else:
            # Default calculations if 'Aina' is not specified or doesn't match the above cases
            riba_kwa_mkopo = int((kiasi_anachokopa * kiasi_cha_riba_iliyojazwa) / 100)
            deni_plus_riba = kiasi_anachokopa + riba_kwa_mkopo
            rejesho_kwa_siku = round((deni_plus_riba) / 30, 0)
        
        # Assign calculated fields to the data
        data['RejeshoKwaSiku'] = int(rejesho_kwa_siku)
        data['JumlaYaDeni'] = deni_plus_riba
        data['Riba'] = riba_kwa_mkopo

        #data['KiasiAnachokopa'] = deni_plus_riba

        JinaKamiliLaMteja = data.get('JinaKamiliLaMteja', None)
        EmailYaMteja = data.get('EmailYaMteja', None)
        SimuYaMteja = data.get('SimuYaMteja', None)


        serializer = AddWatejaWoteSerializer(data=data)

        if serializer.is_valid():
            wateja = serializer.save()

            #hakikisha mteja anaanza rejesho kesho yake


            mteja_created_date = wateja.Created +  timedelta(days=1)

            mwisho_wa_malipo_month = Interval_ya_malipo_yote  # Adjust as needed
            mwisho_wa_malipo_days = mwisho_wa_malipo_month * 30
            #wateja.Up_To = wateja.Created + timedelta(days=mwisho_wa_malipo_days)


            wateja.Created = mteja_created_date #update Created date badala ya leo ianze kesho
            # Calculate and set `Up_To`
            wateja.Up_To = wateja.Created + timedelta(days=mwisho_wa_malipo_days)

            
            wateja.KiasiAnachokopa = deni_plus_riba
            wateja.Ni_Mteja_Hai = True

            #wateja.Amerejesha_Leo = True
            wateja.Nje_Ya_Mkata_Wote = False
            wateja.Nje_Ya_Mkata_Leo = False
            wateja.Wamemaliza_Hawajakopa_Tena = False

            if aina_instance and aina_instance.Aina == 'Muajiriwa':
                wateja.Amerejesha_Leo = False
            else:
                wateja.Amerejesha_Leo = True

            

            wateja.save()

            # Send SMS notification to the registered mteja
            # phone_number = data.get('SimuYaMteja')
            # message = f"Habari {wateja.JinaKamiliLaMteja}, umesajiliwa kikamilifu. Kiasi cha mkopo: {kiasi_anachokopa} TZS."
            # sms_response = self.send_sms(phone_number, message)

            print(f"Simu Ya Mteja {SimuYaMteja}")


            # Send SMS notification to the registered mteja
            message =f"Ndugu {JinaKamiliLaMteja}, umepokea mkopo wa Tsh{deni_plus_riba}/=, unatakiwa umalize kurejesha tarehe {wateja.Up_To}. Hatua zitachukuliwa kama hutomaliza. \n Mawasiliano: 0683133858"
            phone_number = f"255{wateja.SimuYaMteja}"

            sms_response = None
            try:
                sms_response = send_sms_nextsms(phone_number, message)
                if sms_response:
                    print(f"SMS sent successfully to {JinaKamiliLaMteja}.")
                else:
                    print(f"Failed to send SMS to {JinaKamiliLaMteja}.")
            except Exception as e:
                print(f"Error during SMS sending: {e}")

            

            

            # # Email notification to admin
            myemail = "juniordimoso8@gmail.com"
            subject = "GGJ - MKOPO"
            message = f"Ndugu {JinaKamiliLaMteja}, umepokea mkopo wa Tsh {deni_plus_riba}/=, unatakiwa umalize kurejesha tarehe {wateja.Up_To}. \n Hatua zitachukuliwa kama hutomaliza. \n Mawasiliano: 0683133858"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [EmailYaMteja]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)




# View for retrieving a post's details
class RetrieveWatejaWoteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = WatejaWote.objects.get(
                id=pk 
                #username=request.user.username
            )
            serializer = WatejaWoteSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except WatejaWote.DoesNotExist:
            return Response({'error': 'Mteja huyo hayupo'}, status=status.HTTP_404_NOT_FOUND)


# Update Post View
class UpdateWatejaWotePostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            post = WatejaWote.objects.get(
                id=pk 
                #username=request.user.username
            )


            user = request.user
            data = request.data.copy()

            # Automatically fill in fields from the user
            data['AmesajiliwaNa'] = user.username

            Interval_ya_malipo_yote = data.get('Interval', None)
            Interval_ya_malipo_yote = int(Interval_ya_malipo_yote)

            kiasi_cha_riba_iliyojazwa = data.get('Kiasicha_Riba_Kwa_Muda_Wa_Mkopo', 0)
            kiasi_cha_riba_iliyojazwa = int(kiasi_cha_riba_iliyojazwa)

            kiasi_cha_riba_iliyojazwa_in_asilimia = int(kiasi_cha_riba_iliyojazwa / 100)

            # Ensure 'KiasiAnachokopa' is provided
            kiasi_anachokopa = data.get('KiasiAnachokopa', None)
            if not kiasi_anachokopa:
                return Response({"error": "KiasiAnachokopa is required"}, status=400)

            kiasi_anachokopa = int(kiasi_anachokopa)
            # riba_kwa_mkopo = int((kiasi_anachokopa * 20) / 100)
            # deni_plus_riba = kiasi_anachokopa + riba_kwa_mkopo

            # # Perform calculations
            # rejesho_kwa_siku = round((deni_plus_riba) / 30, 0)

            # Get the value of 'Aina' for the new mteja
            aina_id = data.get('Aina', None)
            aina_instance = None
            if aina_id:
                try:
                    aina_instance = AinaZaMarejesho.objects.get(id=aina_id)
                except AinaZaMarejesho.DoesNotExist:
                    return Response({"error": "Invalid Aina ID"}, status=400)

            # Perform calculations based on the 'Aina' value
            if aina_instance and aina_instance.Aina == 'Muajiriwa':
                riba_kwa_mkopo = int((kiasi_anachokopa * kiasi_cha_riba_iliyojazwa) / 100)
                deni_plus_riba = kiasi_anachokopa + riba_kwa_mkopo
                rejesho_kwa_siku = 0

            elif aina_instance and aina_instance.Aina == 'Mfanya Kazi Wa Kituo':
                riba_kwa_mkopo = int((kiasi_anachokopa * kiasi_cha_riba_iliyojazwa) / 100)
                deni_plus_riba = kiasi_anachokopa + riba_kwa_mkopo
                rejesho_kwa_siku = 0

            else:
                # Default calculations if 'Aina' is not specified or doesn't match the above cases
                riba_kwa_mkopo = int((kiasi_anachokopa * kiasi_cha_riba_iliyojazwa) / 100)
                deni_plus_riba = kiasi_anachokopa + riba_kwa_mkopo
                rejesho_kwa_siku = round((deni_plus_riba) / 30, 0)
            
            # Assign calculated fields to the data
            data['RejeshoKwaSiku'] = int(rejesho_kwa_siku)
            data['JumlaYaDeni'] = deni_plus_riba
            data['Riba'] = riba_kwa_mkopo

            #data['KiasiAnachokopa'] = deni_plus_riba

            JinaKamiliLaMteja = data.get('JinaKamiliLaMteja', None)
            EmailYaMteja = data.get('EmailYaMteja', None)
            SimuYaMteja = data.get('SimuYaMteja', None)

            serializer = AddWatejaWoteSerializer(post, 
                data=request.data, 
                partial=True
            )

            if serializer.is_valid():
                #serializer.save()

                wateja = serializer.save()

                print(f"Deleting MarejeshoCopies with reg_no={wateja.reg_no}")
                MarejeshoCopiesTwo.objects.filter(
                    #JinaKamiliLaMteja=wateja.JinaKamiliLaMteja,
                    reg_no=wateja.reg_no
                ).delete()

                # Calculate and set `Up_To`
                tarehe_ya_leo = now()
                # wateja.Created = tarehe_ya_leo
                # wateja.Up_To = tarehe_ya_leo + timedelta(days=30)

                #hakikisha mteja anaanza rejesho kesho yake

                

                mteja_created_date = wateja.Created +  timedelta(days=1)

                mwisho_wa_malipo_month = Interval_ya_malipo_yote  # Adjust as needed
                mwisho_wa_malipo_days = mwisho_wa_malipo_month * 30
                #wateja.Up_To = wateja.Created + timedelta(days=mwisho_wa_malipo_days)


                wateja.Created = mteja_created_date #update Created date badala ya leo ianze kesho
                # Calculate and set `Up_To`
                wateja.Up_To = wateja.Created + timedelta(days=mwisho_wa_malipo_days)
                
                wateja.KiasiAnachokopa = deni_plus_riba
                wateja.RejeshoKwaSiku = rejesho_kwa_siku
                wateja.JumlaYaDeni = deni_plus_riba
                wateja.Riba = riba_kwa_mkopo
                wateja.KiasiAlicholipa = 0
                wateja.JumlaYaFainiZote = 0
                


                wateja.Ni_Mteja_Hai = True

                #wateja.Amerejesha_Leo = True
                wateja.Nje_Ya_Mkata_Wote = False
                wateja.Nje_Ya_Mkata_Leo = False
                wateja.Wamemaliza_Hawajakopa_Tena = False

                if aina_instance and aina_instance.Aina == 'Muajiriwa':
                    wateja.Amerejesha_Leo = False
                else:
                    wateja.Amerejesha_Leo = True

                wateja.save()



                #print("HELLLO TANZANIA")

                # Send SMS notification to the registered mteja
                # phone_number = data.get('SimuYaMteja')
                # message = f"Habari {wateja.JinaKamiliLaMteja}, umesajiliwa kikamilifu. Kiasi cha mkopo: {kiasi_anachokopa} TZS."
                # sms_response = self.send_sms(phone_number, message)

                # account_sid = os.getenv("TWILIO_ACCOUNT_SID")
                # auth_token = os.getenv("TWILIO_AUTH_TOKEN")
                # sender_number = os.getenv("TWILIO_SENDER_NUMBER")

                
                # client = Client(account_sid, auth_token)
                # message = client.messages \
                #             .create(
                #                 body=f"Ndugu {JinaKamiliLaMteja}, umepokea mkopo wa Tsh {deni_plus_riba}/=, unatakiwa umalize kurejesha tarehe {wateja.Up_To}. \n Hatua zitachukuliwa kama hutomaliza. \n Mawasiliano: 0683133858",
                #                 from_= sender_number,
                #                 #to='+255744973421'
                #                 to =f"+255{wateja.SimuYaMteja}"
                #             )

                # Sending SMS after registration
                
                # Send SMS notification to the registered mteja
                message = f"Ndugu {JinaKamiliLaMteja}, umepokea mkopo wa Tsh {deni_plus_riba}/=, unatakiwa umalize kurejesha tarehe {wateja.Up_To}. \n Hatua zitachukuliwa kama hutomaliza. \n Mawasiliano: 0683133858"
                phone_number = f"255{wateja.SimuYaMteja}"

                sms_response = None
                try:
                    sms_response = send_sms_nextsms(phone_number, message)
                    if sms_response:
                        print(f"SMS sent successfully to {JinaKamiliLaMteja}.")
                    else:
                        print(f"Failed to send SMS to {JinaKamiliLaMteja}.")
                except Exception as e:
                    print(f"Error during SMS sending: {e}")

                

                # Email notification to admin
                myemail = "juniordimoso8@gmail.com"
                subject = "GGJ - MKOPO"
                message = f"Ndugu {JinaKamiliLaMteja}, umepokea mkopo wa Tsh {deni_plus_riba}/=, unatakiwa umalize kurejesha tarehe {wateja.Up_To}. \n Hatua zitachukuliwa kama hutomaliza. \n Mawasiliano: 0683133858"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [EmailYaMteja]
                send_mail(subject, message, from_email, recipient_list, fail_silently=True)



                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WatejaWote.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class GetAllWatejaWoteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            # categoryId = int(request.query_params.get('id'))
            # TypeId = int(request.query_params.get('TypeId'))
            


            queryset = WatejaWote.objects.filter(
                #FoodGroup__Jina__icontains = "Vyanzo vya Protini na Mafuta"
                JinaLaKituo__JinaLaKituo__icontains = login_user_JinaLaKituo
                # Type__id__icontains = TypeId
                ).order_by('JinaKamiliLaMteja')

            # # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            JumlaYaWote = queryset.count()

            

            serializer = WatejaWoteSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'JumlaYaWote':JumlaYaWote,
                
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[], "JumlaYaWote":0 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








# Delete Post View
class DeleteWatejaWotePostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            post = WatejaWote.objects.get(
                id=pk 
                #username=request.user.username
            )
            post.delete()
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)
        except WatejaWote.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)















class GetMarejeshoWatejaWoteHaiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            # categoryId = int(request.query_params.get('id'))
            # TypeId = int(request.query_params.get('TypeId'))
            


            queryset = WatejaWote.objects.filter(
                #FoodGroup__Jina__icontains = "Vyanzo vya Protini na Mafuta"
                JinaLaKituo__JinaLaKituo__icontains = login_user_JinaLaKituo,
                Ni_Mteja_Hai=True,
                Amerejesha_Leo=False
                # Type__id__icontains = TypeId
                ).order_by('JinaKamiliLaMteja')

            # # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            

            serializer = WatejaWoteSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class GetWatejaHaiWote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            # categoryId = int(request.query_params.get('id'))
            # TypeId = int(request.query_params.get('TypeId'))
            


            queryset = WatejaWote.objects.filter(
                #FoodGroup__Jina__icontains = "Vyanzo vya Protini na Mafuta"
                JinaLaKituo__JinaLaKituo__icontains = login_user_JinaLaKituo,
                Ni_Mteja_Hai=True
                #Amerejesha_Leo=False
                # Type__id__icontains = TypeId
                ).order_by('JinaKamiliLaMteja')

            # # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            JumlaYaWote = queryset.count()

            

            serializer = WatejaWoteSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'JumlaYaWote':JumlaYaWote,
                
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[], "JumlaYaWote":0 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#------------------CART AND CART ITEMS_-----================


class WatejaWoteCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

    #RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOrder/?pages=1&page_size=2
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOrder.objects.all().order_by('-id')
            #CategoryId = int(request.query_params.get('CategoryId'))
            queryset = WatejaWoteCart.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains = login_user_JinaLaKituo
                #user=user,
                #closed_order_state=False
                # CategoryId=CategoryId
                )
            main_total_price = queryset.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            serializer = WatejaWoteCartSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    


    def post(self, request):
        today = now().date()

        data = request.data
        JinaKamiliLaMteja = request.query_params.get('JinaKamiliLaMteja')

        # Get or create the cart
        cart, _ = WatejaWoteCart.objects.get_or_create(
            JinaKamiliLaMteja=JinaKamiliLaMteja,
            ordered=False
        )
        Mteja = WatejaWote.objects.get(id=data.get('Mteja'))

        # Validate KiasiChaRejeshoChaSiku
        KiasiChaRejeshoChaSiku = data.get('KiasiChaRejeshoChaSiku')
        rejesho_lake_kwa_siku = Mteja.RejeshoKwaSiku / 2
        if int(KiasiChaRejeshoChaSiku) < rejesho_lake_kwa_siku:
            return Response({
                'error': f'Kiasi ulichoingiza kipo chini ya Tsh. {rejesho_lake_kwa_siku} ambacho ni nusu ya rejesho la mteja analotakiwa kurejesha kila siku.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Add item to the cart
        cart_items = WatejaWoteCartItems(
            cart=cart,
            JinaKamiliLaMteja=JinaKamiliLaMteja,
            Mteja=Mteja,
            KiasiChaRejeshoChaSiku=KiasiChaRejeshoChaSiku,
            quantity=1
        )
        cart_items.save()

        # Update Mteja details
        JumlaYaDeni_Value = Mteja.JumlaYaDeni
        remained_deni = JumlaYaDeni_Value - int(KiasiChaRejeshoChaSiku)
        Mteja.JumlaYaDeni = remained_deni
        Mteja.KiasiAlicholipa = Mteja.KiasiAnachokopa - remained_deni

        Mteja.Amerejesha_Leo = True

        # Check if JumlaYaDeni is less than or equal to zero
        if Mteja.JumlaYaDeni <= 0:
            Mteja.Ni_Mteja_Hai = False
            Mteja.Wamemaliza_Hawajakopa_Tena = True
            Mteja.Nje_Ya_Mkata_Wote=False
            Mteja.Nje_Ya_Mkata_Leo = False

        # if Mteja.JumlaYaDeni <= 0 and Nje_Ya_Mkata_Wote == True :
        Mteja.save()

        # Update cart total price
        cart_items_queryset = WatejaWoteCartItems.objects.filter(
            JinaKamiliLaMteja=JinaKamiliLaMteja,
            cart=cart.id
        )
        cart.total_price = sum(item.KiasiChaRejeshoChaSiku for item in cart_items_queryset)
        cart.save()

        # Copy Mteja details to MarejeshoCopies
        MarejeshoCopies.objects.create(
            JinaKamiliLaMteja=Mteja.JinaKamiliLaMteja,
            JinaLaKituo=Mteja.JinaLaKituo.JinaLaKituo,
            SimuYaMteja=Mteja.SimuYaMteja,
            EmailYaMteja=Mteja.EmailYaMteja,
            Mahali=Mteja.Mahali,
            KiasiAnachokopa=Mteja.KiasiAnachokopa,
            KiasiAlicholipa=Mteja.KiasiAlicholipa,
            RejeshoKwaSiku=Mteja.RejeshoKwaSiku,
            JumlaYaDeni=Mteja.JumlaYaDeni,
            Riba=Mteja.Riba,
            AmesajiliwaNa=Mteja.AmesajiliwaNa,
            PichaYaMteja=Mteja.PichaYaMteja,
            Ni_Mteja_Hai=Mteja.Ni_Mteja_Hai,
            Up_To=Mteja.Up_To,
            reg_no=Mteja.reg_no,
            RejeshoLililoPokelewaLeo=KiasiChaRejeshoChaSiku
        )


        MarejeshoCopiesTwo.objects.create(
            JinaKamiliLaMteja=Mteja.JinaKamiliLaMteja,
            JinaLaKituo=Mteja.JinaLaKituo.JinaLaKituo,
            SimuYaMteja=Mteja.SimuYaMteja,
            EmailYaMteja=Mteja.EmailYaMteja,
            Mahali=Mteja.Mahali,
            KiasiAnachokopa=Mteja.KiasiAnachokopa,
            KiasiAlicholipa=Mteja.KiasiAlicholipa,
            RejeshoKwaSiku=Mteja.RejeshoKwaSiku,
            JumlaYaDeni=Mteja.JumlaYaDeni,
            Riba=Mteja.Riba,
            AmesajiliwaNa=Mteja.AmesajiliwaNa,
            PichaYaMteja=Mteja.PichaYaMteja,
            Ni_Mteja_Hai=Mteja.Ni_Mteja_Hai,
            Up_To=Mteja.Up_To,
            reg_no=Mteja.reg_no,
            RejeshoLililoPokelewaLeo=KiasiChaRejeshoChaSiku
        )

        #message = f"Ndugu {Mteja.JinaKamiliLaMteja}, tumepokea rejesho lako la Tsh {KiasiChaRejeshoChaSiku}/= tarehe {today}. Deni lako ni Tsh {Mteja.JumlaYaDeni}/= \n Mawasiliano: 0683133858 "
        phone_number = f"255{Mteja.SimuYaMteja}"
        message = f"Umefanikiwa: Rejesho la {Mteja.JinaKamiliLaMteja}, - Tsh {KiasiChaRejeshoChaSiku}/= tarehe {today} Tayari Limetumwa Makao Makuu. Deni lako ni Tsh {Mteja.JumlaYaDeni}/= \n Mawasiliano: 0683133858 "

        sms_response = None
        try:
            sms_response = send_sms_nextsms(phone_number, message)
            if sms_response:
                print(f"SMS sent successfully to {Mteja.JinaKamiliLaMteja}.")
            else:
                print(f"Failed to send SMS to {Mteja.JinaKamiliLaMteja}.")
        except Exception as e:
            print(f"Error during SMS sending: {e}")

        # Email notification to admin
        myemail = "juniordimoso8@gmail.com"
        subject = "GGJ - MKOPO"
        message = f"Umefanikiwa: Rejesho la {Mteja.JinaKamiliLaMteja}, - Tsh {KiasiChaRejeshoChaSiku}/= tarehe {today} Tayari Limetumwa Makao Makuu. Deni lako ni Tsh {Mteja.JumlaYaDeni}/= \n Mawasiliano: 0683133858 "
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [Mteja.EmailYaMteja]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        return Response({'success': 'Items Added To Your Cart and Mteja details copied successfully'})




    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = WatejaWoteCartItems.objects.get(id=data.get('id'))
        quantity = 1 #data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = WatejaWoteCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = WatejaWoteCart.objects.filter(user=user, ordered=False).first()
        queryset = WatejaWoteCartItems.objects.filter(cart=cart)
        serializer = WatejaWoteCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class MalipoYaFainiCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

    #RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOrder/?pages=1&page_size=2
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOrder.objects.all().order_by('-id')
            #CategoryId = int(request.query_params.get('CategoryId'))
            queryset = WatejaWoteCart.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains = login_user_JinaLaKituo
                #user=user,
                #closed_order_state=False
                # CategoryId=CategoryId
                )
            main_total_price = queryset.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            serializer = WatejaWoteCartSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    


    def post(self, request):
        data = request.data
        JinaKamiliLaMteja = request.query_params.get('JinaKamiliLaMteja')

        # Get or create the cart
        cart, _ = WatejaWoteCart.objects.get_or_create(
            JinaKamiliLaMteja=JinaKamiliLaMteja,
            ordered=False
        )
        Mteja = WatejaWote.objects.get(id=data.get('Mteja'))

        # Validate KiasiChaRejeshoChaSiku
        KiasiChaFainiChaSiku = data.get('KiasiChaFainiChaSiku')
        # rejesho_lake_kwa_siku = Mteja.RejeshoKwaSiku / 2
        # if int(KiasiChaFainiChaSiku) < rejesho_lake_kwa_siku:
        #     return Response({
        #         'error': f'Kiasi ulichoingiza kipo chini ya Tsh. {rejesho_lake_kwa_siku} ambacho ni nusu ya rejesho la mteja analotakiwa kurejesha kila siku.'
        #     }, status=status.HTTP_400_BAD_REQUEST)

        # Add item to the cart
        cart_items = WatejaWoteCartItems(
            cart=cart,
            JinaKamiliLaMteja=JinaKamiliLaMteja,
            Mteja=Mteja,
            KiasiChaFainiChaSiku=KiasiChaFainiChaSiku,
            quantity=1
        )
        cart_items.save()

        # Update Mteja details
        JumlaYa_Faini = Mteja.JumlaYaFainiZote
        remained_deni_la_faini = JumlaYa_Faini - int(KiasiChaFainiChaSiku)

        Mteja.JumlaYaFainiZote = remained_deni_la_faini
        
        Mteja.save()

        # Update cart total price
        cart_items_queryset = WatejaWoteCartItems.objects.filter(
            JinaKamiliLaMteja=JinaKamiliLaMteja,
            cart=cart.id
        )
        cart.total_price = sum(item.KiasiChaRejeshoChaSiku for item in cart_items_queryset)
        cart.save()

        # Copy Mteja details to MarejeshoCopies
        MalipoYaFainiCopies.objects.create(
            JinaKamiliLaMteja=Mteja.JinaKamiliLaMteja,
            JinaLaKituo=Mteja.JinaLaKituo.JinaLaKituo,
            SimuYaMteja=Mteja.SimuYaMteja,
            EmailYaMteja=Mteja.EmailYaMteja,
            Mahali=Mteja.Mahali,
            KiasiAnachokopa=Mteja.KiasiAnachokopa,
            KiasiAlicholipa=Mteja.KiasiAlicholipa,
            RejeshoKwaSiku=Mteja.RejeshoKwaSiku,
            JumlaYaDeni=Mteja.JumlaYaDeni,
            Riba=Mteja.Riba,
            AmesajiliwaNa=Mteja.AmesajiliwaNa,
            PichaYaMteja=Mteja.PichaYaMteja,
            Ni_Mteja_Hai=Mteja.Ni_Mteja_Hai,
            Up_To=Mteja.Up_To,
            reg_no=Mteja.reg_no,
            FainiIliyoPokelewaLeo=KiasiChaFainiChaSiku
        )

        return Response({'success': 'Faini imepokelewa na data  copied successfully'})




    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = WatejaWoteCartItems.objects.get(id=data.get('id'))
        quantity = 1 #data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = WatejaWoteCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = WatejaWoteCart.objects.filter(user=user, ordered=False).first()
        queryset = WatejaWoteCartItems.objects.filter(cart=cart)
        serializer = WatejaWoteCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





#TO DELETE SELECTED CART ITEM
class WatejaWoteDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = WatejaWoteCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            # cart_item.product.ProductQuantity += cart_item.quantity
            # cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except WatejaWoteCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






from django.utils.timezone import now
from django.db.models import Sum

class GetMarejeshoKwaSikuYaLeoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            today = now().date()
            queryset = MarejeshoCopies.objects.filter(
                JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=today,
                FainiKwaSiku__lte=0
            ).order_by('JinaKamiliLaMteja')

            # Calculate the total
            total_rejesho_leo = queryset.aggregate(Sum('RejeshoLililoPokelewaLeo'))['RejeshoLililoPokelewaLeo__sum'] or 0

            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            serializer = MarejeshoCopiesSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                'total_rejesho_leo': total_rejesho_leo,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": [], 'total_rejesho_leo': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilterMarejeshoYaSikuByDate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo

        startDate = request.query_params.get("startDate") #"2023-09-10"
        #endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        queryset = MarejeshoCopies.objects.filter(
            JinaLaKituo__icontains=login_user_JinaLaKituo,
            Created__date=startDate,
            FainiKwaSiku__lte=0
        ).order_by('JinaKamiliLaMteja')

        # Calculate the total
        total_rejesho_leo = queryset.aggregate(Sum('RejeshoLililoPokelewaLeo'))['RejeshoLililoPokelewaLeo__sum'] or 0

        serializer = MarejeshoCopiesSerializer(queryset, many=True)

        # Include the main total price in the response
        response_data = {
            "queryset": serializer.data,
            "total_rejesho_leo": total_rejesho_leo,
        }

        return Response(response_data, status=status.HTTP_200_OK)





class GetFainiKwaSikuYaLeoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            today = now().date()
            queryset = MalipoYaFainiCopies.objects.filter(
                JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=today
                #FainiKwaSiku__gt=0
            ).order_by('JinaKamiliLaMteja')

            # Calculate the total
            total_rejesho_leo = queryset.aggregate(Sum('FainiIliyoPokelewaLeo'))['FainiIliyoPokelewaLeo__sum'] or 0

            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            serializer = MalipoYaFainiCopiesSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                'total_rejesho_leo': total_rejesho_leo,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": [], 'total_rejesho_leo': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilterFainiYaSikuByDate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo

        startDate = request.query_params.get("startDate") #"2023-09-10"
        #endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        queryset = MalipoYaFainiCopies.objects.filter(
            JinaLaKituo__icontains=login_user_JinaLaKituo,
            Created__date=startDate
            #FainiKwaSiku__gt=0
        ).order_by('JinaKamiliLaMteja')

        # Calculate the total
        total_rejesho_leo = queryset.aggregate(Sum('FainiIliyoPokelewaLeo'))['FainiIliyoPokelewaLeo__sum'] or 0

        serializer = MalipoYaFainiCopiesSerializer(queryset, many=True)

        # Include the main total price in the response
        response_data = {
            "queryset": serializer.data,
            "total_rejesho_leo": total_rejesho_leo,
        }

        return Response(response_data, status=status.HTTP_200_OK)




class GetWatejaNjeYaMkatabaWoteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            #today = now().date()
            queryset = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Nje_Ya_Mkata_Wote=True,
                JumlaYaDeni__gt=0
                #Created__date=today
            ).order_by('JinaKamiliLaMteja')

            # Calculate the total
            #total_wateja = queryset.count() or 0

            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            JumlaYaWote = queryset.count()

            serializer = WatejaWoteSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                'JumlaYaWote': JumlaYaWote,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": [], 'JumlaYaWote': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class GetWamemalizaHawajakopaTenaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            #today = now().date()
            queryset = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Nje_Ya_Mkata_Wote=False,
                Ni_Mteja_Hai=False,
                Wamemaliza_Hawajakopa_Tena=True,
                JumlaYaDeni__lte=0
                #Created__date=today
            ).order_by('JinaKamiliLaMteja')

            # Calculate the total
            #total_wateja = queryset.count() or 0

            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            JumlaYaWote = queryset.count()

            serializer = WatejaWoteSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                'JumlaYaWote': JumlaYaWote,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": [], 'JumlaYaWote': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#---------------------Hizi mbili zinatumika tu kule kwenye kupokea marejesho pge

class GetMarejeshoWatejaWoteHaiView2(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            today = now().date()
            marejesho_queryset = MarejeshoCopies.objects.filter(
                JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=today,
                FainiKwaSiku__lte=0
            ).order_by('JinaKamiliLaMteja')

            # Calculate the total
            total_rejesho_leo = marejesho_queryset.aggregate(Sum('RejeshoLililoPokelewaLeo'))['RejeshoLililoPokelewaLeo__sum'] or 0

            # Use pagination
            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_marejesho_queryset(marejesho_queryset, request)

            serializer = MarejeshoCopiesSerializer(marejesho_queryset, many=True)

            response_data = {
                'marejesho_queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages,
                # 'current_page': page,
                'total_rejesho_leo': total_rejesho_leo,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "marejesho_queryset": [], 'total_rejesho_leo': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetFainiWatejaWoteHaiView2(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            today = now().date()
            faini_queryset = MalipoYaFainiCopies.objects.filter(
                JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=today
                #FainiKwaSiku__gt=0
            ).order_by('JinaKamiliLaMteja')

            # Calculate the total
            total_faini_leo = faini_queryset.aggregate(Sum('FainiIliyoPokelewaLeo'))['FainiIliyoPokelewaLeo__sum'] or 0

            # Use pagination
            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_faini_queryset(faini_queryset, request)

            serializer = MalipoYaFainiCopiesSerializer(faini_queryset, many=True)

            response_data = {
                'faini_queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages,
                # 'current_page': page,
                'total_faini_leo': total_faini_leo,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "faini_queryset": [], 'total_faini_leo': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











# class AddRipotiView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
#         user = request.user
#         data = request.data.copy()
#         today = now().date()

#         # Automatically fill in fields from the user
#         data['ImeweingizwaNa'] = user.username
        
#         # Filter Get Marejesho Ya Leo
#         marejesho_ya_leo = MarejeshoCopies.objects.filter(
#             JinaLaKituo__icontains=login_user_JinaLaKituo,
#             Created__date=today,
#             FainiKwaSiku__lte=0
#         )

#         # Calculate the total
#         jumla_marejesho_ya_leo = marejesho_ya_leo.aggregate(Sum('RejeshoLililoPokelewaLeo'))['RejeshoLililoPokelewaLeo__sum'] or 0
#         # Mwsho Get Marejesho Ya Leo

#         # Filter Get Marejesho Ya Leo
#         faini_za_leo = MarejeshoCopies.objects.filter(
#             JinaLaKituo__icontains=login_user_JinaLaKituo,
#             Created__date=today,
#             FainiKwaSiku__gt=0
#         )

#         # Calculate the total
#         jumla_faini_za_leo = faini_za_leo.aggregate(Sum('FainiKwaSiku'))['FainiKwaSiku__sum'] or 0
#         # Mwsho Get Marejesho Ya Leo
        

#         # Assign calculated fields to the data
#         data['JumlaMarejeshoYaLeo'] = int(jumla_marejesho_ya_leo)
#         data['JumlaFainiLeo'] = int(jumla_faini_za_leo)
        

#         serializer = RipotiSerializer(data=data)

#         if serializer.is_valid():
#             wateja = serializer.save()

#             # # Calculate and set `Up_To`
#             # wateja.Up_To = wateja.Created + timedelta(days=30)
#             # wateja.save()

#             # Email notification to admin
#             myemail = "juniordimoso8@gmail.com"
#             subject = "Gegwajo Microfinance"
#             message = "Ripoti ya leo imewekwa kikamilifu"
#             from_email = settings.EMAIL_HOST_USER
#             recipient_list = [myemail]
#             send_mail(subject, message, from_email, recipient_list, fail_silently=True)

#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)



class AddRipotiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        user = request.user
        data = request.data.copy()
        today = now().date()
        yesterday = today - timedelta(days=1)

        # Automatically fill in fields from the user
        data['ImeweingizwaNa'] = user.username

        idadi_ya_wenye_mikataba_hai = WatejaWote.objects.filter(
            JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
            Ni_Mteja_Hai=True
        ).count()
        data['IdadiYaWenyeMikatabaHai'] = idadi_ya_wenye_mikataba_hai

        idadi_ya_waliorejesha_leo = MarejeshoCopies.objects.filter(
            JinaLaKituo__icontains=login_user_JinaLaKituo,
            Created__date=today,
            FainiKwaSiku__lte=0
        ).count()
        data['IdadiYaWaliorejeshaLeo'] = idadi_ya_waliorejesha_leo

        idadi_ya_faini_zilizopokelewa_leo = MalipoYaFainiCopies.objects.filter(
            JinaLaKituo__icontains=login_user_JinaLaKituo,
            Created__date=today
            #FainiKwaSiku__gt=0
        ).count()
        data['IdadiYaFainiZilizopokelewaLeo'] = idadi_ya_faini_zilizopokelewa_leo


        # Calculate JumlaMarejeshoYaLeo
        marejesho_ya_leo = MarejeshoCopies.objects.filter(
            JinaLaKituo__icontains=login_user_JinaLaKituo,
            Created__date=today,
            FainiKwaSiku__lte=0
        )
        jumla_marejesho_ya_leo = marejesho_ya_leo.aggregate(Sum('RejeshoLililoPokelewaLeo'))['RejeshoLililoPokelewaLeo__sum'] or 0
        data['JumlaMarejeshoYaLeo'] = int(jumla_marejesho_ya_leo)

        # Calculate JumlaFainiLeo
        faini_za_leo = MalipoYaFainiCopies.objects.filter(
            JinaLaKituo__icontains=login_user_JinaLaKituo,
            Created__date=today,
            #FainiKwaSiku__gt=0
        )
        jumla_faini_za_leo = faini_za_leo.aggregate(Sum('FainiIliyoPokelewaLeo'))['FainiIliyoPokelewaLeo__sum'] or 0
        data['JumlaFainiLeo'] = int(jumla_faini_za_leo)

        # Get BakiJana (Balance of yesterday's Ripoti)
        baki_jana_ripoti = Ripoti.objects.filter(
            Created__date=yesterday,
            JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
        ).first()
        baki_jana = baki_jana_ripoti.Balance if baki_jana_ripoti else 0
        data['BakiJana'] = int(baki_jana)

        # Calculate MapatoYaJumla
        fomu_na_bima = int(data.get('FomuNaBima', 0))
        imetoka_kwabosi = int(data.get('ImetokaKwaBosi', 0))
        imetoka_kituo_jirani = int(data.get('ImetokaKituoJirani', 0))

        mapato_ya_jumla = (
            jumla_marejesho_ya_leo +
            jumla_faini_za_leo +
            baki_jana +
            fomu_na_bima +
            imetoka_kwabosi +
            imetoka_kituo_jirani
        )
        data['MapatoYaJumla'] = int(mapato_ya_jumla)

        # Calculate MatumiziYaJumla
        mkopo = int(data.get('Mkopo', 0))
        posho = int(data.get('Posho', 0))
        imeenda_kwabosi = int(data.get('ImeendaKwaBosi', 0))
        imeenda_kituo_jirani = int(data.get('ImeendaKituoJirani', 0))
        matumizi_mengine = int(data.get('MatumiziMengine', 0))

        matumizi_ya_jumla = (
            mkopo +
            posho +
            imeenda_kwabosi +
            imeenda_kituo_jirani +
            matumizi_mengine
        )
        data['MatumiziYaJumla'] = int(matumizi_ya_jumla)

        # Calculate Balance
        balance = mapato_ya_jumla - matumizi_ya_jumla
        data['Balance'] = int(balance)

        # Serialize and save the Ripoti instance
        serializer = RipotiSerializer(data=data)
        if serializer.is_valid():
            ripoti = serializer.save()

            #Copy Amerejesha_Leo = False to another model
            # Copy relevant records to MarejeshoCopies
            #ili mtu apigwe faini ni lazima hizo condition zote zifuatwe
            #YULE ANAYERUDISHA BAADA YAMWEZI HATAKIWI KUPIGWA FAINI
            mteja_hai = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Ni_Mteja_Hai=True,
                Amerejesha_Leo=False,
                Nje_Ya_Mkata_Wote=False
               # AinaZaMarejesho__icontains="Kila Siku"
            ).exclude(Aina__Aina__in=["Muajiriwa", "Mfanya Kazi Wa Kituo"])

            for mteja in mteja_hai:
                if not MarejeshoCopies.objects.filter(
                    JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
                    reg_no=mteja.reg_no, 
                    Created__date=today
                ).exists():
                    mteja.JumlaYaFainiZote = (mteja.JumlaYaFainiZote or 0) + 1000
                    mteja.save()
                    MarejeshoCopies.objects.create(
                        JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
                        JinaLaKituo=mteja.JinaLaKituo.JinaLaKituo,
                        SimuYaMteja=mteja.SimuYaMteja,
                        EmailYaMteja=mteja.EmailYaMteja,
                        Mahali=mteja.Mahali,
                        KiasiAnachokopa=mteja.KiasiAnachokopa,
                        KiasiAlicholipa=mteja.KiasiAlicholipa,
                        RejeshoKwaSiku=mteja.RejeshoKwaSiku,
                        JumlaYaDeni=mteja.JumlaYaDeni,
                        Riba=mteja.Riba,
                        AmesajiliwaNa=mteja.AmesajiliwaNa,
                        PichaYaMteja=mteja.PichaYaMteja,
                        Ni_Mteja_Hai=mteja.Ni_Mteja_Hai,
                        Up_To=mteja.Up_To,
                        reg_no=mteja.reg_no,
                        FainiKwaSiku=1000
                    )

                if not MarejeshoCopiesTwo.objects.filter(
                    JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
                    reg_no=mteja.reg_no, 
                    Created__date=today
                ).exists():
                    # mteja.JumlaYaFainiZote = (mteja.JumlaYaFainiZote or 0) + 1000
                    # mteja.save()
                    MarejeshoCopiesTwo.objects.create(
                        JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
                        JinaLaKituo=mteja.JinaLaKituo.JinaLaKituo,
                        SimuYaMteja=mteja.SimuYaMteja,
                        EmailYaMteja=mteja.EmailYaMteja,
                        Mahali=mteja.Mahali,
                        KiasiAnachokopa=mteja.KiasiAnachokopa,
                        KiasiAlicholipa=mteja.KiasiAlicholipa,
                        RejeshoKwaSiku=mteja.RejeshoKwaSiku,
                        JumlaYaDeni=mteja.JumlaYaDeni,
                        Riba=mteja.Riba,
                        AmesajiliwaNa=mteja.AmesajiliwaNa,
                        PichaYaMteja=mteja.PichaYaMteja,
                        Ni_Mteja_Hai=mteja.Ni_Mteja_Hai,
                        Up_To=mteja.Up_To,
                        reg_no=mteja.reg_no,
                        FainiKwaSiku=1000
                    )

            # Update Amerejesha_Leo for all WatejaWote after saving Ripoti
            wateja_aliorejesha_leo = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Amerejesha_Leo=True,
                Ni_Mteja_Hai=True
            )
            
            # Reset the Amerejesha_Leo field to False for those Wateja
            wateja_aliorejesha_leo.update(Amerejesha_Leo=False)

            # Email notification to admin
            myemail = "juniordimoso8@gmail.com"
            subject = "Gegwajo Microfinance"
            message = f"Ripoti ya leo ya kituo cha {login_user_JinaLaKituo} imewekwa kikamilifu"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [myemail]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)



class GetRipotiSikuYaLeoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            today = now().date()
            queryset = Ripoti.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=today
                #FainiKwaSiku__lte=0
            ).order_by('-Created')

            # Calculate the total
            #total_rejesho_leo = queryset.aggregate(Sum('RejeshoLililoPokelewaLeo'))['RejeshoLililoPokelewaLeo__sum'] or 0

            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            serializer = RipotiSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                #'total_rejesho_leo': total_rejesho_leo,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilterRipotiYaSikuByDate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo

        startDate = request.query_params.get("startDate") #"2023-09-10"
        #endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        queryset = Ripoti.objects.filter(
            JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
            Created__date=startDate
            #FainiKwaSiku__gt=0
        ).order_by('-Created')

        # Calculate the total
        #total_rejesho_leo = queryset.aggregate(Sum('RejeshoLililoPokelewaLeo'))['RejeshoLililoPokelewaLeo__sum'] or 0

        serializer = RipotiSerializer(queryset, many=True)

        # Include the main total price in the response
        response_data = {
            "queryset": serializer.data,
            #"total_rejesho_leo": total_rejesho_leo,
        }

        return Response(response_data, status=status.HTTP_200_OK)






class GetHawajarejeshaJanaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            today = now().date()
            yesterday = today - timedelta(days=1)

            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            today = now().date()
            queryset = MarejeshoCopies.objects.filter(
                JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=yesterday,
                FainiKwaSiku__gt=0
            ).order_by('JinaKamiliLaMteja')

            # Calculate the total
            #total_rejesho_leo = queryset.aggregate(Sum('FainiKwaSiku'))['FainiKwaSiku__sum'] or 0
            total_rejesho_leo = queryset.count()
            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            serializer = MarejeshoCopiesSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                'total_rejesho_leo': total_rejesho_leo,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": [], 'total_rejesho_leo': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilterHawajarejeshaByDate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        yesterday = today - timedelta(days=1)

        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo

        startDate = request.query_params.get("startDate") #"2023-09-10"
        #endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        queryset = MarejeshoCopies.objects.filter(
            JinaLaKituo__icontains=login_user_JinaLaKituo,
            Created__date=startDate,
            FainiKwaSiku__gt=0
        ).order_by('JinaKamiliLaMteja')

        # Calculate the total
        total_rejesho_leo = queryset.count()

        serializer = MarejeshoCopiesSerializer(queryset, many=True)

        # Include the main total price in the response
        response_data = {
            "queryset": serializer.data,
            "total_rejesho_leo": total_rejesho_leo,
        }

        return Response(response_data, status=status.HTTP_200_OK)







#-----------------GET MAREJESHO YOTE YA MTEJA--------------
class GetMarejeshoYoteYaMtejaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            JinaKamiliLaMteja = request.query_params.get('JinaKamiliLaMteja')
            reg_no = request.query_params.get('reg_no')

            # Filter entries for today
            today = now().date()
            queryset = MarejeshoCopiesTwo.objects.filter(
                JinaLaKituo__icontains=login_user_JinaLaKituo,
                JinaKamiliLaMteja__icontains=JinaKamiliLaMteja,
                reg_no__icontains=reg_no
                #Created__date=today,
                #FainiKwaSiku__lte=0
            ).order_by('id')

            # Calculate the total
            total_rejesho_leo = queryset.aggregate(Sum('RejeshoLililoPokelewaLeo'))['RejeshoLililoPokelewaLeo__sum'] or 0

            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            serializer = MarejeshoCopiesTwoSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                'total_rejesho_leo': total_rejesho_leo,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": [], 'total_rejesho_leo': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











#--------------------KUFUTA REJESHO NA FAINI--------------


class DeleteRejeshoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        #login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:

            today = now().date()
            yesterday = today - timedelta(days=1)
            # Fetch the MarejeshoCopies instance
            marejesho = MarejeshoCopies.objects.get(id=pk)

            # Fetch the corresponding WatejaWote instance
            mteja = WatejaWote.objects.get(
                JinaKamiliLaMteja=marejesho.JinaKamiliLaMteja,
                JinaLaKituo__JinaLaKituo__icontains=marejesho.JinaLaKituo
            )

            # Delete matching entries from MarejeshoCopiesTwo
            MarejeshoCopiesTwo.objects.filter(
                JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
                reg_no=mteja.reg_no,
                Created__date=today
            ).delete()

            # Update JumlaYaDeni and KiasiAlicholipa in WatejaWote
            mteja.JumlaYaDeni += marejesho.RejeshoLililoPokelewaLeo
            mteja.KiasiAlicholipa = mteja.KiasiAnachokopa - mteja.JumlaYaDeni

            # Reset Amerejesha_Leo to False
            mteja.Amerejesha_Leo = False
            mteja.Ni_Mteja_Hai = True
            mteja.Wamemaliza_Hawajakopa_Tena = False
            mteja.save()

            # Delete the MarejeshoCopies instance
            marejesho.delete()

            return Response({'message': 'Rejesho limefutwa kikamilifu, na mteja amesasishwa.'}, status=status.HTTP_200_OK)

        except MarejeshoCopies.DoesNotExist:
            return Response({'error': 'Rejesho halijapatikana.'}, status=status.HTTP_404_NOT_FOUND)
        except WatejaWote.DoesNotExist:
            return Response({'error': 'Mteja halijapatikana.'}, status=status.HTTP_404_NOT_FOUND)




class DeleteFainiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            # Fetch the MarejeshoCopies instance
            marejesho = MalipoYaFainiCopies.objects.get(id=pk)

            # Fetch the corresponding WatejaWote instance
            mteja = WatejaWote.objects.get(
                JinaKamiliLaMteja=marejesho.JinaKamiliLaMteja,
                JinaLaKituo__JinaLaKituo__icontains=marejesho.JinaLaKituo
            )

            # Update JumlaYaDeni and KiasiAlicholipa in WatejaWote
            mteja.JumlaYaFainiZote += marejesho.FainiIliyoPokelewaLeo
            #mteja.KiasiAlicholipa = mteja.KiasiAnachokopa - mteja.JumlaYaDeni

            # Reset Amerejesha_Leo to False
            #mteja.Amerejesha_Leo = False
            mteja.save()

            # Delete the MarejeshoCopies instance
            marejesho.delete()

            return Response({'message': 'Faini imefutwa kikamilifu, na mteja amesasishwa.'}, status=status.HTTP_200_OK)

        except MarejeshoCopies.DoesNotExist:
            return Response({'error': 'Rejesho halijapatikana.'}, status=status.HTTP_404_NOT_FOUND)
        except WatejaWote.DoesNotExist:
            return Response({'error': 'Mteja halijapatikana.'}, status=status.HTTP_404_NOT_FOUND)








#-----------------NJE YA MKATABA LEO-----------------


class GetWatejaNjeYaMkatabaLeoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            #today = now().date()
            queryset = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Nje_Ya_Mkata_Leo=True
                #Created__date=today
            ).order_by('JinaKamiliLaMteja')

            # Calculate the total
            #total_wateja = queryset.count() or 0

            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            JumlaYaWote = queryset.count()

            serializer = WatejaWoteSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                'JumlaYaWote': JumlaYaWote,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": [], "JumlaYaWote": 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#-------------------NJE YA MKATABA TAREHE-----------------

class GetNjeYaMkatabaTareheFulaniView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            today = now().date()
            yesterday = today - timedelta(days=1)

            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            today = now().date()
            queryset = NjeYaMkatabaCopies.objects.filter(
                JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=today
                
            ).order_by('JinaKamiliLaMteja')

            # Calculate the total
            #total_rejesho_leo = queryset.aggregate(Sum('FainiKwaSiku'))['FainiKwaSiku__sum'] or 0
            
            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            JumlaYaWote = queryset.count()

            serializer = NjeYaMkatabaCopiesSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                'JumlaYaWote': JumlaYaWote,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": [], 'JumlaYaWote': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilterNjeYaMkatabaTareheFulaniByDate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        yesterday = today - timedelta(days=1)

        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo

        startDate = request.query_params.get("startDate") #"2023-09-10"
        #endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        queryset = NjeYaMkatabaCopies.objects.filter(
            JinaLaKituo__icontains=login_user_JinaLaKituo,
            Created__date=startDate
            #FainiKwaSiku__gt=0
        ).order_by('JinaKamiliLaMteja')

        # Calculate the total
        JumlaYaWote = queryset.count()

        serializer = NjeYaMkatabaCopiesSerializer(queryset, many=True)

        # Include the main total price in the response
        response_data = {
            "queryset": serializer.data,
            "JumlaYaWote": JumlaYaWote,
        }

        return Response(response_data, status=status.HTTP_200_OK)




class DeleteRipotiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        #login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Fetch the MarejeshoCopies instance
            marejesho = Ripoti.objects.get(id=pk)

            # Delete the MarejeshoCopies instance
            marejesho.delete()

            return Response({'message': 'Ripoti imefutwa kikamilifu.'}, status=status.HTTP_200_OK)

        except Ripoti.DoesNotExist:
            return Response({'error': 'Ripoti haijapatikana.'}, status=status.HTTP_404_NOT_FOUND)
        except Ripoti.DoesNotExist:
            return Response({'error': 'Ripoti haijapatikana.'}, status=status.HTTP_404_NOT_FOUND)











class OngezaKituoView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    

    def post(self, request, *args, **kwargs):
        current_time = now()
        print(f"current_time", current_time)
        # user = request.user
        data = request.data.copy()

    
        #data['KiasiAnachokopa'] = deni_plus_riba

        serializer = VituoVyoteSerializer(data=data)

        if serializer.is_valid():
            wateja = serializer.save()

            

            

            # Email notification to admin
            myemail = "juniordimoso8@gmail.com"
            subject = "Gegwajo Microfinance"
            message = f"Kitu kimeongezwa na  {request.user.username}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [myemail]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)













#----------------------------GET VITUO VYOTE--------------------------



class GetVituoVyoteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            #today = now().date()
            queryset = VituoVyote.objects.all(
                #JinaLaKituo__icontains=login_user_JinaLaKituo,
                #Nje_Ya_Mkata_Leo=True
                #Created__date=today
            ).order_by('-id')

            # Calculate the total
            #total_wateja = queryset.count() or 0

            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            JumlaYaWote = queryset.count()

            serializer = VituoVyoteSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                'JumlaYaWote': JumlaYaWote,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": [], "JumlaYaWote": 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class DeleteKituoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        #login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Fetch the MarejeshoCopies instance
            kituo = VituoVyote.objects.get(id=pk)

            # Delete the kituoCopies instance
            kituo.delete()

            return Response({'message': 'Ripoti kimefutwa kikamilifu.'}, status=status.HTTP_200_OK)

        except VituoVyote.DoesNotExist:
            return Response({'error': 'kituo hakijapatikana.'}, status=status.HTTP_404_NOT_FOUND)
        except VituoVyote.DoesNotExist:
            return Response({'error': 'kituo hakijapatikana.'}, status=status.HTTP_404_NOT_FOUND)




class GetMyUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            # Filter entries for today
            #today = now().date()
            queryset = MyUser.objects.all(
                #JinaLaKituo__icontains=login_user_JinaLaKituo,
                #Nje_Ya_Mkata_Leo=True
                #Created__date=today
            ).order_by('-id')

            # Calculate the total
            #total_wateja = queryset.count() or 0

            # Use pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            JumlaYaWote = queryset.count()

            serializer = MyUserSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page,
                'JumlaYaWote': JumlaYaWote,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": [], "JumlaYaWote": 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class DeleteMyUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        #login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo
        try:
            # Fetch the MarejeshoCopies instance
            kituo = MyUser.objects.get(id=pk)

            # Delete the kituoCopies instance
            kituo.delete()

            return Response({'message': 'User amefutwa kikamilifu.'}, status=status.HTTP_200_OK)

        except MyUser.DoesNotExist:
            return Response({'error': 'User hajapatikana.'}, status=status.HTTP_404_NOT_FOUND)
        except MyUser.DoesNotExist:
            return Response({'error': 'User hajapatikana.'}, status=status.HTTP_404_NOT_FOUND)













#--------------------------TUMA MSG KWA MTEJA--------------------------------

class TumaMsgKwaMtejaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # EG:http://127.0.0.1:8000/TumaMsgKwaMtejaView/?JinaKamiliLaMteja=Juma&EmailYaMteja=juniordimoso8@gmail.com&SimuYaMteja=234&KiasiAnachokopa=50000&KiasiAlicholipa=10000&RejeshoKwaSiku=2000&JumlaYaDeni=40000&Riba=1000

    

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()

        JinaKamiliLaMteja = request.query_params.get('JinaKamiliLaMteja')
        #EmailYaMteja = request.query_params.get('EmailYaMteja')
        SimuYaMteja = request.query_params.get('SimuYaMteja')

        KiasiAnachokopa = int(request.query_params.get('KiasiAnachokopa'))
        KiasiAlicholipa = int(request.query_params.get('KiasiAlicholipa'))
        RejeshoKwaSiku = int(request.query_params.get('RejeshoKwaSiku'))
        JumlaYaDeni = int(request.query_params.get('JumlaYaDeni'))
        Riba = int(request.query_params.get('Riba'))



        data['JinaKamiliLaMteja'] = JinaKamiliLaMteja
        #data['EmailYaMteja'] = EmailYaMteja
        data['SimuYaMteja'] = SimuYaMteja


        
        Message = data.get('Message', None)
        


        serializer = JumbeZaWatejaSerializer(data=data)

        if serializer.is_valid():
            wateja = serializer.save()

            message = f"Ndugu {JinaKamiliLaMteja}, {Message}. \n Kiasi ulichokopa ni Tsh. {KiasiAnachokopa} \n Kiasi ulicholipa ni Tsh. {KiasiAlicholipa} \n jumla ya deni lililobaki ni Tsh. {JumlaYaDeni}  \n Kwa mawasiliano zaidi piga simu namba 0628431507"
            phone_number = f"255{wateja.SimuYaMteja}"

            sms_response = None
            try:
                sms_response = send_sms_nextsms(phone_number, message)
                if sms_response:
                    print(f"SMS sent successfully to {JinaKamiliLaMteja}.")
                else:
                    print(f"Failed to send SMS to {JinaKamiliLaMteja}.")
            except Exception as e:
                print(f"Error during SMS sending: {e}")

            

            # Email notification to admin
            myemail = "juniordimoso8@gmail.com"
            subject = "Gegwajo Microfinance"
            message = f"Ndugu {JinaKamiliLaMteja}, {Message}. \n Kiasi ulichokopa ni Tsh. {KiasiAnachokopa} \n Kiasi ulicholipa ni Tsh. {KiasiAlicholipa} \n jumla ya deni lililobaki ni Tsh. {JumlaYaDeni}  \n Kwa mawasiliano zaidi piga simu namba 0628431507"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [myemail]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

















class GetTransactionSummaryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            login_user_JinaLaKituo = request.user.JinaLaKituo.JinaLaKituo

            jumla_wateja_wote = WatejaWote.objects.all(
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).count()

            jumla_wateja_wote_kwenye_kituo = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).count()

            jumla_wateja_wote_hai = WatejaWote.objects.filter(
                # JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Ni_Mteja_Hai=True
            ).count()

            jumla_wateja_wote_hai_kwenye_kituo = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Ni_Mteja_Hai=True
            ).count()

            #HIZI ZA CHINI NI KWA WATEJA HAI TU

            jumla_mikopo_iliyotoka = WatejaWote.objects.filter(
                Ni_Mteja_Hai=True
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('KiasiAnachokopa'))['KiasiAnachokopa__sum'] or 0

            jumla_mikopo_iliyotoka_kwenye_kituo = WatejaWote.objects.filter(
                Ni_Mteja_Hai=True,
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('KiasiAnachokopa'))['KiasiAnachokopa__sum'] or 0

            today = now().date()
            yesterday = today - timedelta(days=1)

            jumla_mikopo_iliyotoka_leo = WatejaWote.objects.filter(
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=today
            ).aggregate(Sum('KiasiAnachokopa'))['KiasiAnachokopa__sum'] or 0

            jumla_mikopo_iliyotoka_leo_kwenye_kituo = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=today
            ).aggregate(Sum('KiasiAnachokopa'))['KiasiAnachokopa__sum'] or 0

            jumla_riba_zote = WatejaWote.objects.filter(
                Ni_Mteja_Hai=True
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('Riba'))['Riba__sum'] or 0

            jumla_riba_zote_kwenye_kituo = WatejaWote.objects.filter(
                Ni_Mteja_Hai=True,
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('Riba'))['Riba__sum'] or 0

            jumla_riba_zote_za_leo = WatejaWote.objects.filter(
                Created__date=today
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('Riba'))['Riba__sum'] or 0

            jumla_riba_zote_za_leo_kwenye_kituo = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                Created__date=today
            ).aggregate(Sum('Riba'))['Riba__sum'] or 0


            #-----------------FAINI------------
            jumla_faini_zote_zilizopokelewa = MalipoYaFainiCopies.objects.all(
                #Created__date=today             
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('FainiIliyoPokelewaLeo'))['FainiIliyoPokelewaLeo__sum'] or 0


            jumla_faini_zote_zilizopokelewa_leo = MalipoYaFainiCopies.objects.filter(
                Created__date=today             
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('FainiIliyoPokelewaLeo'))['FainiIliyoPokelewaLeo__sum'] or 0

            jumla_faini_zote_zilizopokelewa_kwenye_kituo = MalipoYaFainiCopies.objects.filter(
                #Created__date=today             
                JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('FainiIliyoPokelewaLeo'))['FainiIliyoPokelewaLeo__sum'] or 0


            jumla_faini_zote_zilizopokelewa_leo_kwenye_kituo = MalipoYaFainiCopies.objects.filter(
                Created__date=today ,            
                JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('FainiIliyoPokelewaLeo'))['FainiIliyoPokelewaLeo__sum'] or 0

            # jumla_management_fee = WatejaWote.objects.filter(
            #     JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            # ).aggregate(Sum('ManagementFee'))['ManagementFee__sum'] or 0

            # jumla_total_interest = WatejaWote.objects.filter(
            #     JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            # ).aggregate(Sum('TotalInterest'))['TotalInterest__sum'] or 0
            jumla_faini_zote_zilizokatwa = MarejeshoCopies.objects.all(
                #Created__date=today             
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('FainiKwaSiku'))['FainiKwaSiku__sum'] or 0


            jumla_faini_zote_zilizokatwa_leo = MarejeshoCopies.objects.filter(
                Created__date=yesterday             
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('FainiKwaSiku'))['FainiKwaSiku__sum'] or 0

            jumla_faini_zote_zilizokatwa_kwenye_kituo = MarejeshoCopies.objects.filter(
                #Created__date=today             
                JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('FainiKwaSiku'))['FainiKwaSiku__sum'] or 0


            jumla_faini_zote_zilizokatwa_leo_kwenye_kituo = MarejeshoCopies.objects.filter(
                Created__date=yesterday ,            
                JinaLaKituo__icontains=login_user_JinaLaKituo
            ).aggregate(Sum('FainiKwaSiku'))['FainiKwaSiku__sum'] or 0
             
             


            jumla_mikopo_isiyolipwa = WatejaWote.objects.filter(
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                JumlaYaDeni__gt=0
            ).aggregate(Sum('JumlaYaDeni'))['JumlaYaDeni__sum'] or 0

            jumla_mikopo_isiyolipwa_kwenye_kituo = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                JumlaYaDeni__gt=0
            ).aggregate(Sum('JumlaYaDeni'))['JumlaYaDeni__sum'] or 0

            idadi_ya_wasiomaliza_mikopo = WatejaWote.objects.filter(
                #JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                JumlaYaDeni__gt=0
            ).count()

            idadi_ya_wasiomaliza_mikopo_kwenye_kituo = WatejaWote.objects.filter(
                JinaLaKituo__JinaLaKituo__icontains=login_user_JinaLaKituo,
                JumlaYaDeni__gt=0
            ).count()

            response_data = {
                'jumla_faini_zote_zilizopokelewa':jumla_faini_zote_zilizopokelewa,
                'jumla_faini_zote_zilizopokelewa_leo':jumla_faini_zote_zilizopokelewa_leo,
                'jumla_faini_zote_zilizopokelewa_kwenye_kituo':jumla_faini_zote_zilizopokelewa_kwenye_kituo,
                'jumla_faini_zote_zilizopokelewa_leo_kwenye_kituo':jumla_faini_zote_zilizopokelewa_leo_kwenye_kituo,

                'jumla_faini_zote_zilizokatwa':jumla_faini_zote_zilizokatwa,
                'jumla_faini_zote_zilizokatwa_leo':jumla_faini_zote_zilizokatwa_leo,
                'jumla_faini_zote_zilizokatwa_kwenye_kituo':jumla_faini_zote_zilizokatwa_kwenye_kituo,
                'jumla_faini_zote_zilizokatwa_leo_kwenye_kituo':jumla_faini_zote_zilizokatwa_leo_kwenye_kituo,


                'jumla_mikopo_iliyotoka': jumla_mikopo_iliyotoka,
                'jumla_mikopo_iliyotoka_kwenye_kituo':jumla_mikopo_iliyotoka_kwenye_kituo,
                'jumla_mikopo_iliyotoka_leo': jumla_mikopo_iliyotoka_leo,
                'jumla_mikopo_iliyotoka_leo_kwenye_kituo':jumla_mikopo_iliyotoka_leo_kwenye_kituo,
                'jumla_wateja_wote': jumla_wateja_wote,
                'jumla_wateja_wote_kwenye_kituo': jumla_wateja_wote_kwenye_kituo,
                'jumla_wateja_wote_hai': jumla_wateja_wote_hai,
                'jumla_wateja_wote_hai_kwenye_kituo':jumla_wateja_wote_hai_kwenye_kituo,
                'jumla_riba_zote': jumla_riba_zote,
                'jumla_riba_zote_kwenye_kituo':jumla_riba_zote_kwenye_kituo,
                'jumla_riba_zote_za_leo':jumla_riba_zote_za_leo,
                'jumla_riba_zote_za_leo_kwenye_kituo':jumla_riba_zote_za_leo_kwenye_kituo,
                # 'jumla_management_fee': jumla_management_fee,
                # 'jumla_total_interest': jumla_total_interest,
                'jumla_mikopo_isiyolipwa': jumla_mikopo_isiyolipwa,
                'jumla_mikopo_isiyolipwa_kwenye_kituo':jumla_mikopo_isiyolipwa_kwenye_kituo,
                'idadi_ya_wasiomaliza_mikopo': idadi_ya_wasiomaliza_mikopo,
                'idadi_ya_wasiomaliza_mikopo_kwenye_kituo':idadi_ya_wasiomaliza_mikopo_kwenye_kituo,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




