from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
#from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser
import random
from datetime import timedelta
from django.utils.timezone import now #, timedelta
# Create your models here.

def generated_reg_no():
    last_reg_no = WatejaWote.objects.all().order_by('id').last()
    if not last_reg_no:
        return '1'
    reg_no = last_reg_no.reg_no
    new_reg_no = int(reg_no) + 1
    return new_reg_no


def generated_user_reg_no():
    last_reg_no = MyUser.objects.all().order_by('id').last()
    if not last_reg_no:
        return '1'
    reg_no = last_reg_no.reg_no
    new_reg_no = int(reg_no) + 1
    return new_reg_no

class VituoVyote(models.Model):
    
    JinaLaKituo = models.CharField(verbose_name="Jina La Kituo",max_length=100, blank=True,null=True)
    Mahali = models.CharField(verbose_name="Mahali Kilipo",max_length=500, blank=True,null=True) 
    #Chakula = models.ForeignKey('Vyakula', verbose_name="Aina Ya Chakula",on_delete=models.PROTECT, blank=True,null=True)
    #price = models.FloatField(verbose_name="Bei Ya Chakula", blank=True,null=True) 
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.JinaLaKituo}"
    
    class Meta:
        verbose_name_plural = "Vituo Vyote"



class AinaZaMarejesho(models.Model):
    
    Aina = models.CharField(verbose_name="Aina Ya Mpokeaji",max_length=500, blank=True,null=True)
    
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.Aina}"
    
    class Meta:
        verbose_name_plural = "Aina Za Marejesho"




class MyUserManager(BaseUserManager):
    def create_user(self, email, username,phone,Location, is_admin,is_staff,is_cashier,JinaLaKituo=None, password=None):
        # if not email:
        #     raise ValueError("email is required")
        if not username:
            raise ValueError("Your user name is required")

        


        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            is_admin=is_admin,
            is_staff=is_staff,
            is_cashier=is_cashier,
            JinaLaKituo=JinaLaKituo,
            Location=Location,
            
            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            phone="0000000",  # default phone for superuser
            Location="N/A",      # default location
            is_admin=True,
            is_staff=True,
            is_cashier=True,
            JinaLaKituo=None,
            password=password
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

    

  
class MyUser(AbstractBaseUser):
    #reg_no= models.CharField(max_length=100000, default=generated_user_reg_no, unique=True, editable=False,blank=True,null=True)
    email=models.EmailField(blank=True, null=True, verbose_name="email", max_length=100, unique=False)
    #first_name=models.CharField(verbose_name="first name", max_length=100, unique=False)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    #middle_name=models.CharField(verbose_name="middle name", max_length=100, unique=False)
    #last_name=models.CharField(verbose_name="last name", max_length=100, unique=False)
    company_name=models.CharField(verbose_name="company name",default="Gegwajo Microfinance", blank=True,null=True, max_length=500, unique=False)
    phone=models.CharField(blank=True, null=True, verbose_name="phone", max_length=10)
    Location=models.CharField(verbose_name="Mahali", max_length=200, blank=True, null=True)
    
    JinaLaKituo = models.ForeignKey(VituoVyote, on_delete=models.PROTECT, blank=True,null=True) 
    
    profile_image = models.ImageField(upload_to='media/',verbose_name="Picha Ya Mtu", blank=True, null=True)
    #profile_image = models.ImageField(upload_to='media/',verbose_name="Picha Ya Mtu", blank=True, null=True, default='mtu.jpg')
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    # Role_Choices = (
    #         ('MULTI TEACHER', 'MULTI TEACHER'),
    #         ('PHYSICS TEACHER', 'PHYSICS TEACHER'),
    #         ('CHEMISTRY TEACHER', 'CHEMISTRY TEACHER'),
    #         ('BIOLOGY TEACHER', 'BIOLOGY TEACHER'),
    #         ('ENGLISH TEACHER', 'ENGLISH TEACHER'),
    #         ('CIVICS TEACHER', 'CIVICS TEACHER'),
    #         ('MATHEMATICS TEACHER', 'MATHEMATICS TEACHER'),
    #         ('HISTORY TEACHER', 'HISTORY TEACHER'),
    #         ('GEOGRAPHY TEACHER', 'GEOGRAPHY TEACHER'),
    #         ('KISWAHILI TEACHER', 'KISWAHILI TEACHER'),
    #     )

    # role=models.CharField(verbose_name="role", choices=Role_Choices, max_length=50)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_cashier=models.BooleanField(default=True)

    hide_email = models.BooleanField(default=True)

    
    


    USERNAME_FIELD="username"
    REQUIRED_FIELDS=['email']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # Method to update push token
    def update_push_token(self, token):
        self.expo_push_token = token
        self.save()


    # def save(self, *args, **kwargs):
    #     if self.date_joined and self.last_login and self.date_joined > self.last_login:
    #         raise ValueError("Created date cannot be later than Updated date.")
    #     super().save(*args, **kwargs)






