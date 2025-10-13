# App/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

from django.core.mail import send_mail
from django.conf import settings

from datetime import datetime, timedelta
from django.utils.timezone import now
from App.models import *


def weekly_vaccine_reminder():
    today = now().date()
    yesterday = today - timedelta(days=1)

    # Get users who haven't returned and have not been processed today
    mteja_hai = WatejaWote2.objects.filter(Ni_Mteja_Hai=True, Amerejesha_Leo=False)

    for mteja in mteja_hai:
        if not MarejeshoCopies.objects.filter(
            JinaKamiliLaMteja=mteja.JinaKamiliLaMteja, 
            Created__date=today,
            #reg_no=mteja.reg_no
        ).exists():
            # Increment JumlaYaFainiZote by 1000
            mteja.JumlaYaFainiZote = (mteja.JumlaYaFainiZote or 0) + 1000
            mteja.save()

            # Copy data to MarejeshoCopies
            MarejeshoCopies.objects.create(
                JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
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
                #reg_no=mteja.reg_no,
                FainiKwaSiku=1000
            )
        print(f"Task running for {mteja.JinaKamiliLaMteja}")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Pass the function object directly
    scheduler.add_job(weekly_vaccine_reminder, 'cron', hour=21, minute=30, replace_existing=True, id='weekly_vaccine_reminder')

    register_events(scheduler)
    scheduler.start()
