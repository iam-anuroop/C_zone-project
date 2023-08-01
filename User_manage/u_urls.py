from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name='registration'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('emailnotification/',views.emailnotification,name='emailnotification'),
    path('resetpassword/<uidb64>/<token>/',views.resetpasswordorusername,name='resetpassword'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('userprofile/',views.Profileupdate,name='userprofile'),
    path('userdelete/',views.Userdelete,name='userdelete'),
    path('yourbookings/',views.Your_bookings,name='yourbookings'),
    path('invoice/<int:booking_id>/',views.invoice_view,name='invoice'),

    ]