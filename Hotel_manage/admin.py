from django.contrib import admin
from .models import HotelDetails,Roomtype,BookingDetails,Hotelowner,PaymentDetails,ReviewDetails

# Register your models here.

class HoteldetailsAdmin(admin.ModelAdmin):
    list_display = ('id','hotel_name','hotel_email','last_login', 'date_joined')
admin.site.register(HotelDetails,HoteldetailsAdmin)

class HotelownerAdmin(admin.ModelAdmin):
    list_display = ('id','hotel_id','owner_name')
admin.site.register(Hotelowner,HotelownerAdmin)

class RoomtypeAdmin(admin.ModelAdmin):
    list_display = ('id','hotel_id','roomtype','created_at','updated_at')
admin.site.register(Roomtype,RoomtypeAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id','user','hotel','room_type','check_in_date','check_out_date')
admin.site.register(BookingDetails,BookingAdmin)

class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','hotel','user','amount_paid')
admin.site.register(PaymentDetails,PaymentDetailsAdmin)

class ReviewDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','hotel','user','rating','comment')
admin.site.register(ReviewDetails,ReviewDetailsAdmin)