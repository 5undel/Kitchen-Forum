from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, TopicRoom
# Create your views here.

# Function for login method
def startpage(request):

    context = {}
    return render(request, 'base/startpage.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')
    context = {'page': page}
    return render(request, 'base/reg_login.html', context)

# Function for logout method


def logoutUser(request):
    logout(request)
    return redirect('home')

# Function for registration method


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ann error occurred during registration.')
    return render(request, 'base/reg_login.html', {'form': form})

# Create funtions to get rooms link in home page


def home(request):
    r = request.GET.get('r') if request.GET.get('r') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=r) |
        Q(name__icontains=r) |
        Q(description__icontains=r)
    )
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)

# Function in the rooms to se messages, users in the room


def room(request, pk):
    room = Room.objects.get(id=pk)
    roommessages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    topics = Topic.objects.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'roommessages': roommessages,
               'participants': participants, 'topics': topics}
    return render(request, 'base/room.html', context)

# In userpage to see which room they are in


def userPage(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    roommessages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'roommessages': roommessages, 'topics': topics}
    return render(request, 'base/mypage.html', context)

# functions to create room, User have to be login to create it


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


# functions to create topic, User have to be login to create it
@login_required(login_url='login')
def createTopic(request):
    form = TopicRoom()

    if request.method == 'POST':
        form = TopicRoom(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/topic_form.html', context)

# functions to update a room, User have to me login to create it


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You do not have permission to change!!')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# functions to delete a room, User have to me login to create it


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You do not have permission to delet this!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object': room})

# functions to delete a message, User have to me login to create it


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You do not have permission to delet this!!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object': message})
