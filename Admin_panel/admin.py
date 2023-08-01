from django.contrib import admin
from .models import Hotel_income


class Hotel_incomeAdmin(admin.ModelAdmin):
        list_display = ('id','hotel','total_bookings','total_paid', 'last_payment_date','pending_payment')
admin.site.register(Hotel_income,Hotel_incomeAdmin)




# Register your models here.
