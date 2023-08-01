from django.shortcuts import render,redirect,HttpResponse
from Hotel_manage.models import HotelDetails 
from User_manage.models import UserDetails
from Admin_panel.models import Hotel_income
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from datetime import date

# from



def Adminpanel_view(request):
    if request.user.is_superuser:
        
        list_hotels = HotelDetails.objects.filter(is_registerd = True,is_confirmed = False,is_active = True)

    else:
        return redirect('home')

    return render(request,'admin_panel/admin_panel.html',{'hotels':list_hotels})


# Accepted hotel view 

def Hotelaccept(request,hotel_id):

    try:
        hotel = HotelDetails.objects.get(id=hotel_id)
        hotel.is_confirmed = True
        hotel.save()
        
        mail_subject = "Your hotel Regisration Confirmed"
        message = render_to_string("hotel_account/hotel_accept_email.html",{
            'hotel':hotel,
        })
        to_email = hotel.hotel_email
        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.send()

    except Exception as e:
        messages.error(request, f"An error occurred during registration: {str(e)}")
        return HttpResponse('Something went wrong')


    return redirect('adminpanel')


# Rejected hotel view deleteing rejecte hotel 

def Hotelreject(request,hotel_id):

    try:
        hotel = HotelDetails.objects.get(id=hotel_id)

        mail_subject = "Your hotel Regisration Rejected"
        message = render_to_string("hotel_account/hotel_reject_email.html",{
            'hotel':hotel,
        })
        to_email = hotel.hotel_email
        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.send()



        hotel.delete()

    except:
        return HttpResponse('Something went wrong')
    
    return redirect('adminpanel')



def Admin_hotel_view(request):
    if request.user.is_superuser:

        list_hotels = HotelDetails.objects.filter(is_registerd = True,is_active = True)
    
    else:

        return redirect('home')

    return render(request,'admin_panel/admin_hotel.html',{'hotels':list_hotels})



def Admin_user_view(request):

    if request.user.is_superuser:

        list_users = UserDetails.objects.filter(is_active = True)

    else:

        return redirect('home')

    return render(request,'admin_panel/admin_users.html',{'users':list_users})




def Admin_hotel_payment_view(request):
    if request.user.is_superuser:

        list_hotels = Hotel_income.objects.all()

    else:

        return redirect('home')

    return render(request,'admin_panel/admin_hotel_payment.html',{'hotels':list_hotels})
# Create your views here.
