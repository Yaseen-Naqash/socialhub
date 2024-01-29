from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='homeurl'),
    path('room/<str:pk>/',views.room,name='roomurl'),
    path('create-room/',views.createRoom,name='createroomurl'),
    path('room-update/<str:pk>/',views.updateRoom,name='updateroomurl'),
    path('delete/<str:pk>/',views.deleteRoom,name='deleteurl'),


]