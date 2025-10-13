from App.models import *
from django.core.mail import send_mail
from django.conf import settings

from datetime import datetime, timedelta
from django.utils.timezone import now



import requests
from requests.auth import HTTPBasicAuth  
import requests
from django.http import JsonResponse

from dotenv import load_dotenv
import os

import requests

import base64
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables
load_dotenv()




# def send_sms(phone_number, message):
#     """
#     Sends an SMS using Beem Africa API.
    
#     :param phone_number: The recipient's phone number in international format (e.g., +255XXXXXXXXX)
#     :param message: The message to send
#     """
#     url = os.getenv("BEEM_ACCOUNT_URL")
#     api_key = os.getenv("BEEM_ACCOUNT_API_KEY")  # Replace with your Beem Africa API key
#     secret_key = os.getenv("BEEM_ACCOUNT_SECRET_KEY")  # Replace with your Beem Africa secret key
#     sender_id = os.getenv("BEEM_ACCOUNT_SENDER_ID")  # Replace with your approved Sender Name

#     # Encode API key and secret key in base64
#     auth_string = f"{api_key}:{secret_key}"
#     auth_bytes = auth_string.encode("utf-8")
#     auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Basic {auth_base64}"
#     }
    
#     payload = {
#         "source_addr": sender_id,
#         "encoding": 0,
#         "schedule_time": "",
#         "recipients": [{"recipient_id": 1, "dest_addr": phone_number}],
#         "message": message
#     }

#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         response.raise_for_status()  # Raise an error for HTTP codes 4XX/5XX
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error sending SMS: {e}")
#         return None




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


