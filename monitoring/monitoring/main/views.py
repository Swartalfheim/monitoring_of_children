from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home_page_view(request):
    return render(request, 'home.html')

def about_page_view(request):
    return render(request, 'about.html')

def register_page_view(request):
    return render(request, 'register.html')

def login_page_view(requset):
    return render(requset, 'login.html')

def dashboard_page_view(requset):
    return render(requset, 'dashboard.html')