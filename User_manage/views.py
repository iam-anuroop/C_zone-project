from django.shortcuts import render, redirect ,get_object_or_404 ,HttpResponse 
from .registration_form import UserRegistrationForm
from .models import UserDetails
from Hotel_manage.models import BookingDetails , PaymentDetails
from django.contrib import messages
import re
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode 
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login,logout
from datetime import date
from django.contrib.auth.decorators import login_required

# for invoice download 
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings




#user registration
def register(request):
    if request.method == 'POST':
        
        form = UserRegistrationForm(request.POST)
        uname = request.POST.get('username')
        if UserDetails.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists')
        else:
            if form.is_valid():
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                confirmpassword = form.cleaned_data['confirmpassword']

                # 1. Check if email already exists
                if UserDetails.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                # 2. Phone number validation
                elif not re.match(r'^[0-9]{10}$', phone):
                    messages.error(request, 'Invalid phone number')
                # 3. Check if username already exists and validate username format
                elif not re.match(r'^[A-Za-z]', username):
                    messages.error(request, 'Username must start with an alphabet')
                elif len(username) < 5:
                    messages.error(request, 'Username must contain at least 5 characters')
                # 4. Validate password and confirm password
                elif password != confirmpassword:
                    messages.error(request, 'Password does not match')
                elif len(password) < 5:
                    messages.error(request, 'Password must be at least 5 characters long')
                else:
                    try:
                        fullname = form.cleaned_data['fullname']
                        user = UserDetails.objects.create_user(fullname=fullname, email=email, phone=phone, username=username, password=password)
                        current_site = get_current_site(request)
                        mail_subject = "Please activate your account"
                        message = render_to_string("account/email_verify.html", {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': default_token_generator.make_token(user),
                        })
                        to_email = email
                        send_mail = EmailMessage(mail_subject, message, to=[to_email])
                        send_mail.send()
                        user.save()
                        return redirect('emailnotification')
                    except Exception as e:
                        messages.error(request, f"An error occurred during registration: {str(e)}")
            else:
                messages.error(request, "Invalid form data")
    else:
        form = UserRegistrationForm()
    return render(request, 'account/registration.html', {'form': form})



# email notification
def emailnotification(request):


    return render(request,'account/emailnotification.html')



#email activation
def activate(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = UserDetails.objects.get(pk=uid)
    try:
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active=True
            user.save()
            messages.success(request, 'Account activated successfully you can now login')
            return redirect('login')
        else:
            messages.error(request, 'Invalid activation link')
    except :
        messages.error(request, 'Invalid activation link')
    return redirect('login')




# login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None :
            if user.is_active == True:
                try:
                    login(request, user)
                    request.session['pk'] = user.pk
                    messages.success(request, 'Login successful')
                    return redirect('home')
                except Exception as e:
                    messages.error(request, f"An error occurred during login: {str(e)}")
            else:
                 messages.error(request,'you need to verify your email,by clicking the verification link') 
        else:
            try:
                noactive_user = UserDetails.objects.get(email=email)
                print(noactive_user)

                if noactive_user:
                    if noactive_user.is_active == False:
                        messages.error(request, 'Activate your email')
                    else:
                        messages.error(request, 'Invalid username or password')
                else:
                    messages.error(request, 'This Email doesnt have an account please register')
            except:
                messages.error(request,'This Email doesnt have an account please register')
    return render(request, 'account/login.html')



# logout
def logout_view(request):
    logout(request)
    # request.session.flush()
    return redirect('registration')


# forgot password first page for email
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = UserDetails.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = "Password/username Reset"
            message = render_to_string("account/password_resetemail.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()
            return render(request, 'account/emailnotification.html')
        except UserDetails.DoesNotExist:
            messages.error(request, 'Invalid email address')
    return render(request, 'account/forgotpassword.html')


# reset password
def resetpasswordorusername(request, uidb64, token):
    if request.method=='POST':
        newvalue=request.POST['password']
        confirmnewvalue=request.POST['confirmpassword']
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserDetails.objects.get(pk=uid)
        try:
            if user is not None and default_token_generator.check_token(user, token):
                if newvalue == confirmnewvalue and len(newvalue)>4:
                    user.mail_activation=True
                    user.set_password(newvalue)
                    user.save()
                    messages.success(request, 'Password changed successfully')
                    return redirect('emailnotification')
                else:
                    if newvalue != confirmnewvalue:
                        messages.error(request,'password not matching')
                    else:
                        messages.error(request,'password length must atleast 5 characters')
            else:
                messages.error(request, 'Invalid activation link')
        except :
            messages.error(request, 'Invalid activation link')
    return render(request,'account/resetpassword.html')



# bookings with out payment to show on kart
@login_required(login_url='login')
def Your_bookings(request):

    try:

        your_book = BookingDetails.objects.filter(user = request.user,is_paid =False)
        booking = BookingDetails.objects.filter(user = request.user,is_paid =True)

        today_date = date.today()
        booked_room_ids = BookingDetails.objects.filter(check_out_date__gt = today_date,is_paid = True).values_list("room_type_id",flat=True)


        return render(request,'pages/your_bookings.html',{'books':your_book,'booking':booking, 'booked_room_ids':booked_room_ids})
    except:
        return HttpResponse('something went wrong')




# invoice data generator
# def generate_invoice_data(booking):
#     hi='hi'
#     return {'hi':hi}

# invoice download
def invoice_view(request, booking_id):
    booking = get_object_or_404(BookingDetails, id=booking_id)
    # invoice_data = generate_invoice_data(booking)
    temp_data = get_object_or_404(PaymentDetails,booking=booking)

    template = get_template('invoice/invoice.html')
    context = {'data': booking,'amount':temp_data.amount_paid}
    rendered_template = template.render(context)

    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(rendered_template.encode('UTF-8')), response)

    if not pdf.err:
        # Set the response content type as 'application/pdf'
        response = HttpResponse(response.getvalue(), content_type='application/pdf')

        # Set the Content-Disposition header to force the browser to download the file
        response['Content-Disposition'] = f'attachment; filename="c_zone_invoice_{booking.id}.pdf"'
        return response
    else:
        # Handle the case when there is an error while generating the PDF
        return HttpResponse('Error generating PDF', status=500)




#user profile crud operation for updating and deleting their account 
@login_required(login_url='login')
def Profileupdate(request):
    user = request.user
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        # email activation mail for verify the mail ath cheyyanam
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if not re.match(r'^[A-Za-z]', username):
            messages.error(request, 'Username must start with an alphabet')
        elif len(username) < 5:
            messages.error(request, 'Username must contain at least 5 characters')
        elif not re.match(r'^[0-9]{10}$', phone):
            messages.error(request, 'Invalid phone number')
        elif email != user.email:
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string("account/email_verify.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()
        else :
            user.fullname = fullname
            user.username = username
            user.email = email
            user.phone = phone
            user.save()
    return render(request,'account/userprofile.html',{'user':user})




# delete user account 
def Userdelete(request):
    if request.user:
        user = request.user
        user.delete()
        return redirect('home')
    return render(request,'account/userprofile.html')



# Create your views here.