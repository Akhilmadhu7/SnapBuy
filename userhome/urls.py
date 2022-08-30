from django.urls import path
from . import views


urlpatterns = [

    path('userlogin',views.userlog_view,name='userlog'),

    path('otp-verify/<int:phone_number>/',views.otpverify,name='otp'),

    path('phone-login',views.phonelogin,name='phone_login'),

    path('',views.index_view,name='userindex'),

    path('userlogout',views.userlogout_view,name='user_logout'),
    
    path('userregister',views.userregister_view,name='register'),

    path('userprofile',views.profile_view,name='profile'),

    path('editprofile/<int:id>/',views.editprofile_view, name= 'profile_edit'),

    path('add_address',views.add_addressview, name='address_add'),

    path('editpassword/<int:id>/',views.editpassword_view,name='change_password'),

    path('delete-address/<int:id>/',views.delete_address,name='del_address')
  
]