def run():
    try:
        today = now().date()
        wateja_list = WatejaWote.objects.filter(JumlaYaDeni__gt=0)
        deni_plus_faini = 0
        tarehe_ya_kulipa_tena_nje_ya_mkataba_wote = 0
        tarehe_ya_leo = 0
        kuanza_kesho = 0
        tarehe_ya_kumaliza=0

        deni_alilomaliza_nalo = 0

        kiasi_anachokopa = 0

        riba_mpya = 0
        deni_plus_riba = 0
        rejesho_kwa_siku = 0

        total_checked = 0
        condition_checked = {
            "30_days_left": 0,
            "31_days_left": 0,
            "40_days_left": 0
        }
        


        for mteja in wateja_list:
            total_checked += 1
            time_elapsed = mteja.time_left or 0
            deni_plus_faini = (mteja.JumlaYaDeni or 0) + (mteja.JumlaYaFainiZote or 0)

            # if time_elapsed == 31 and mteja.Ni_Mteja_Hai and mteja.JumlaYaDeni <= 0:
            #     mteja.Ni_Mteja_Hai = False
            #     mteja.save(update_fields=['Ni_Mteja_Hai'])
                #send_email(mteja, "Ni Mteja Hai condition reached.")

            if time_elapsed == 30 and not mteja.Nje_Ya_Mkata_Leo and mteja.JumlaYaDeni > 0:
                condition_checked["30_days_left"] += 1
                mteja.Nje_Ya_Mkata_Leo = True
                mteja.save(update_fields=['Nje_Ya_Mkata_Leo'])
                send_email(mteja, f"Ndugu mteja {mteja.JinaKamiliLaMteja} mkataba wako unaisha leo, deni lako limebaki Tsh {deni_plus_faini}/=\n Fika ofisini kumaliza deni lako kabla mfumo haujakubadilishia mkataba mpya. \n Mawasiliano: 0621690739 / 0747462389 ")
                copy_to_nje_ya_mkataba_copies(mteja)

                # Sending SMS after registration
                

                message = f"Ndugu mteja {mteja.JinaKamiliLaMteja} mkataba wako unaisha leo, deni lako limebaki Tsh {deni_plus_faini}/=\n Fika ofisini kumaliza deni lako kabla mfumo haujakubadilishia mkataba mpya. \n Mawasiliano: 0621690739 / 0747462389"
                phone_number = f"255{mteja.SimuYaMteja}"

                sms_response = None
                try:
                    sms_response = send_sms_nextsms(phone_number, message)
                    if sms_response:
                        print(f"SMS sent successfully to {mteja.JinaKamiliLaMteja}.")
                    else:
                        print(f"Failed to send SMS to {mteja.JinaKamiliLaMteja}.")
                except Exception as e:
                    print(f"Error during SMS sending: {e}")

                #Mwisho wa kutuma sms

            if time_elapsed == 31 and mteja.Nje_Ya_Mkata_Leo:
                mteja.Nje_Ya_Mkata_Leo = False
                mteja.save(update_fields=['Nje_Ya_Mkata_Leo'])
                #send_email(mteja, "Umetoka nje ya mkataba wa siku 30.")

            #hii ni kwaajili ya kumchange mteja kuwa true kwenye mkatababa wote
            if time_elapsed == 31 and not mteja.Nje_Ya_Mkata_Wote and mteja.JumlaYaDeni > 0:
                condition_checked["31_days_left"] += 1
                mteja.Nje_Ya_Mkata_Wote = True
                mteja.save(update_fields=['Nje_Ya_Mkata_Wote'])
                #send_email(mteja, f"Ndugu mteja {mteja.JinaKamiliLaMteja} mkataba wako umejibadilisha leo. Deni lako jipya ni Tsh {deni_plus_faini}/=, rejesha mpaka tarehe {tarehe_ya_kulipa_tena_nje_ya_mktaba_wote}. \n Hatua zitachukuliwa ikiwa hutomaliza. \n Mawasiliano: 0621690739 / 0747462389")
            

            if time_elapsed == 40 and mteja.Nje_Ya_Mkata_Wote and mteja.JumlaYaDeni > 0:
                condition_checked["40_days_left"] += 1

                # Delete matching entries from MarejeshoCopiesTwo ili marejesho yake yaanze
                #kusoma upya
                MarejeshoCopiesTwo.objects.filter(
                    JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
                    reg_no=mteja.reg_no
                ).delete()

                
                mteja.Nje_Ya_Mkata_Wote = False
                mteja.Nje_Ya_Mkata_Leo = False
                mteja.Ni_Mteja_Hai = True
                mteja.Amerejesha_Leo = False
                mteja.Wamemaliza_Hawajakopa_Tena = False

                deni_alilomaliza_nalo = (mteja.JumlaYaDeni or 0) + (mteja.JumlaYaFainiZote or 0)

                kiasi_anachokopa = int(deni_alilomaliza_nalo)

                #Filter kulingana na category za wateja
                if mteja.Aina and mteja.Aina.Aina == "Muajiriwa":
                    riba_mpya = int((kiasi_anachokopa * 30) / 100)
                    deni_plus_riba = kiasi_anachokopa + riba_mpya
                    rejesho_kwa_siku = 0

                elif mteja.Aina and mteja.Aina.Aina == "Mfanya Kazi Wa Kituo":
                    riba_mpya = int((kiasi_anachokopa * 10) / 100)
                    deni_plus_riba = kiasi_anachokopa + riba_mpya
                    rejesho_kwa_siku = 0

                else:
                    riba_mpya = int((kiasi_anachokopa * 20) / 100)
                    deni_plus_riba = kiasi_anachokopa + riba_mpya
                    rejesho_kwa_siku = round((deni_plus_riba) / 30, 0)





                tarehe_ya_leo = now()
                #hakikisha mteja anaanza kulipa kesho
                kuanza_kesho = tarehe_ya_leo +  timedelta(days=1)
                tarehe_ya_kumaliza = kuanza_kesho + timedelta(days=30)

                mteja.KiasiAnachokopa = deni_plus_riba
                mteja.Riba = riba_mpya
                mteja.JumlaYaDeni = deni_plus_riba
                mteja.KiasiAlicholipa = 0
                mteja.RejeshoKwaSiku = rejesho_kwa_siku
                mteja.JumlaYaFainiZote=0




                mteja.Created = kuanza_kesho

                mteja.Up_To = tarehe_ya_kumaliza

                

                #calculation

                mteja.save(update_fields=[
                    'Nje_Ya_Mkata_Wote',
                    'Nje_Ya_Mkata_Leo',
                    'Ni_Mteja_Hai',
                    'Amerejesha_Leo',
                    'KiasiAnachokopa',
                    'Riba',
                    'JumlaYaDeni',
                    'KiasiAlicholipa',
                    'RejeshoKwaSiku',
                    'JumlaYaFainiZote',
                    'Wamemaliza_Hawajakopa_Tena',

                    'Created',
                    'Up_To'
                ])
                #send_email(mteja, f"Ndugu mteja {mteja.JinaKamiliLaMteja} mkataba wako umejibadilisha leo. Deni lako jipya ni Tsh {deni_plus_riba}/=, rejesha mpaka tarehe {tarehe_ya_kumaliza}. \n Hatua zitachukuliwa ikiwa hutomaliza. \n Mawasiliano: 0621690739 / 0747462389")


                # Sending SMS after registration
                # message = f"Ndugu mteja {mteja.JinaKamiliLaMteja} mkataba wako umejibadilisha leo. Deni lako jipya ni Tsh {deni_plus_riba}/=, rejesha mpaka tarehe {tarehe_ya_kumaliza}. \n Hatua zitachukuliwa ikiwa hutomaliza. \n Mawasiliano: 0621690739 / 0747462389"
                
                # phone_number = f"255{mteja.SimuYaMteja}"

                # sms_response = None
                # try:
                #     sms_response = send_sms_nextsms(phone_number, message)
                #     if sms_response:
                #         print(f"SMS sent successfully to {mteja.JinaKamiliLaMteja}.")
                #     else:
                #         print(f"Failed to send SMS to {mteja.JinaKamiliLaMteja}.")
                # except Exception as e:
                #     print(f"Error during SMS sending: {e}")
                

                #Mwisho wa kutuma sms
            

        # print(f"Total wateja checked: {total_checked}")
        # for condition, count in condition_checked.items():
        #     print(f"Condition '{condition}': {count} wateja checked.")

            print(f"Executed: {mteja.JinaKamiliLaMteja}")

    except Exception as e:
        print(f"Error occurred for {mteja.JinaKamiliLaMteja}: {str(e)}")
        #print(f"Error occurred: {str(e)}")

