from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Room ,Topic , Message
from .forms import RoomForm
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    pagename='loginpage'

    if request.user.is_authenticated:
        return redirect('homeurl')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        #try:
        #    user=User.objects.get(username=username)
        #except:
        #    messages.error(request,'user doesnt exist!')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('homeurl')
        else:
            messages.error(request,'username or password is incorrect')
    context={'pagename':pagename}
    return render(request,'base/login_register.html',context)

def logOut(requst):
    logout(requst)
    return redirect('homeurl')

def registerPage(request):
    form = UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username.lower()
            user.save()
            return redirect('loginurl')
        else:
            messages.error(request,'Your informations is invalid')

    pagename='registerpage'
    context={'pagename':pagename , 'form':form}
    return render(request,'base/login_register.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    recent_messages=Message.objects.filter(Q(room__topic__name__icontains=q))[:5]
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(description__icontains = q) |
                                Q(name__icontains = q))
    
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    context = {'topics':topics,'rooms':rooms,'rooms_count':rooms_count,'recent_messages':recent_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST' :
        newmessage=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('roomurl',pk=room.id)

    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render (request,'base/room.html',context)

@login_required(login_url='loginurl')
def createRoom(request):
    form = RoomForm()
    if (request.method=='POST'):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homeurl')

    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='loginurl')
def updateRoom(requst,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    #if requst.user != room.host:
    #    return HttpResponse("you are not allowed here")
    if (requst.method == 'POST'):
        form = RoomForm(requst.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('homeurl')

    context = {'form':form}
    return render(requst,'base/room_form.html',context)

@login_required(login_url='loginurl')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    #if request.user != room.host:
    #    return HttpResponse("you are not allowed here")
    if request.method=='POST':
        room.delete()
        return redirect('homeurl')
    context = {'obj':room.name}
    return render(request,'base/delete.html',context)

@login_required(login_url='loginurl')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    room=message.room
    if request.method=='POST':
        message.delete()
        return redirect('roomurl',pk=room.id)
    context = {'obj':message}
    return render(request,'base/delete.html',context)

@login_required(login_url='loginurl')
def editMessage(request,pk):
    message = Message.objects.get(id=pk)
    room = message.room
    if request.method=='POST':
        message.body=request.POST.get('body')
        message.save()
        return redirect('roomurl',pk=room.id)
    context = {'message':message}
    return render(request,'base/edit_message.html',context)

def profile(request,pk):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.all()
    user = User.objects.get(id=pk)
    rooms=Room.objects.filter(Q(topic__name__icontains=q)|Q(description__icontains=q)|Q(name__icontains=q),host=user)
    recent_messages=Message.objects.filter(user=user)[:5]
    context = {'user':user,'topics':topics,'rooms':rooms,'recent_messages':recent_messages}
    return render (request,'base/profile.html',context)
# Create your views here.
