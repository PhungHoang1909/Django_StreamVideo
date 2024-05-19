from django.shortcuts import render

# Create your views here.

def main_view(request):
    context = {}

    return render(request, 'streamapp/base.html', context=context)