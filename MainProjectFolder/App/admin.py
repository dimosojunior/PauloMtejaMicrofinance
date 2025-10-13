from django.contrib import admin
from App.models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin
from django.utils.timezone import now

@admin.register(MyUser)
class MyUserAdmin(ImportExportModelAdmin):
    list_display=('username', 'email', 'phone', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields=('email',)
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('date_joined','last_login',)
    fieldsets=()


    # add_fieldsets=(
    #     (None,{
    #         'classes':('wide'),
    #         'fields':('email', 'username','phone', 'first_name', 'middle_name', 'last_name', 'company_name', 'phone', 'password1', 'password2'),
    #     }),
    # )
    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username', 'phone', 'password1', 'password2'),
        }),
    )

    ordering=('email',)



@admin.register(OTP)
class OTPAdmin(ImportExportModelAdmin):
    list_display = ["id","user","otp", "created_at"]
    list_filter =["created_at"]
    search_fields = ["user"]


@admin.register(VituoVyote)  
class VituoVyoteAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaLaKituo","Mahali","Created", "Updated"]
    list_filter =["Created"]
    search_fields = ["JinaLaKituo"]

@admin.register(AinaZaMarejesho)  
class AinaZaMarejeshoAdmin(ImportExportModelAdmin):
    list_display = ["id","Aina","Created", "Updated"]
    list_filter =["Created"]
    search_fields = ["Aina"]

@admin.register(JumbeZaWateja)  
class JumbeZaWatejaAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaKamiliLaMteja", "SimuYaMteja","Created", "Updated"]
    list_filter =["Created"]
    search_fields = ["JinaKamiliLaMteja"]

@admin.register(WatejaWote)
class WatejaWoteAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaKamiliLaMteja","reg_no","time_left","JinaLaKituo","Aina", "SimuYaMteja","Ni_Mteja_Hai","Nje_Ya_Mkata_Leo","Nje_Ya_Mkata_Wote","Mahali","KiasiAnachokopa","JumlaYaDeni","RejeshoKwaSiku", "Created", "Up_To"]
    list_filter =["Created"]
    search_fields = ["JinaKamiliLaMteja"]

    fields = [
        "JinaKamiliLaMteja", "JinaLaKituo","Aina", "SimuYaMteja", "SimuYaMzaminiWa1", "SimuYaMzaminiWa2", 
        "JinaLaMzaminiWa1", "JinaLaMzaminiWa2", "EmailYaMteja", "Mahali", "MaelezoYaMteja",
        "KiasiAnachokopa", "KiasiAlicholipa", "RejeshoKwaSiku", "JumlaYaDeni", "Riba",
        "AmesajiliwaNa", "Amerejesha_Leo", "PichaYaMteja", "Ni_Mteja_Hai", "Nje_Ya_Mkata_Wote", 
        "Nje_Ya_Mkata_Leo", "Wamemaliza_Hawajakopa_Tena","JumlaYaFainiZote", "Created", "Up_To"
        #"AinaZaMarejesho"
    ]

    def save_model(self, request, obj, form, change):
        if not obj.Created:
            obj.Created = now()  # Set `Created` if not already set
        obj.save()

@admin.register(WatejaWoteCart)
class WatejaWoteCartAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaKamiliLaMteja","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["JinaKamiliLaMteja"]

@admin.register(WatejaWoteCartItems)
class WatejaWoteCartItemsAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaKamiliLaMteja","cart", "Mteja","KiasiChaRejeshoChaSiku", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["JinaKamiliLaMteja"]


@admin.register(MarejeshoCopies)
class MarejeshoCopiesAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaKamiliLaMteja","JinaLaKituo","SimuYaMteja","EmailYaMteja","Mahali","KiasiAnachokopa","JumlaYaDeni","RejeshoKwaSiku", "Created"]
    list_filter =["Created"]
    search_fields = ["JinaKamiliLaMteja"]

    fields = [
        "JinaKamiliLaMteja", "JinaLaKituo", "SimuYaMteja", "reg_no", 
        "EmailYaMteja", "Mahali",
        "KiasiAnachokopa", "KiasiAlicholipa", "RejeshoKwaSiku", "JumlaYaDeni", "Riba",
        "AmesajiliwaNa", "RejeshoLililoPokelewaLeo", "PichaYaMteja", "Ni_Mteja_Hai", "Up_To", 
        "FainiKwaSiku", "Created"
    ]

    def save_model(self, request, obj, form, change):
        if not obj.Created:
            obj.Created = now()  # Set `Created` if not already set
        obj.save()


