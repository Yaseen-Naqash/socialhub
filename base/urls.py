from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='homeurl'),
    path('room/<str:pk>/',views.room,name='roomurl'),
    path('create-room/',views.createRoom,name='createroomurl'),
    path('room-update/<str:pk>/',views.updateRoom,name='updateroomurl'),
    path('delete/<str:pk>/',views.deleteRoom,name='deleteurl'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='deleteMessageurl'),
    path('edit-message/<str:pk>/',views.editMessage,name='editmessageurl'),
    path('login/',views.loginPage,name='loginurl'),
    path('logout/',views.logOut,name='logouturl'),
    path('register/',views.registerPage,name='registerurl'),
    path('profile/<str:pk>/',views.profile,name='profileurl'),
    path('edit-profile/',views.editUser,name='edituserurl'),
    path('topics/',views.topics,name='topicsurl'),
    path('activity/',views.activity,name='activityurl'),


]