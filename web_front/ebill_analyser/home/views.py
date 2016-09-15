from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    cont = {'param': 'This is a sample param'}
    return render(request, 'home/index.html', cont)
