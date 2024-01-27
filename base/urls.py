from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='homeurl'),
    path('room/<str:pk>/',views.room,name='roomurl'),

]