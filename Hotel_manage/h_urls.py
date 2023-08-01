from django.urls import path
from . import views

urlpatterns = [
    path('',views.Hotelregister,name='hotelregistration'),
    path('hotel_owner/',views.ownerregistration,name='hotelowner_reg'),
    path('activatehotel/<uidb64>/<token>/',views.activatehotel,name='activatehotel'),
    path('hotel_login/',views.Hotellogin,name='hotellogin'),
    path('hotel_home/',views.Hotelhome,name='hotelhome'),
    path('hotel_logout/',views.Hotellogout,name='hotellogout'),
    path('roomtype/',views.Roomtype_view,name='roomtypeupdate'),
    path('hotelrooms/<int:hotel_id>/',views.Hotel_rooms_view,name='hotelrooms'),
    path('hotelbook/<int:hotel_id>/<int:room_id>',views.hotel_book,name='hotelbook'),
    path('payment/<int:booking_id>/<int:room_id>',views.Payment_view,name='payment'),


    path('success/',views.success,name='success')
    ]
