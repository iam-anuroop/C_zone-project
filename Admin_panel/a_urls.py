from django.urls import path
from . import views


urlpatterns = [
    path('',views.Adminpanel_view,name='adminpanel'),
    path('accepthotel/<int:hotel_id>/',views.Hotelaccept,name='hotelaccept'),
    path('rejecthotel/<int:hotel_id>/',views.Hotelreject,name='hotelreject'),
    path('admin_hotel/',views.Admin_hotel_view,name='adminhotel'),
    path('admin_user/',views.Admin_user_view,name='adminuser'),
    path('admin_hotel_payment/',views.Admin_hotel_payment_view,name='adminhotelpayment'),

]