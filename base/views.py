from django.shortcuts import render

# Create your views here.

rooms = [
    {'id':1, 'name':'cook with me'},
    {'id':2, 'name':'recept'},
    {'id':3, 'name':'chefs'},
]
def home(request):
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request):
    return render(request, 'base/room.html')