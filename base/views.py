from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from .models import Room , Topic, Message
from .forms import RoomForm
# Create your views here.
from django.http import HttpResponse
#template inheritance
def loginPage(request):
    page = 'login'
    # restriction of user pages
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password is incorrect')
    context={'page':page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #get access to the form data
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,'Account created successfully')
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid form')
    context={'form':form}
    return render(request, 'base/login_register.html',context)
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q)|
        Q(name__icontains=q)
    )
    room_count=rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q) 
    )
    topics=Topic.objects.all()
    context = {'rooms': rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request, 'base/home.html', context)
def room(request,id):
    room= Room.objects.get(id=id)
    room_messages=Message.objects.filter(room=room).order_by('-created')
    participant_s = room.participants.all()


    #adding comment 
    if request.method=='POST':
        romessage = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        #check if user is a participant
        room.participants.add(request.user)
        romessage.save()
        return redirect('room',id=id)
    context = {'room': room,'comments':room_messages,'participants':participant_s}
    return render(request, 'base/room.html',context)

def userProfile(request,id):
    user=User.objects.get(id=id)
    rooms=user.room_set.all()
    rooms_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'topics':topics,'room_messages':rooms_messages}
    return render(request, 'base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()

    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,id):
    room=Room.objects.get(id=id)
    form=RoomForm(instance=room)
    # restriction of user pages
    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room')

    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html',context)
    
@login_required(login_url='login')
def deleteRoom(request,id):
    room=Room.objects.get(id=id)
    # restriction of user pages
    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room')

    if request.method=='POST':
        room.delete()
        return redirect('home')
    context={'obj':room}
    return render(request, 'base/delete.html',context)

@login_required(login_url='login')
def deleteMessage(request,id):
    message=Message.objects.get(id=id)
    # restriction of user pages
    if request.user != message.user:
        return HttpResponse('You are not allowed to edit this room')

    if request.method=='POST':
        message.delete()
        return redirect('home')
    context={'obj':message}
    return render(request, 'base/delete.html',context)