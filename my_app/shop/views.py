from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')


def room(request):
    return HttpResponse('room.html')

def loginPage(request):
    return render(request, 'shop/login.html')


def indexPage(request):
    return render(request, 'shop/index.html')
