from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Cook with me'},
#     {'id': 2, 'name': 'Recept'},
#     {'id': 3, 'name': 'Chefs'},
# ]


def home(request):
    r = request.GET.get('r') if request.GET.get('r') != None else ''
    rooms = Room.objects.filter(topic__name__icontains=r)

    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

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

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You do not have permission to delet this!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'object': room})
