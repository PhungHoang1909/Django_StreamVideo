from django.shortcuts import render

# Create your views here.
# stream/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'stream/index.html')
