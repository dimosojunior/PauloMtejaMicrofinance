# no_rejesho_scheduler.py
from App.models import *
from datetime import timedelta
from django.utils.timezone import now

def check_and_update_rejesho():
    today = now().date()
    yesterday = today - timedelta(days=1)

    mteja_hai = WatejaWote2.objects.filter(Ni_Mteja_Hai=True, Amerejesha_Leo=False)

    for mteja in mteja_hai:
        if not MarejeshoCopies.objects.filter(
            JinaKamiliLaMteja=mteja.JinaKamiliLaMteja,
            Created__date=today,
        ).exists():
            mteja.JumlaYaFainiZote = (mteja.JumlaYaFainiZote or 0) + 1000
            mteja.save()

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
                FainiKwaSiku=1000
            )
        print(f"Task running for {mteja.JinaKamiliLaMteja}")

if __name__ == "__main__":
    check_and_update_rejesho()
