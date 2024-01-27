from django.shortcuts import render

rooms = [
    {'id':1 , 'name':'heres a place to be happy','population':586},
    {'id':2 , 'name':'learning python','population':456},
    {'id':3 , 'name':'boardgame lovers','population':823},
]

def home(request):
    context = {'rooms':rooms}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=None
    for specific_room in rooms:
        if specific_room['id'] == int(pk):
            room=specific_room
    context = {'room':room}
    return render (request,'base/room.html',context)



# Create your views here.
