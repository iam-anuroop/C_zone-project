from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .Hotel_form import HotelRegistrationForm  , Roomtypeform ,Bookingform,Hotelownerform
from django.contrib.auth.decorators import login_required
from User_manage.models import UserDetails
from .models import HotelDetails , Roomtype ,BookingDetails ,PaymentDetails,ReviewDetails
from Admin_panel.models import Hotel_income
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import os
import razorpay
from datetime import date
from django.db.models import Count,Avg
# Create your views here.


# hotel registration
@login_required(login_url='login')
def Hotelregister(request):
    if request.user == None:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = HotelRegistrationForm(request.POST,request.FILES)
            password = request.POST.get('password')
            email = request.POST.get('hotel_email')
            confirm_password = request.POST.get('confirmpassword')
            print(confirm_password)
            if form.is_valid():
                if password == confirm_password:
                    hotel = form.save(commit=False)
                    user = request.user
                    user.is_hoteluser = True
                    hotel.user_id = request.user
                    hotel.set_password(password)
                    user.save()
                    hotel.save()
                    request.session['hotel_id']=hotel.id


                    try:
                        current_site = get_current_site(request)
                        mail_subject = "Please activate your account"
                        message = render_to_string("hotel_account/email_verify.html", {
                            'user': request.user,
                            # 'hotel':hotel,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(hotel.pk)),
                            'token': default_token_generator.make_token(hotel),
                        })
                        to_email = email
                        send_mail = EmailMessage(mail_subject, message, to=[to_email])
                        send_mail.send()

                        return redirect('hotelowner_reg')
                    except Exception as e:
                        messages.error(request, f"An error occurred during registration: {str(e)}")

                    # logout(request) #making the user logout 

                    return redirect('hotelowner_reg')
                else:
                    messages.error(request,'password not matching')

            else:
                print(form.errors)
                messages.error(request,'invalid form')
        else:
            form= HotelRegistrationForm()
            
    return render(request,'hotel_account/hotel_reg.html',{'form': form,})


# hotel regostration second part owner details 
def ownerregistration(request):
    hotel_id = request.session.get('hotel_id')
    hotel_email = request.session.get('hotel_email')
    try:
        hotel = HotelDetails.objects.get(id=hotel_id)
        if request.method == 'POST':
            form = Hotelownerform(request.POST, request.FILES)
            if form.is_valid():
                owner=form.save(commit=False)
                hotel.is_registerd = True
                hotel.save()
                owner.hotel_id = hotel
                owner.save()
                return redirect('emailnotification')  
        else:
            form = Hotelownerform()
    except:
        try:
            hotel = HotelDetails.objects.get(hotel_email=hotel_email)
            hotel.delete()
            messages.error(request,'You need to register once again')
            return redirect('hotelregistration')
        except:
            messages.error(request,'You need to register once again')
            return redirect('hotelregistration')

    form = Hotelownerform()
    return render(request,'hotel_account/hotel_owner.html',{'form':form})


#email activation for hotel account

