from django.shortcuts import render
from home.models import Ebill


def index(request):
    frequencies = Ebill.get_call_frequencies()
    calls = Ebill.get_calls_per_day()
    cont = {'frequencies': frequencies, 'calls': calls}
    return render(request, 'home/index.html', cont)
