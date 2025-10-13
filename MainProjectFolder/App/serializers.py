from App.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from App.models import *

from rest_framework import serializers
from django.contrib.auth.hashers import check_password

# from rest_framework.validators import UniqueValidator
# from rest_framework_jwt.settings import api_settings



class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = self.context['request'].user

        # Check if the current password is correct
        if not check_password(data['current_password'], user.password):
            raise serializers.ValidationError({'current_password': 'Neno siri uliloingiza sio sahihi'})

        # Check if new password matches confirm password
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})

        return data





class VituoVyoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VituoVyote
        fields = '__all__'


class AinaZaMarejeshoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AinaZaMarejesho
        fields = '__all__'



class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(max_length=128)

    def validate(self, data):
        try:
            user = MyUser.objects.get(email=data['email'])
        except MyUser.DoesNotExist:
            raise serializers.ValidationError("Mtumiaji mwenye email hii teyari yupo.")

        otp_instance = OTP.objects.filter(user=user, otp=data['otp']).last()
        if not otp_instance or not otp_instance.is_valid():
            raise serializers.ValidationError("OTP sio sahihi au imeshaisha muda wake.")
        return data

    def save(self):
        user = MyUser.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.save()
        OTP.objects.filter(user=user).delete()
        return user

        


class MyUserSerializer(serializers.ModelSerializer):
    JinaLaKituo = VituoVyoteSerializer(many=False)
    
    class Meta:
        model = MyUser
        fields = '__all__'










class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        #fields = ('username', 'email','phone', 'password')
        #fields = ['password', 'username','is_admin', 'is_staff', 'is_cashier']
        fields= '__all__'




class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'username', 
            'email', 
            'phone',
            'company_name',
            
            'profile_image',
            
            'Location'
        )



#______________MWISHO HAPA DJANGO REACT AUTHENTICATION_________________





class UserDataSerializer(serializers.ModelSerializer):
    JinaLaKituo = VituoVyoteSerializer(many=False)
    
    class Meta:
        model = MyUser
        fields = '__all__'
        # fields = ['id', 'username', 'email','phone','first_name','profile_image']












# kwa ajili ya kumregister mtu bila kutumia token
class UserCreationSerializer(serializers.ModelSerializer):
	username=serializers.CharField(max_length=25)
	email=serializers.EmailField(max_length=50)
	password=serializers.CharField(max_length=50)


	class Meta:
		model= MyUser
		fields= ['username','email','password']
		#fields='__all__'

	def validate(self,attrs):
		username_exists = MyUser.objects.filter(username=attrs['username']).exists()
		if username_exists:
			raise serializers.ValidationError(detail="User with username already exists")


		email_exists = MyUser.objects.filter(email=attrs['email']).exists()
		if email_exists:
			raise serializers.ValidationError(detail="User with email already exists")

		return super().validate(attrs)




class AddWatejaWoteSerializer(serializers.ModelSerializer):
    #JinaLaKituo = VituoVyoteSerializer(many=False)
    # FoodGroup = MakundiYaWatejaWoteSerializer(many=False)
    class Meta:
        model = WatejaWote
        fields = '__all__'

class WatejaWoteSerializer(serializers.ModelSerializer):
    JinaLaKituo = VituoVyoteSerializer(many=False)
    # FoodGroup = MakundiYaWatejaWoteSerializer(many=False)
    class Meta:
        model = WatejaWote
        fields = '__all__'


#--------------------CART AND CART ITEMS--------------------
class WatejaWoteCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatejaWoteCart
        fields = '__all__'


class WatejaWoteCartItemsSerializer(serializers.ModelSerializer):
    cart = WatejaWoteCartSerializer()
    Mteja = WatejaWoteSerializer()

    #table = WatejaWoteTablesSerializer()
    class Meta:
        model = WatejaWoteCartItems
        fields = '__all__'




class MarejeshoCopiesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MarejeshoCopies
        fields = '__all__'

class MarejeshoCopiesTwoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MarejeshoCopiesTwo
        fields = '__all__'

class MalipoYaFainiCopiesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MalipoYaFainiCopies
        fields = '__all__'

class NjeYaMkatabaCopiesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NjeYaMkatabaCopies
        fields = '__all__'

class RipotiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ripoti
        fields = '__all__'





class JumbeZaWatejaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JumbeZaWateja
        fields = '__all__'