def activatehotel(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    hotel = HotelDetails.objects.get(pk=uid)
    print(uid,hotel,token)
    try:
        if hotel is not None and default_token_generator.check_token(hotel, token):
            hotel.is_active=True
            hotel.save()
            messages.success(request, 'Account activated successfully you can now login')
            return redirect('hotellogin')
        else:
            messages.error(request, 'Invalid activation link')
    except :
        messages.error(request, 'Invalid activation link')
    return redirect('hotellogin')




# hotel login
@login_required(login_url='login')
def Hotellogin(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        print(email, password)
        try:
            hotel = HotelDetails.objects.get(hotel_email=email)
            print(hotel)
            if check_password(password, hotel.password) and hotel.is_active==True and hotel.is_registerd ==True:  # Manually check the password
                print('Password matched!')
                hotel.is_logined = True
                hotel.save()
                request.session['hotel_id'] = hotel.id
                return redirect('hotelhome')
            else:
                # is registered
                if hotel.is_registerd == False:
                    messages.error(request,'you need to add owner details')
                    request.session['hotel_email']=hotel.hotel_email
                    return redirect('hotelowner_reg')
                # hotelactiavte
                elif hotel.is_active == False:
                    messages.error(request,'Verify you account through the verification link')
                else:
                    messages.error(request,'Incorrect password')
                
                print('Invalid password.')
                return redirect('hotellogin')
        except HotelDetails.DoesNotExist:
            # print(hotel)

            print('User not found.')
            
    return render(request, 'hotel_account/hotel_login.html')




# hotelhome
def Hotelhome(request):
    hotel_id = request.session.get('hotel_id')

    if hotel_id:
        try:
            hotel = HotelDetails.objects.get(id=hotel_id)
            if hotel.is_logined:
                paid_bookings = BookingDetails.objects.filter(hotel = hotel_id,is_paid = True)
                bookings = BookingDetails.objects.filter(hotel = hotel_id,is_paid = False)
                return render(request, 'hotel_account/hotel_home.html',{'paid_bookings':paid_bookings , 'bookings':bookings  })
            else:
                messages.error(request, 'You need to log in first')
                return redirect('hotellogin')
        except HotelDetails.DoesNotExist:
            messages.error(request, 'Invalid hotel details')
            return redirect('hotellogin')
    else:
        messages.error(request, 'You need to log in first')
        return redirect('hotellogin')





# logout hotel
def Hotellogout(request):
    hotel_id = request.session.get('hotel_id')
    if hotel_id is not None:
        hotel = get_object_or_404(HotelDetails, id=hotel_id)
        hotel.is_logined = False
        hotel.save()
    else:
        pass    
    # Always redirect to the hotel login page after logout.
    return redirect('hotellogin')

# room type 
@login_required(login_url='login')
def Roomtype_view(request):
    hotel_id = request.session.get('hotel_id')
    if hotel_id is None:
        messages.error(request, 'You need to login first')
        return redirect('hotellogin')

    try:
        hotel = HotelDetails.objects.get(id=hotel_id, is_logined=True)
    except HotelDetails.DoesNotExist:
        messages.error(request, 'You need to login first')
        return redirect('hotellogin')

    if request.method == 'POST':
        form = Roomtypeform(request.POST, request.FILES)

        if form.is_valid():
            room = form.save(commit=False)
            room.hotel_id = hotel
            room.check_out_date = date.today()
            room.save()
            messages.success(request, 'Room type added successfully.')
            return redirect('roomtypeupdate')
        else:
            messages.error(request, 'Form is not valid. Please check the data you entered.')
    else:
        form = Roomtypeform()

    datas = Roomtype.objects.filter(hotel_id=hotel_id)
    return render(request, 'hotel_account/roomtype.html', {'datas': datas, 'form': form})



# hotel_rooms and price page view
@login_required(login_url='login')
def Hotel_rooms_view(request,hotel_id):
    hotel = get_object_or_404(HotelDetails, id=hotel_id)
    rooms = Roomtype.objects.filter(hotel_id=hotel_id)

    today_date = date.today()

    booked_room_ids = BookingDetails.objects.filter(check_out_date__gt = today_date,is_paid = True).values_list("room_type_id",flat=True)
    if request.method == 'POST':
        try:
            review = request.POST.get('review')  # Get the review from the form
            rating = request.POST.get('rating-value')
            print(review,rating)
            if rating == "" or review == "":
                print('hiiii')
                messages.error(request,'please provide rating and review')
            else:
                ReviewDetails.objects.create(
                    hotel = hotel,
                    user = request.user,
                    comment = review,
                    rating = rating
                )
            new_avg_rating = ReviewDetails.objects.filter(hotel=hotel).aggregate(Avg('rating'))['rating__avg']
            hotel.avg_rating = new_avg_rating
            hotel.save()
        except Exception as e:
            print(f'Error: {str(e)}')
            

    is_user_booked = BookingDetails.objects.filter(hotel=hotel, user=request.user).exists()
    hotel_review = ReviewDetails.objects.filter(hotel=hotel)

    context = {
        'rooms':rooms ,
          'hotel':hotel ,
          'booked_room_ids':booked_room_ids,
          'is_user_booked':is_user_booked,
          'hotel_review':hotel_review,
          }

    return render(request,'pages/hotel_rooms.html',context)




# booking form view
@login_required(login_url='login')
def hotel_book(request,hotel_id,room_id):
    hotel = get_object_or_404(HotelDetails, id=hotel_id)
    room = get_object_or_404(Roomtype, id=room_id)
    print(hotel,room)
    if request.method == 'POST':
        capacity=request.POST.get('num_of_guests')
        form =Bookingform(request.POST,request.FILES)

        if int(capacity) > int(room.capacity):
            messages.error(request,'Guests are more than capacity')
        # Save the booking data to the database
        elif form.is_valid():
            booking = form.save(commit=False)
            booking.hotel = hotel
            booking.room_type = room
            booking.user = request.user  # Assuming the user is authenticated
            if booking.check_in_date > date.today() and booking.check_in_date < booking.check_out_date:
                booking.save()
                return redirect('payment',booking_id=booking.id,room_id=room.id)
            else:
                messages.error(request,'Choose a proper date')
            
        else:
            print(form.errors)
        # booking.save()

    # form = Bookingform()
    return render(request,'pages/hotelbook.html',{'hotel':hotel,'room':room})



from django.conf import settings
# payment metho view 
def Payment_view (request,booking_id=0,room_id=0):
    print(booking_id)
    print(room_id)
    booking = get_object_or_404(BookingDetails,id=booking_id)
    room = get_object_or_404(Roomtype, id=room_id)


    grand_total = 0
    total = room.price
    
    tax = (2 * total)/100
    grand_total = total + tax

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    payment = client.order.create({'amount':int(grand_total)*100 , 'currency':'INR' , 'payment_capture':1 })
    key_id = settings.RAZOR_KEY_ID

   

    context = {
        'room':room,
        'booking':booking,
        'grand_total':grand_total,
        'payment':payment,
        'booking_id':booking_id,
        'room_id':room_id
    }

    return render(request,'pages/payment.html',context)



def success(request):
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    booking_id = request.GET.get('booking_id')
    room_id = request.GET.get('room_id')
    booking = get_object_or_404(BookingDetails,id=booking_id)
    print(room_id,booking_id,razorpay_payment_id)


    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


    try:
        payment = client.payment.fetch(razorpay_payment_id)

        amount_paid = payment['amount'] / 100  # Amount is in paise, so convert to rupees
        razor_pay_status = payment['status']
        print(razor_pay_status,amount_paid)

        PaymentDetails.objects.create(
            razor_payment_id=razorpay_payment_id,
            user=booking.user,  # Assuming the booking has a ForeignKey to the user
            hotel=booking.hotel,
            booking_id = booking.id,
            amount_paid=amount_paid,
            razor_pay_status=razor_pay_status
        )
        booking.is_paid = True
        booking.save()

        mail_subject = "Your booking is confirmed"
        message = render_to_string("pages/booking_success_email.html",{
            'user':booking.user,
            'booking':booking,
            'hotel':booking.hotel,
        })
        to_email = booking.user.email
        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.send()

        room = Roomtype.objects.get(id = room_id)
        room.check_out_date = booking.check_out_date
        room.save()

        if Hotel_income.objects.filter(hotel=booking.hotel).exists():
            try:
                hotel_pay = get_object_or_404(Hotel_income,hotel=booking.hotel)
                hotel_pay.total_bookings = int(hotel_pay.total_bookings) + int(1)
                hotel_pay.pending_payment = float(hotel_pay.pending_payment) + float(amount_paid)
                hotel_pay.save()
            except Exception as e:
                return HttpResponse(f'Error: {str(e)}')

        else:
            Hotel_income.objects.create(
                hotel = booking.hotel,
                total_bookings= 1 ,
                pending_payment = amount_paid,
                )

        

    except razorpay.errors.BadRequestError as e:
        return HttpResponse(f'Error: {str(e)}')


    
    return render(request,'pages/success_payment.html')


    # hotel_name = form.cleaned_data['hotel_name']
    # hotel_email = form.cleaned_data['hotel_email']
    # hotel_registration_number = form.cleaned_data['hotel_registration_number']
    # hotel_contact_number = form.cleaned_data['hotel_contact_number']
    # hotel_address = form.cleaned_data['hotel_address']
    # hotel_location = form.cleaned_data['hotel_location']
    # district = form.cleaned_data['district']
    # state = form.cleaned_data['state']
    # city = form.cleaned_data['city']
    # pin_code = form.cleaned_data['pin_code']
    # hotel_owner_name = form.cleaned_data['hotel_owner_name']
    # hotel_owner_email = form.cleaned_data['hotel_owner_email']
    # hotel_owner_contact = form.cleaned_data['hotel_owner_contact']
    # hotel_owner_address = form.cleaned_data['hotel_owner_address']

     # if request.method == 'POST':
    #     print('jjjjjjj')
    #     razor_payment_id = request.POST.get('razor_payment_id')  

    #     payment_details = PaymentDetails.objects.create(
    #         razor_payment_id=razor_payment_id,
    #         user=request.user,
    #         hotel=booking.hotel,
    #         amount_paid=str(grand_total),
    #         # razor_pay_status='Success',  # You can set this based on your payment response
    #     )
    #     payment_details.save()

