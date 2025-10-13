from App.models import *
from django.utils.timezone import now
from datetime import timedelta


class Command(BaseCommand):
    help = 'Check conditions for WatejaWote2 and send emails.'

    def handle(self, *args, **kwargs):
        wateja_list = WatejaWote2.objects.all()

        for mteja in wateja_list:
            time_elapsed =  mteja.time_left

            if time_elapsed == 4 and mteja.Ni_Mteja_Hai:
                mteja.Ni_Mteja_Hai = False
                mteja.save(update_fields=['Ni_Mteja_Hai'])
                self.send_email(mteja, "Ni Mteja Hai condition reached.")

            if time_elapsed == 3 and not mteja.Nje_Ya_Mkata_Leo:
                mteja.Nje_Ya_Mkata_Leo = True
                mteja.save(update_fields=['Nje_Ya_Mkata_Leo'])
                self.send_email(mteja, "Nje Ya Mkata Leo condition reached.")
                self.copy_to_nje_ya_mkataba_copies(mteja)

            if time_elapsed == 3 and mteja.Nje_Ya_Mkata_Leo:
                mteja.Nje_Ya_Mkata_Leo = False
                mteja.save(update_fields=['Nje_Ya_Mkata_Leo'])
                self.send_email(mteja, "Umetoka nje ya mkataba wa siku 30")

            if time_elapsed == 4 and not mteja.Nje_Ya_Mkata_Wote:
                mteja.Nje_Ya_Mkata_Wote = True
                mteja.save(update_fields=['Nje_Ya_Mkata_Wote'])
                self.send_email(mteja, "Nje Ya Mkata Wote condition reached.")

    def send_email(self, mteja, condition_message):
        subject = "Notification: Condition Met"
        message = f"Mteja: {mteja.JinaKamiliLaMteja}\nCondition: {condition_message}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [mteja.EmailYaMteja]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

    def copy_to_nje_ya_mkataba_copies(self, mteja):
        # Copy relevant information to NjeYaMkatabaCopies
        NjeYaMkatabaCopies.objects.create(
            #reg_no=mteja.reg_no,
            JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
            #JinaLaKituo=mteja.JinaLaKituo.JinaLaKituo if mteja.JinaLaKituo else None,
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
            #Created=mteja.Created,
            Updated=mteja.Updated,
            Up_To=mteja.Up_To,
        )
