from django.contrib import admin
from .models import UserDetails

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','fullname', 'email', 'phone', 'username')
    list_filter = ('username',)
    search_fields = ('fullname', 'email', 'phone', 'username')