@admin.register(MarejeshoCopiesTwo)
class MarejeshoCopiesTwoAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaKamiliLaMteja","JinaLaKituo","SimuYaMteja","EmailYaMteja","Mahali","KiasiAnachokopa","JumlaYaDeni","RejeshoKwaSiku", "Created"]
    list_filter =["Created"]
    search_fields = ["JinaKamiliLaMteja"]

    fields = [
        "JinaKamiliLaMteja", "JinaLaKituo", "SimuYaMteja", "reg_no", 
        "EmailYaMteja", "Mahali",
        "KiasiAnachokopa", "KiasiAlicholipa", "RejeshoKwaSiku", "JumlaYaDeni", "Riba",
        "AmesajiliwaNa", "RejeshoLililoPokelewaLeo", "PichaYaMteja", "Ni_Mteja_Hai", "Up_To", 
        "FainiKwaSiku", "Created"
    ]

    def save_model(self, request, obj, form, change):
        if not obj.Created:
            obj.Created = now()  # Set `Created` if not already set
        obj.save()

@admin.register(NjeYaMkatabaCopies)
class NjeYaMkatabaCopiesAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaKamiliLaMteja","JinaLaKituo","SimuYaMteja","EmailYaMteja","Mahali","KiasiAnachokopa","JumlaYaDeni","RejeshoKwaSiku", "Created"]
    list_filter =["Created"]
    search_fields = ["JinaKamiliLaMteja"]

    fields = [
        "JinaKamiliLaMteja", "JinaLaKituo", "SimuYaMteja", "reg_no", 
        "EmailYaMteja", "Mahali",
        "KiasiAnachokopa", "KiasiAlicholipa", "RejeshoKwaSiku", "JumlaYaDeni", "Riba",
        "AmesajiliwaNa", "RejeshoLililoPokelewaLeo", "PichaYaMteja", "Ni_Mteja_Hai", "Up_To", 
        "FainiKwaSiku", "Created"
    ]

    def save_model(self, request, obj, form, change):
        if not obj.Created:
            obj.Created = now()  # Set `Created` if not already set
        obj.save()


@admin.register(MalipoYaFainiCopies)
class MalipoYaFainiCopiesAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaKamiliLaMteja","JinaLaKituo","SimuYaMteja","EmailYaMteja","Mahali","KiasiAnachokopa","JumlaYaDeni","RejeshoKwaSiku", "Created"]
    list_filter =["Created"]
    search_fields = ["JinaKamiliLaMteja"]

    fields = [
        "JinaKamiliLaMteja", "JinaLaKituo", "SimuYaMteja", "reg_no", 
        "EmailYaMteja", "Mahali",
        "KiasiAnachokopa", "KiasiAlicholipa", "RejeshoKwaSiku", "JumlaYaDeni", "Riba",
        "AmesajiliwaNa", "FainiIliyoPokelewaLeo", "PichaYaMteja", "Ni_Mteja_Hai", "Up_To", 
        "FainiKwaSiku", "Created"
    ]

    def save_model(self, request, obj, form, change):
        if not obj.Created:
            obj.Created = now()  # Set `Created` if not already set
        obj.save()


@admin.register(Ripoti)
class RipotiAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "Created",
        "JinaLaKituo",
        "JumlaMarejeshoYaLeo",
        "JumlaFainiLeo",
        "FomuNaBima",
        "BakiJana",
        "ImetokaKwaBosi",
        "ImetokaKituoJirani", 
        "MapatoYaJumla",
        "Mkopo",
        "Posho",
        "ImeendaKwaBosi",
        "ImeendaKituoJirani",
        "MatumiziMengine",
        "MatumiziYaJumla",
        "IdadiYaMikopoYaLeo",
        "IdadiYaMikatabaMipyaLeo",
        "IdadiYaWenyeMikatabaHai",
        "IdadiYaWaliorejeshaLeo",
        "IdadiYaFainiZilizopokelewaLeo",
        "ImeweingizwaNa",
        "Balance"
    ]
    list_filter =["Created"]
    search_fields = ["Created"]

    fields = [
        #"id",
        "JinaLaKituo",
        "Created",
        "JumlaMarejeshoYaLeo",
        "JumlaFainiLeo",
        "FomuNaBima",
        "BakiJana",
        "ImetokaKwaBosi",
        "ImetokaKituoJirani", 
        "KituoIlichotokaHela",
        "MapatoYaJumla",
        "Mkopo",
        "Posho",
        "ImeendaKwaBosi",
        "ImeendaKituoJirani",
        "KituoIlichoendaHela",
        "MatumiziMengine",
        "MatumiziYaJumla",
        "IdadiYaMikopoYaLeo",
        "IdadiYaMikatabaMipyaLeo",
        "IdadiYaWenyeMikatabaHai",
        "IdadiYaWaliorejeshaLeo",
        "IdadiYaFainiZilizopokelewaLeo",
        "ImeweingizwaNa",
        "Balance"
    ]

    def save_model(self, request, obj, form, change):
        if not obj.Created:
            obj.Created = now()  # Set `Created` if not already set
        obj.save()

# admin.site.register(WatejaWoteCart, WatejaWoteCartAdmin)
# admin.site.register(WatejaWoteCartItems, WatejaWoteCartItemsAdmin)

