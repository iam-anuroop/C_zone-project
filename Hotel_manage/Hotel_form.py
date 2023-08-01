# forms.py
from django import forms
from .models import HotelDetails , Roomtype , BookingDetails , Hotelowner

class HotelRegistrationForm(forms.ModelForm):
    class Meta:
        model = HotelDetails
        exclude = ['user_id','avg_rating','is_hoteluser']    # Exclude user field as it will be set automatically

class Hotelownerform(forms.ModelForm):
    class Meta:
        model = Hotelowner
        exclude = ['hotel_id']


class Roomtypeform(forms.ModelForm):
    class Meta:
        model = Roomtype
        fields = ['roomtype', 'description', 'capacity', 'price', 'photo']


class Bookingform(forms.ModelForm):
    class Meta:
        model =  BookingDetails
        exclude = ['booking_id','user','hotel','is_paid','is_advancepaid','room_type']
