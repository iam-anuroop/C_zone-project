from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('rooms/',views.Rooms_view,name='rooms'),
    path('search/',views.Searchotel,name='search'),
    path('filter/',views.Filter_room,name='filter'),
]