def send_email(mteja, condition_message):
    subject = "Notification: Condition Met"
    message = f"Jina La Mteja: {mteja.JinaKamiliLaMteja}\n Ujumbe: {condition_message}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [mteja.EmailYaMteja]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

def copy_to_nje_ya_mkataba_copies(mteja):
    NjeYaMkatabaCopies.objects.create(
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
        Updated=mteja.Updated,
        reg_no=mteja.reg_no,
        Up_To=mteja.Up_To,
    )







# from App.models import *
# from django.core.mail import send_mail
# from django.conf import settings

# from datetime import datetime, timedelta
# from django.utils.timezone import now

# def run():
#     try:
#         today = now().date()
#         wateja_list = WatejaWote.objects.all()
#         deni_plus_faini = 0
#         tarehe_ya_kulipa_tena_nje_ya_mkataba_wote = 0
#         tarehe_ya_leo = 0
#         tarehe_ya_kumaliza=0

#         deni_alilomaliza_nalo = 0

#         kiasi_anachokopa = 0

#         riba_mpya = 0
#         deni_plus_riba = 0
#         rejesho_kwa_siku = 0
        


#         for mteja in wateja_list:
#             time_elapsed = mteja.time_left
#             deni_plus_faini = mteja.JumlaYaDeni + mteja.JumlaYaFainiZote

#             # if time_elapsed == 31 and mteja.Ni_Mteja_Hai and mteja.JumlaYaDeni <= 0:
#             #     mteja.Ni_Mteja_Hai = False
#             #     mteja.save(update_fields=['Ni_Mteja_Hai'])
#                 #send_email(mteja, "Ni Mteja Hai condition reached.")

#             if time_elapsed == 30 and not mteja.Nje_Ya_Mkata_Leo and mteja.JumlaYaDeni > 0:
#                 mteja.Nje_Ya_Mkata_Leo = True
#                 mteja.save(update_fields=['Nje_Ya_Mkata_Leo'])
#                 send_email(mteja, f"Ndugu mteja {mteja.JinaKamiliLaMteja} mkataba wako unaisha leo, deni lako limebaki Tsh {deni_plus_faini}/=\n Fika ofisini kumaliza deni lako kabla mfumo haujakubadilishia mkataba mpya. \n Mawasiliano: 0621690739 / 0747462389 ")
#                 copy_to_nje_ya_mkataba_copies(mteja)

#             if time_elapsed == 31 and mteja.Nje_Ya_Mkata_Leo:
#                 mteja.Nje_Ya_Mkata_Leo = False
#                 mteja.save(update_fields=['Nje_Ya_Mkata_Leo'])
#                 #send_email(mteja, "Umetoka nje ya mkataba wa siku 30.")

#             #hii ni kwaajili ya kumchange mteja kuwa true kwenye mkatababa wote
#             if time_elapsed == 31 and not mteja.Nje_Ya_Mkata_Wote and mteja.JumlaYaDeni > 0:
#                 mteja.Nje_Ya_Mkata_Wote = True
#                 mteja.save(update_fields=['Nje_Ya_Mkata_Wote'])
#                 #send_email(mteja, f"Ndugu mteja {mteja.JinaKamiliLaMteja} mkataba wako umejibadilisha leo. Deni lako jipya ni Tsh {deni_plus_faini}/=, rejesha mpaka tarehe {tarehe_ya_kulipa_tena_nje_ya_mktaba_wote}. \n Hatua zitachukuliwa ikiwa hutomaliza. \n Mawasiliano: 0621690739 / 0747462389")
            

