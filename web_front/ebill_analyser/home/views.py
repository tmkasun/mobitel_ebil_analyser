from django.shortcuts import render
from home.models import Ebill

def index(request):
    frequencies = Ebill.get_call_frequencies()
    cont = {'frequencies': frequencies}
    return render(request, 'home/index.html', cont)
