from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from User_manage.models import UserDetails
import uuid




class HotelManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create a new HotelDetails instance
        hotel = self.model(email=self.normalize_email(email), **extra_fields)
        hotel.set_password(password)
        hotel.save(using=self._db)
        return hotel

# model for creating hotels 

class HotelDetails(AbstractBaseUser):
    user_id = models.ForeignKey(UserDetails, on_delete=models.SET_NULL,null=True)
    hotel_name = models.CharField(max_length=255)
    hotel_email = models.EmailField(unique=True,null=False)
    hotel_registration_number = models.CharField(max_length=255)
    hotel_contact_number = models.CharField(max_length=20)
    hotel_address = models.CharField(max_length=255)
    hotel_location = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)
    hotel_profile = models.ImageField(upload_to='hotel_profile/')
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1,null=True,default=0)



    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_logined = models.BooleanField(default=False)
    is_registerd = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)


    USERNAME_FIELD = 'hotel_email'

    objects = HotelManager()


    def __str__(self):
        return self.hotel_name



# Bankaccounts details 



# Hotelowner details 
class Hotelowner(models.Model):
    hotel_id = models.ForeignKey(HotelDetails,on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=255)
    owner_email = models.EmailField()
    owner_contact = models.CharField(max_length=20)
    owner_address = models.CharField(max_length=255)
    id_card = models.ImageField(upload_to='hotelowner_idcard/')


    def __str__(self):
        return self.owner_name



# hotel booking details of user 
class Roomtype(models.Model):
    hotel_id = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
    roomtype = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='room_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    check_out_date = models.DateField(null=True, blank=True)




    def __str__(self):
        return self.roomtype
    
    # def check_date(self):
    #     today = timezone.now().date()
    #     if self.check_out_date is not None:
    #         if self.check_out_date > today:
    #             self.is_reserved = False
    #         else:
    #             self.is_reserved = True
    #     self.save()
    #     return self.check_out_date > today




# booking details table
class BookingDetails(models.Model):
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_type = models.ForeignKey(Roomtype,on_delete=models.SET_NULL,null=True)
    num_of_guests = models.IntegerField()
    special_requests = models.TextField()
    name = models.CharField(max_length=100)
    id_card = models.ImageField(upload_to='roomuser_idcard/')


    is_paid = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.booking_id)



# payment ...details 
class PaymentDetails(models.Model):
    razor_payment_id = models.CharField(max_length=255)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
    booking = models.ForeignKey(BookingDetails,on_delete=models.CASCADE)
    amount_paid = models.CharField(max_length=100) # this is the total amount
    razor_pay_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.razor_payment_id)





# review details
class ReviewDetails(models.Model):
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # Rating out of 5, e.g., 4.5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.fullname