#             if time_elapsed == 40 and mteja.Nje_Ya_Mkata_Wote and mteja.JumlaYaDeni > 0:

#                 # Delete matching entries from MarejeshoCopies
#                 MarejeshoCopiesTwo.objects.filter(
#                     JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
#                     reg_no=mteja.reg_no
#                 ).delete()

                
#                 mteja.Nje_Ya_Mkata_Wote = False
#                 mteja.Nje_Ya_Mkata_Leo = False
#                 mteja.Ni_Mteja_Hai = True
#                 mteja.Amerejesha_Leo = False
#                 mteja.Wamemaliza_Hawajakopa_Tena = False

#                 deni_alilomaliza_nalo = mteja.JumlaYaDeni + mteja.JumlaYaFainiZote

#                 kiasi_anachokopa = int(deni_alilomaliza_nalo)

#                 riba_mpya = int((kiasi_anachokopa * 20) / 100)
#                 deni_plus_riba = kiasi_anachokopa + riba_mpya
#                 rejesho_kwa_siku = round((deni_plus_riba) / 30, 0)
#                 tarehe_ya_leo = now()
#                 tarehe_ya_kumaliza = tarehe_ya_leo + timedelta(days=30)

#                 mteja.KiasiAnachokopa = deni_plus_riba
#                 mteja.Riba = riba_mpya
#                 mteja.JumlaYaDeni = deni_plus_riba
#                 mteja.KiasiAlicholipa = 0
#                 mteja.RejeshoKwaSiku = rejesho_kwa_siku
#                 mteja.JumlaYaFainiZote=0




#                 mteja.Created = tarehe_ya_leo

#                 mteja.Up_To = tarehe_ya_kumaliza

                

#                 #calculation

#                 mteja.save(update_fields=[
#                     'Nje_Ya_Mkata_Wote',
#                     'Nje_Ya_Mkata_Leo',
#                     'Ni_Mteja_Hai',
#                     'Amerejesha_Leo',
#                     'KiasiAnachokopa',
#                     'Riba',
#                     'JumlaYaDeni',
#                     'KiasiAlicholipa',
#                     'RejeshoKwaSiku',
#                     'JumlaYaFainiZote',
#                     'Wamemaliza_Hawajakopa_Tena',

#                     'Created',
#                     'Up_To'
#                 ])
#                 send_email(mteja, f"Ndugu mteja {mteja.JinaKamiliLaMteja} mkataba wako umejibadilisha leo. Deni lako jipya ni Tsh {deni_plus_riba}/=, rejesha mpaka tarehe {tarehe_ya_kumaliza}. \n Hatua zitachukuliwa ikiwa hutomaliza. \n Mawasiliano: 0621690739 / 0747462389")
#             print(f"Executed: {mteja.JinaKamiliLaMteja}")

#     except Exception as e:
#         print(f"Error occurred: {str(e)}")

# def send_email(mteja, condition_message):
#     subject = "Notification: Condition Met"
#     message = f"Jina La Mteja: {mteja.JinaKamiliLaMteja}\n Ujumbe: {condition_message}"
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [mteja.EmailYaMteja]
#     send_mail(subject, message, from_email, recipient_list, fail_silently=True)

# def copy_to_nje_ya_mkataba_copies(mteja):
#     NjeYaMkatabaCopies.objects.create(
#         JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
#         JinaLaKituo=mteja.JinaLaKituo.JinaLaKituo,
#         SimuYaMteja=mteja.SimuYaMteja,
#         EmailYaMteja=mteja.EmailYaMteja,
#         Mahali=mteja.Mahali,
#         KiasiAnachokopa=mteja.KiasiAnachokopa,
#         KiasiAlicholipa=mteja.KiasiAlicholipa,
#         RejeshoKwaSiku=mteja.RejeshoKwaSiku,
#         JumlaYaDeni=mteja.JumlaYaDeni,
#         Riba=mteja.Riba,
#         AmesajiliwaNa=mteja.AmesajiliwaNa,
#         PichaYaMteja=mteja.PichaYaMteja,
#         Ni_Mteja_Hai=mteja.Ni_Mteja_Hai,
#         Updated=mteja.Updated,
#         reg_no=mteja.reg_no,
#         Up_To=mteja.Up_To,
#     )