class OTP(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        super().save(*args, **kwargs)

    def is_valid(self):
        from django.utils import timezone
        return self.created_at >= timezone.now() - timezone.timedelta(minutes=10)














class WatejaWote(models.Model):
    reg_no= models.CharField(max_length=100000, default=generated_reg_no, unique=True, editable=False,blank=True,null=True)
    
    Aina = models.ForeignKey(AinaZaMarejesho,verbose_name="Aina Ya Mpokeaji", on_delete=models.PROTECT, blank=True,null=True) 

    JinaKamiliLaMteja = models.CharField(verbose_name="Jina Kamili La Mteja", max_length=500,blank=True,null=True)
    JinaLaKituo = models.ForeignKey(VituoVyote, on_delete=models.PROTECT, blank=True,null=True) 

    SimuYaMteja = models.IntegerField(verbose_name="Namba Ya Simu Ya Mteja", blank=True,null=True)
    SimuYaMzaminiWa1 = models.IntegerField(verbose_name="Namba Ya Simu Ya Mzamini Wa 1", blank=True,null=True)
    SimuYaMzaminiWa2 = models.IntegerField(verbose_name="Namba Ya Simu Ya Mzamini Wa 2", blank=True,null=True)
    JinaLaMzaminiWa1 = models.CharField(verbose_name="Jina Kamili La Mzamini Wa 1", max_length=500,blank=True,null=True)
    JinaLaMzaminiWa2 = models.CharField(verbose_name="Jina Kamili La Mzamini Wa 2", max_length=500,blank=True,null=True)

    EmailYaMteja = models.EmailField(verbose_name="Email Ya Mteja", max_length=500,blank=True,null=True)
    Mahali = models.CharField(verbose_name="Mahali Anapoishi", max_length=500,blank=True,null=True)
    MaelezoYaMteja = models.TextField(verbose_name="Maelezo Ya Mteja", max_length=10000,blank=True,null=True)

    KiasiAnachokopa = models.IntegerField(verbose_name="Kiasi Kiasi Anachokopa", blank=True,null=True, default=0)
    KiasiAlicholipa = models.IntegerField(verbose_name="Kiasi Alicholipa Mpaka Sasa", blank=True,null=True, default=0)
    RejeshoKwaSiku = models.IntegerField(verbose_name="Rejesho Kwa Siku", blank=True,null=True, default=0)
    JumlaYaDeni = models.IntegerField(verbose_name="Jumla Ya Deni Analodaiwa", blank=True,null=True, default=0)
    Riba = models.IntegerField(verbose_name="Riba", blank=True,null=True, default=0)

    AmesajiliwaNa = models.CharField(verbose_name="Amesajiliwa Na ?", max_length=500,blank=True,null=True)
    Amerejesha_Leo = models.BooleanField(default=False, blank=True, null=True)
    
    PichaYaMteja = models.ImageField(verbose_name="Picha Ya Mteja", upload_to='media/PichaZaVyakula/',blank=True,null=True)

    #if created is greater than 30 inakuwa false
    Ni_Mteja_Hai = models.BooleanField(default=True, blank=True, null=True)

    Nje_Ya_Mkata_Wote = models.BooleanField(default=False, blank=True, null=True)
    Nje_Ya_Mkata_Leo = models.BooleanField(default=False, blank=True, null=True)

    Wamemaliza_Hawajakopa_Tena = models.BooleanField(default=False, blank=True, null=True)
    
    
    Up_To = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    JumlaYaFainiZote = models.IntegerField(verbose_name="JumlaYaFainiZote", blank=True,null=True, default=0)

    Created = models.DateTimeField(default=now, blank=True, null=True)
    Updated = models.DateTimeField(auto_now=True)


    Interval = models.IntegerField(verbose_name="Interval", blank=True,null=True, default=0)
    Kiasicha_Riba_Kwa_Muda_Wa_Mkopo = models.IntegerField(verbose_name="Kiasicha Riba Kwa Muda Wa Mkopo (Kwa Watumishi wa Umma )", blank=True,null=True, default=0)

    # AinaZaMarejesho_Choices = (
    #         ('Kila Siku', 'Kila Siku'),
    #         ('Baada Ya Mwezi', 'Baada Ya Mwezi'),

    #     )
    # AinaZaMarejesho = models.CharField(choices=AinaZaMarejesho_Choices, verbose_name="Aina Za Marejesho",max_length=500, blank=True,null=True)

    time_left = models.IntegerField(blank=True, null=True)
    is_red = models.BooleanField(default=False)


    AinaYaKazi = models.CharField(verbose_name="Aina Ya Kazi", max_length=500,blank=True,null=True)
    KituoChaKazi = models.CharField(verbose_name="Kituo Cha Kazi", max_length=500,blank=True,null=True)
    IdaraYaKazi = models.CharField(verbose_name="Idara Ya Kazi", max_length=500,blank=True,null=True)
    KataYaKazi = models.CharField(verbose_name="Kata Ya Kazi", max_length=500,blank=True,null=True)
    CheckNo = models.IntegerField(verbose_name="Check Number", blank=True,null=True, default=0)


    #AinaYaKitambulisho = models.ForeignKey(Vitambulisho, on_delete=models.PROTECT, blank=True,null=True) 
    #NambaYaKitambulisho = models.CharField(verbose_name="Namba Ya Kitambulisho", max_length=500,blank=True,null=True)

    
    
    class Meta:
        verbose_name_plural = "Wateja Wote"
        
    
    def __str__(self):
        return f" {self.JinaKamiliLaMteja} "

    #TUKIENDA KWENYE SERVER TUTATUMIA HII
    

    # def check_conditions(self):
    #     """Checks and updates fields based on time differences."""
    #     time_elapsed = (now() - self.Created).days

    #     if time_elapsed == 30 and self.Ni_Mteja_Hai:
    #         self.Ni_Mteja_Hai = False
    #         self.save(update_fields=['Ni_Mteja_Hai'])

    #     if time_elapsed == 30 and not self.Nje_Ya_Mkata_Leo:
    #         self.Nje_Ya_Mkata_Leo = True
    #         self.save(update_fields=['Nje_Ya_Mkata_Leo'])

    #     if time_elapsed == 40 and not self.Nje_Ya_Mkata_Wote:
    #         self.Nje_Ya_Mkata_Wote = True
    #         self.save(update_fields=['Nje_Ya_Mkata_Wote'])



    @property
    def time_left(self):
        if not self.Created:
            return None  # Return None if Created is not set
        # Calculate time elapsed in days
        time_elapsed = (timezone.now() - self.Created).days
        # Start counting from 1 instead of 0
        return time_elapsed + 1



    # @property
    # def is_red(self):
    #     #background iwe red endapo ukichukua siku alizotaka kukumbushwa - muda wa sasa
    #     #sawasawa na siku 1 background iwe nyekundu, maana yake tunamkumbusha user
    #     #siku moja kabla sa siku aliyoweka
        
    #     return self.time_left == 30

    @property
    def is_red(self):
        time_left = self.time_left
        if time_left is None:
            return False  # Rudisha False ikiwa hakuna tarehe ya kuanza (Created)
        return time_left == 30




class WatejaWoteCart(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    JinaKamiliLaMteja = models.CharField(verbose_name="Jina Kamili La Mteja", max_length=500,blank=True,null=True)
    ordered = models.BooleanField(default=False)
    total_price = models.IntegerField(verbose_name="Jumla Ya Kiasi Alicholipa", default=0, blank=True, null=True)
    
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "WatejaWote  Cart"

    def __str__(self):
        return str(self.JinaKamiliLaMteja) + " " + str(self.total_price)
         


class WatejaWoteCartItems(models.Model):
    cart = models.ForeignKey(WatejaWoteCart, on_delete=models.PROTECT) 
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    JinaKamiliLaMteja = models.CharField(verbose_name="Jina Kamili La Mteja", max_length=500,blank=True,null=True)
    
    Mteja = models.ForeignKey(WatejaWote,on_delete=models.PROTECT)
    KiasiChaRejeshoChaSiku = models.FloatField(default=0, blank=True,null=True)
    KiasiChaFainiChaSiku = models.FloatField(default=0, blank=True,null=True)
    #Customer = models.ForeignKey(ProductsCustomers,on_delete=models.PROTECT,blank=True,null=True)
    quantity = models.IntegerField(default=1, blank=True,null=True)
    #table = models.ForeignKey(ProductsTables,on_delete=models.PROTECT,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "WatejaWote  Cart Items"
    
    def __str__(self):
        return f" {self.Mteja.JinaKamiliLaMteja}"
        
    

# @receiver(pre_save, sender=WatejaWoteCartItems)
# def Wateja__correct_price(sender, **kwargs):
#     cart_items = kwargs['instance']
#     price_of_product = WatejaWote.objects.get(id=cart_items.Mteja.id)
#     cart_items.KiasiChaRejeshoChaSiku = cart_items.quantity * float(price_of_product.price)
#     # total_cart_items = CartItems.objects.filter(user = cart_items.user )
#     # cart = Cart.objects.get(id = cart_items.cart.id)
#     # cart.total_price = cart_items.price
#     # cart.save()



class MarejeshoCopies(models.Model):
    reg_no = models.CharField(verbose_name="Namba Ya Mteja", max_length=100000, blank=True, null=True)

    JinaKamiliLaMteja = models.CharField(verbose_name="Jina Kamili La Mteja", max_length=500, blank=True, null=True)
    JinaLaKituo = models.CharField(verbose_name="Jina La Kituo Cha Mteja", max_length=500, blank=True, null=True)
    #JinaLaKituo = models.ForeignKey(VituoVyote, on_delete=models.PROTECT, blank=True, null=True)
    SimuYaMteja = models.IntegerField(verbose_name="Namba Ya Simu Ya Mteja", blank=True, null=True)
    EmailYaMteja = models.EmailField(verbose_name="Email Ya Mteja", max_length=500, blank=True, null=True)
    Mahali = models.CharField(verbose_name="Mahali Anapoishi", max_length=500, blank=True, null=True)
    KiasiAnachokopa = models.IntegerField(verbose_name="Kiasi Anachokopa", blank=True, null=True, default=0)
    KiasiAlicholipa = models.IntegerField(verbose_name="Kiasi Alicholipa", blank=True, null=True, default=0)
    RejeshoKwaSiku = models.IntegerField(verbose_name="Rejesho Kwa Siku", blank=True, null=True, default=0)
    JumlaYaDeni = models.IntegerField(verbose_name="Jumla Ya Deni Analodaiwa", blank=True, null=True, default=0)
    Riba = models.IntegerField(verbose_name="Riba", blank=True, null=True, default=0)
    RejeshoLililoPokelewaLeo = models.IntegerField(verbose_name="Rejesho Lililo Pokelewa Leo", blank=True, null=True, default=0)
    FainiKwaSiku = models.IntegerField(verbose_name="Faini Kwa Siku", blank=True, null=True, default=0)

    AmesajiliwaNa = models.CharField(verbose_name="Amesajiliwa Na ?", max_length=500, blank=True, null=True)
    PichaYaMteja = models.ImageField(verbose_name="Picha Ya Mteja", upload_to='media/PichaZaVyakula/', blank=True, null=True)
    Ni_Mteja_Hai = models.BooleanField(default=True, blank=True, null=True)
    Created = models.DateTimeField(default=now, blank=True, null=True)
    Updated = models.DateTimeField(auto_now=True)
    Up_To = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Marejesho Copies"

    def __str__(self):
        return f"{self.JinaKamiliLaMteja}"


class MarejeshoCopiesTwo(models.Model):
    reg_no = models.CharField(verbose_name="Namba Ya Mteja", max_length=100000, blank=True, null=True)

    JinaKamiliLaMteja = models.CharField(verbose_name="Jina Kamili La Mteja", max_length=500, blank=True, null=True)
    JinaLaKituo = models.CharField(verbose_name="Jina La Kituo Cha Mteja", max_length=500, blank=True, null=True)
    #JinaLaKituo = models.ForeignKey(VituoVyote, on_delete=models.PROTECT, blank=True, null=True)
    SimuYaMteja = models.IntegerField(verbose_name="Namba Ya Simu Ya Mteja", blank=True, null=True)
    EmailYaMteja = models.EmailField(verbose_name="Email Ya Mteja", max_length=500, blank=True, null=True)
    Mahali = models.CharField(verbose_name="Mahali Anapoishi", max_length=500, blank=True, null=True)
    KiasiAnachokopa = models.IntegerField(verbose_name="Kiasi Anachokopa", blank=True, null=True, default=0)
    KiasiAlicholipa = models.IntegerField(verbose_name="Kiasi Alicholipa", blank=True, null=True, default=0)
    RejeshoKwaSiku = models.IntegerField(verbose_name="Rejesho Kwa Siku", blank=True, null=True, default=0)
    JumlaYaDeni = models.IntegerField(verbose_name="Jumla Ya Deni Analodaiwa", blank=True, null=True, default=0)
    Riba = models.IntegerField(verbose_name="Riba", blank=True, null=True, default=0)
    RejeshoLililoPokelewaLeo = models.IntegerField(verbose_name="Rejesho Lililo Pokelewa Leo", blank=True, null=True, default=0)
    FainiKwaSiku = models.IntegerField(verbose_name="Faini Kwa Siku", blank=True, null=True, default=0)

    AmesajiliwaNa = models.CharField(verbose_name="Amesajiliwa Na ?", max_length=500, blank=True, null=True)
    PichaYaMteja = models.ImageField(verbose_name="Picha Ya Mteja", upload_to='media/PichaZaVyakula/', blank=True, null=True)
    Ni_Mteja_Hai = models.BooleanField(default=True, blank=True, null=True)
    Created = models.DateTimeField(default=now, blank=True, null=True)
    Updated = models.DateTimeField(auto_now=True)
    Up_To = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Marejesho Copies Two"

    def __str__(self):
        return f"{self.JinaKamiliLaMteja}"


class NjeYaMkatabaCopies(models.Model):
    reg_no = models.CharField(verbose_name="Namba Ya Mteja", max_length=100000, blank=True, null=True)

    JinaKamiliLaMteja = models.CharField(verbose_name="Jina Kamili La Mteja", max_length=500, blank=True, null=True)
    JinaLaKituo = models.CharField(verbose_name="Jina La Kituo Cha Mteja", max_length=500, blank=True, null=True)
    #JinaLaKituo = models.ForeignKey(VituoVyote, on_delete=models.PROTECT, blank=True, null=True)
    SimuYaMteja = models.IntegerField(verbose_name="Namba Ya Simu Ya Mteja", blank=True, null=True)
    EmailYaMteja = models.EmailField(verbose_name="Email Ya Mteja", max_length=500, blank=True, null=True)
    Mahali = models.CharField(verbose_name="Mahali Anapoishi", max_length=500, blank=True, null=True)
    KiasiAnachokopa = models.IntegerField(verbose_name="Kiasi Anachokopa", blank=True, null=True, default=0)
    KiasiAlicholipa = models.IntegerField(verbose_name="Kiasi Alicholipa", blank=True, null=True, default=0)
    RejeshoKwaSiku = models.IntegerField(verbose_name="Rejesho Kwa Siku", blank=True, null=True, default=0)
    JumlaYaDeni = models.IntegerField(verbose_name="Jumla Ya Deni Analodaiwa", blank=True, null=True, default=0)
    Riba = models.IntegerField(verbose_name="Riba", blank=True, null=True, default=0)
    RejeshoLililoPokelewaLeo = models.IntegerField(verbose_name="Rejesho Lililo Pokelewa Leo", blank=True, null=True, default=0)
    FainiKwaSiku = models.IntegerField(verbose_name="Faini Kwa Siku", blank=True, null=True, default=0)

    AmesajiliwaNa = models.CharField(verbose_name="Amesajiliwa Na ?", max_length=500, blank=True, null=True)
    PichaYaMteja = models.ImageField(verbose_name="Picha Ya Mteja", upload_to='media/PichaZaVyakula/', blank=True, null=True)
    Ni_Mteja_Hai = models.BooleanField(default=True, blank=True, null=True)
    Created = models.DateTimeField(default=now, blank=True, null=True)
    Updated = models.DateTimeField(auto_now=True)
    Up_To = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Nje Ya Mkataba Copies"

    def __str__(self):
        return f"{self.JinaKamiliLaMteja}"



class MalipoYaFainiCopies(models.Model):
    reg_no = models.CharField(verbose_name="Namba Ya Mteja", max_length=100000, blank=True, null=True)
    
    JinaKamiliLaMteja = models.CharField(verbose_name="Jina Kamili La Mteja", max_length=500, blank=True, null=True)
    JinaLaKituo = models.CharField(verbose_name="Jina La Kituo Cha Mteja", max_length=500, blank=True, null=True)
    #JinaLaKituo = models.ForeignKey(VituoVyote, on_delete=models.PROTECT, blank=True, null=True)
    SimuYaMteja = models.IntegerField(verbose_name="Namba Ya Simu Ya Mteja", blank=True, null=True)
    EmailYaMteja = models.EmailField(verbose_name="Email Ya Mteja", max_length=500, blank=True, null=True)
    Mahali = models.CharField(verbose_name="Mahali Anapoishi", max_length=500, blank=True, null=True)
    KiasiAnachokopa = models.IntegerField(verbose_name="Kiasi Anachokopa", blank=True, null=True, default=0)
    KiasiAlicholipa = models.IntegerField(verbose_name="Kiasi Alicholipa", blank=True, null=True, default=0)
    RejeshoKwaSiku = models.IntegerField(verbose_name="Rejesho Kwa Siku", blank=True, null=True, default=0)
    JumlaYaDeni = models.IntegerField(verbose_name="Jumla Ya Deni Analodaiwa", blank=True, null=True, default=0)
    Riba = models.IntegerField(verbose_name="Riba", blank=True, null=True, default=0)
    FainiIliyoPokelewaLeo = models.IntegerField(verbose_name="Faini Iliyopokelewa Leo", blank=True, null=True, default=0)
    FainiKwaSiku = models.IntegerField(verbose_name="Faini Kwa Siku", blank=True, null=True, default=0)

    AmesajiliwaNa = models.CharField(verbose_name="Amesajiliwa Na ?", max_length=500, blank=True, null=True)
    PichaYaMteja = models.ImageField(verbose_name="Picha Ya Mteja", upload_to='media/PichaZaVyakula/', blank=True, null=True)
    Ni_Mteja_Hai = models.BooleanField(default=True, blank=True, null=True)
    Created = models.DateTimeField(default=now, blank=True, null=True)
    Updated = models.DateTimeField(auto_now=True)
    Up_To = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Malipo Ya Faini Copies"

    def __str__(self):
        return f"{self.JinaKamiliLaMteja}"


class Ripoti(models.Model):
    JinaLaKituo = models.ForeignKey(VituoVyote, on_delete=models.PROTECT, blank=True, null=True)
    JumlaMarejeshoYaLeo = models.IntegerField(verbose_name="Jumla Ya Marejesho Ya Leo", blank=True, null=True)
    JumlaFainiLeo = models.IntegerField(verbose_name="Jumla Ya Faini Za Leo", blank=True, null=True)
    FomuNaBima = models.IntegerField(verbose_name="Fomu Na Bima", blank=True, null=True)
    BakiJana = models.IntegerField(verbose_name="Kiasi Kilichobaji Jana", blank=True, null=True)
    ImetokaKwaBosi = models.IntegerField(verbose_name="Imetoka Kwa Bosi", blank=True, null=True)
    ImetokaKituoJirani = models.IntegerField(verbose_name="Imetoka Kituo Jirani", blank=True, null=True)
    MapatoYaJumla = models.IntegerField(verbose_name="Jumla Ya Mapato Ya Leo", blank=True, null=True)
    
    Mkopo = models.IntegerField(verbose_name="Mkopo", blank=True, null=True)
    Posho = models.IntegerField(verbose_name="Posho", blank=True, null=True)
    ImeendaKwaBosi = models.IntegerField(verbose_name="Imeenda Kwa Bosi", blank=True, null=True)
    ImeendaKituoJirani = models.IntegerField(verbose_name="Imeenda Kituo Jirani", blank=True, null=True)
    MatumiziMengine = models.IntegerField(verbose_name="Matumizi Mengine", blank=True, null=True)
    MatumiziYaJumla = models.IntegerField(verbose_name="Matumizi Ya Jumla", blank=True, null=True)
    
    IdadiYaMikopoYaLeo = models.IntegerField(verbose_name="Idadi Ya Mikopo Ya Leo", blank=True, null=True)
    IdadiYaMikatabaMipyaLeo = models.IntegerField(verbose_name="Idadi Ya Mikataba Mipya Leo", blank=True, null=True)
    IdadiYaWenyeMikatabaHai = models.IntegerField(verbose_name="Idadi Ya Wenye Mikataba Hai", blank=True, null=True)
    IdadiYaWaliorejeshaLeo = models.IntegerField(verbose_name="Idadi Ya Waliorejesha Leo", blank=True, null=True)
    IdadiYaFainiZilizopokelewaLeo = models.IntegerField(verbose_name="Idadi Ya Faini Zilizopokelewa Leo", blank=True, null=True)
    
    Balance = models.IntegerField(verbose_name="Balance", blank=True, null=True)

    KituoIlichoendaHela = models.CharField(verbose_name="Kituo Ilichoenda Hela", max_length=500, blank=True, null=True)
    KituoIlichotokaHela = models.CharField(verbose_name="Kituo Ilichotoka Hela", max_length=500, blank=True, null=True)

    ImeweingizwaNa = models.CharField(verbose_name="Imeweingizwa Na ?", max_length=500, blank=True, null=True)   
    Created = models.DateTimeField(default=now, blank=True, null=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Ripoti"

    def __str__(self):
        return f"{self.id}"









class JumbeZaWateja(models.Model):
    JinaKamiliLaMteja = models.CharField(verbose_name="Jina La Mteja",max_length=500, blank=True,null=True)
    SimuYaMteja = models.IntegerField(verbose_name="Simu Ya Mteja", blank=True,null=True)
    EmailYaMteja = models.EmailField(verbose_name="Email Ya Mteja",max_length=200, blank=True,null=True)
    
    Message = models.TextField(verbose_name="Ujumbe",max_length=10000, blank=True,null=True)
    
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.Message}"
    
    class Meta:
        verbose_name_plural = "Jumbe Za Wateja"