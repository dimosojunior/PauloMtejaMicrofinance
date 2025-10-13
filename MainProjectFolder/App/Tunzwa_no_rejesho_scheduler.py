from datetime import datetime, timedelta
from django.utils.timezone import now
from App.models import *

def check_and_update_rejesho():
    # Current date and time
    current_time = now()

    # Time range for the day
    start_of_day = current_time.replace(hour=6, minute=0, second=0, microsecond=0)  # 6:00 AM
    end_of_day = current_time.replace(hour=18, minute=0, second=0, microsecond=0)  # 6:00 PM

    # Query for Mteja records where Ni_Mteja_Hai is True
    mteja_hai = WatejaWote2.objects.filter(Ni_Mteja_Hai=True)

    for mteja in mteja_hai:
        # Check if the updated time is outside today's range
        if mteja.Amerejesha_Leo == False:
            # Increment JumlaYaFainiZote by 1000
            mteja.JumlaYaFainiZote = (mteja.JumlaYaFainiZote or 0) + 1000
            mteja.save()

            # Copy Mteja's information to MarejeshoCopies
            MarejeshoCopies.objects.create(
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
                Up_To=mteja.Up_To,
                #reg_no=mteja.reg_no,
                FainiKwaSiku=1000  # Assign fine of 1000 for this instance
            )
