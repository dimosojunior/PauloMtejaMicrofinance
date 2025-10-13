from . import views
from django.urls import path


urlpatterns = [
	

    

    #---------------KWA AJILI YA APIS --------------
    path('register_user/', views.RegistrationView.as_view(), name='register2'),
    path('login_user/', views.ReactLoginView.as_view(), name='login2'),
    path('logout_user/', views.LogoutView.as_view(), name='logout2'),
    path('user_data/', views.UserDataView.as_view(), name='user-data2'),
    path('update_user/', views.UpdateUserView.as_view(), name='update_user'),

    path('send-otp/', views.SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    # path('UserView/', views.UserView.as_view(), name="UserView"),

     
]