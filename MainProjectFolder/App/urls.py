from django.urls import path
from . import views


#app_name = "polls"

urlpatterns = [

    path('SendSMSNextSMSView/', views.SendSMSNextSMSView.as_view(), name='SendSMSNextSMSView'),
    path('SendSMSBeemView/', views.SendSMSBeemView.as_view(), name='SendSMSBeemView'),
    


    
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),

    path('LatestVersionView/', views.LatestVersionView.as_view(), name='LatestVersionView'),
    
    path('AddWatejaWoteView/', views.AddWatejaWoteView.as_view(), name='AddWatejaWoteView'),
    path('GetAllWatejaWoteView/', views.GetAllWatejaWoteView.as_view(), name='GetAllWatejaWoteView'),
    path('GetMarejeshoWatejaWoteHaiView/', views.GetMarejeshoWatejaWoteHaiView.as_view(), name='GetMarejeshoWatejaWoteHaiView'),

    path('WatejaWoteCart/', views.WatejaWoteCartView.as_view(), name='WatejaWoteCart'),
    #path('WatejaWoteOrder/', views.WatejaWoteOrderView.as_view(), name='WatejaWote--order-list'),

    path('RetrieveWatejaWoteView/<int:pk>/', views.RetrieveWatejaWoteView.as_view(), name='RetrieveWatejaWoteView'),
    path('UpdateWatejaWotePostView/<int:pk>/edit/', views.UpdateWatejaWotePostView.as_view(), name='UpdateWatejaWotePostView'),
    path('DeleteWatejaWotePostView/<int:pk>/delete/', views.DeleteWatejaWotePostView.as_view(), name='DeleteWatejaWotePostView'),
    path('CountAllWatejaWoteView/', views.CountAllWatejaWoteView.as_view(), name='CountAllWatejaWoteView'),
    path('CountAllWatejaWoteNjeYaMikataView/', views.CountAllWatejaWoteNjeYaMikataView.as_view(), name='CountAllWatejaWoteNjeYaMikataView'),
    
    path('GetMarejeshoKwaSikuYaLeoView/', views.GetMarejeshoKwaSikuYaLeoView.as_view(), name='GetMarejeshoKwaSikuYaLeoView'),
    path('FilterMarejeshoYaSikuByDate/', views.FilterMarejeshoYaSikuByDate.as_view(), name='FilterMarejeshoYaSikuByDate'),

    path('GetWatejaNjeYaMkatabaLeoView/', views.GetWatejaNjeYaMkatabaLeoView.as_view(), name='GetWatejaNjeYaMkatabaLeoView'),
    path('GetWatejaNjeYaMkatabaWoteView/', views.GetWatejaNjeYaMkatabaWoteView.as_view(), name='GetWatejaNjeYaMkatabaWoteView'),
    path('GetWatejaHaiWote/', views.GetWatejaHaiWote.as_view(), name='GetWatejaHaiWote'),


    path('GetFainiKwaSikuYaLeoView/', views.GetFainiKwaSikuYaLeoView.as_view(), name='GetFainiKwaSikuYaLeoView'),
    path('FilterFainiYaSikuByDate/', views.FilterFainiYaSikuByDate.as_view(), name='FilterFainiYaSikuByDate'),


    path('GetMarejeshoWatejaWoteHaiView2/', views.GetMarejeshoWatejaWoteHaiView2.as_view(), name='GetMarejeshoWatejaWoteHaiView2'),
    path('GetFainiWatejaWoteHaiView2/', views.GetFainiWatejaWoteHaiView2.as_view(), name='GetFainiWatejaWoteHaiView2'),





    path('AddRipotiView/', views.AddRipotiView.as_view(), name='AddRipotiView'),
    path('GetRipotiSikuYaLeoView/', views.GetRipotiSikuYaLeoView.as_view(), name='GetRipotiSikuYaLeoView'),
    path('FilterRipotiYaSikuByDate/', views.FilterRipotiYaSikuByDate.as_view(), name='FilterRipotiYaSikuByDate'),




    path('GetHawajarejeshaJanaView/', views.GetHawajarejeshaJanaView.as_view(), name='GetHawajarejeshaJanaView'),
    path('FilterHawajarejeshaByDate/', views.FilterHawajarejeshaByDate.as_view(), name='FilterHawajarejeshaByDate'),

    path('MalipoYaFainiCartView/', views.MalipoYaFainiCartView.as_view(), name='MalipoYaFainiCartView'),
    path('CountHawajarejeshaJanaView/', views.CountHawajarejeshaJanaView.as_view(), name='CountHawajarejeshaJanaView'),


    path('GetMarejeshoYoteYaMtejaView/', views.GetMarejeshoYoteYaMtejaView.as_view(), name='GetMarejeshoYoteYaMtejaView'),
    path('GetWamemalizaHawajakopaTenaView/', views.GetWamemalizaHawajakopaTenaView.as_view(), name='GetWamemalizaHawajakopaTenaView'),
    path('CountAllWamemalizaHawajakopaTenaView/', views.CountAllWamemalizaHawajakopaTenaView.as_view(), name='CountAllWamemalizaHawajakopaTenaView'),


    path('DeleteRejeshoView/<int:pk>/delete/', views.DeleteRejeshoView.as_view(), name='DeleteRejeshoView'),
    path('DeleteFainiView/<int:pk>/delete/', views.DeleteFainiView.as_view(), name='DeleteFainiView'),





    
    path('GetNjeYaMkatabaTareheFulaniView/', views.GetNjeYaMkatabaTareheFulaniView.as_view(), name='GetNjeYaMkatabaTareheFulaniView'),
    path('FilterNjeYaMkatabaTareheFulaniByDate/', views.FilterNjeYaMkatabaTareheFulaniByDate.as_view(), name='FilterNjeYaMkatabaTareheFulaniByDate'),



    #path('SendSampleText/', views.SendSampleText.as_view(), name='SendSampleText'),

    path('DeleteRipotiView/<int:pk>/delete/', views.DeleteRipotiView.as_view(), name='DeleteRipotiView'),

    



    path('OngezaKituoView/', views.OngezaKituoView.as_view(), name='OngezaKituoView'),


    path('GetVituoVyoteView/', views.GetVituoVyoteView.as_view(), name='GetVituoVyoteView'),
    path('DeleteKituoView/<int:pk>/delete/', views.DeleteKituoView.as_view(), name='DeleteKituoView'),

    path('GetMyUserView/', views.GetMyUserView.as_view(), name='GetMyUserView'),
    path('DeleteMyUserView/<int:pk>/delete/', views.DeleteMyUserView.as_view(), name='DeleteMyUserView'),






    path('TumaMsgKwaMtejaView/', views.TumaMsgKwaMtejaView.as_view(), name='TumaMsgKwaMtejaView'),
    path('GetTransactionSummaryView/', views.GetTransactionSummaryView.as_view(), name='GetTransactionSummaryView'),

]
