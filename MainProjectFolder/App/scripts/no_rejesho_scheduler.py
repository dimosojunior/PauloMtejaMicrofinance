from App.models import WatejaWote, MarejeshoCopiesTwo
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
import base64
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def run():
    try:
        today = now().date()
        wateja_list = WatejaWote.objects.all(
            #JumlaYaDeni__gt=0
        )
        deni_plus_faini = 0
        tarehe_ya_kulipa_tena_nje_ya_mkataba_wote = 0
        tarehe_ya_leo = 0
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

            # 30-day condition
            if time_elapsed == 30 and not mteja.Nje_Ya_Mkata_Leo and mteja.JumlaYaDeni > 0:
                condition_checked["30_days_left"] += 1
                mteja.Nje_Ya_Mkata_Leo = True
                mteja.save(update_fields=['Nje_Ya_Mkata_Leo'])
                copy_to_nje_ya_mkataba_copies(mteja)

                message = f"Ndugu mteja {mteja.JinaKamiliLaMteja} mkataba wako unaisha leo, deni lako limebaki Tsh {deni_plus_faini}/=\n Fika ofisini kumaliza deni lako kabla mfumo haujakubadilishia mkataba mpya. \n Mawasiliano: 0621690739 / 0747462389 "
                send_email(mteja, message)

                phone_number = f"255{mteja.SimuYaMteja}"
                sms_response = send_sms(phone_number, message)
                if not sms_response:
                    print(f"Failed to send SMS to {mteja.SimuYaMteja} time_left 30")

            # 31-day condition
            if time_elapsed == 31 and not mteja.Nje_Ya_Mkata_Wote and mteja.JumlaYaDeni > 0:
                condition_checked["31_days_left"] += 1
                mteja.Nje_Ya_Mkata_Wote = True
                mteja.save(update_fields=['Nje_Ya_Mkata_Wote'])

            # 40-day condition
            if time_elapsed == 40 and mteja.Nje_Ya_Mkata_Wote and mteja.JumlaYaDeni > 0:
                condition_checked["40_days_left"] += 1
                MarejeshoCopiesTwo.objects.filter(
                    JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
                    reg_no=mteja.reg_no
                ).delete()
                # Reset values and reinitialize mteja
                mteja.Nje_Ya_Mkata_Wote = False
                mteja.Nje_Ya_Mkata_Leo = False
                mteja.Ni_Mteja_Hai = True
                mteja.Amerejesha_Leo = False
                mteja.Wamemaliza_Hawajakopa_Tena = False
                deni_alilomaliza_nalo = (mteja.JumlaYaDeni or 0) + (mteja.JumlaYaFainiZote or 0)
                kiasi_anachokopa = int(deni_alilomaliza_nalo)
                riba_mpya = int((kiasi_anachokopa * 20) / 100)
                deni_plus_riba = kiasi_anachokopa + riba_mpya
                rejesho_kwa_siku = round((deni_plus_riba) / 30, 0)

                mteja.KiasiAnachokopa = deni_plus_riba
                mteja.Riba = riba_mpya
                mteja.JumlaYaDeni = deni_plus_riba
                mteja.KiasiAlicholipa = 0
                mteja.RejeshoKwaSiku = rejesho_kwa_siku
                mteja.JumlaYaFainiZote = 0

                tarehe_ya_leo = now()
                tarehe_ya_kumaliza = tarehe_ya_leo + timedelta(days=30)

                mteja.Created = tarehe_ya_leo

                mteja.Up_To = tarehe_ya_kumaliza

                mteja.save(update_fields=[
                    'Nje_Ya_Mkata_Wote', 'Nje_Ya_Mkata_Leo', 'Ni_Mteja_Hai',
                    'Amerejesha_Leo', 'KiasiAnachokopa', 'Riba', 'JumlaYaDeni',
                    'KiasiAlicholipa', 'RejeshoKwaSiku', 'JumlaYaFainiZote',
                    'Created', 'Up_To'
                ])


                message = f"Ndugu mteja {mteja.JinaKamiliLaMteja} mkataba wako umejibadilisha leo. Deni lako jipya ni Tsh {deni_plus_riba}/=, rejesha mpaka tarehe {tarehe_ya_kumaliza}. \n Hatua zitachukuliwa ikiwa hutomaliza. \n Mawasiliano: 0621690739 / 0747462389"
                send_email(mteja, message)

                phone_number = f"255{mteja.SimuYaMteja}"
                sms_response = send_sms(phone_number, message)
                if not sms_response:
                    print(f"Failed to send SMS to {mteja.SimuYaMteja} time_left 41")


        print(f"Total wateja checked: {total_checked}")
        for condition, count in condition_checked.items():
            print(f"Condition '{condition}': {count} wateja checked.")

    except Exception as e:
        print(f"Error during task execution: {e}")








def send_sms(phone_number, message):
    url = os.getenv("BEEM_ACCOUNT_URL")
    api_key = os.getenv("BEEM_ACCOUNT_API_KEY")
    secret_key = os.getenv("BEEM_ACCOUNT_SECRET_KEY")
    sender_id = os.getenv("BEEM_ACCOUNT_SENDER_ID")

    auth_string = f"{api_key}:{secret_key}"
    auth_base64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

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
        print(f"Error sending SMS: {e}")
        return None

def send_email(mteja, message):
    try:
        send_mail(
            subject="Notification",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[mteja.EmailYaMteja]
        )
    except Exception as e:
        print(f"Error sending email to {mteja.EmailYaMteja}: {e}")

def copy_to_nje_ya_mkataba_copies(mteja):
    try:
        # Add your logic to copy mteja details
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
        print(f"Mteja {mteja.JinaKamiliLaMteja} copied to 'nje ya mkataba' copies.")
    except Exception as e:
        print(f"Error copying mteja {mteja.JinaKamiliLaMteja}: {e}")
