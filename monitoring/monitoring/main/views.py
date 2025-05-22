from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ditina
from .forms import DitinaForm

#@login_required
def dashboard_page_view(request):
    form_submitted = False
    if request.method == 'POST':
        form = DitinaForm(request.POST)
        form_submitted = True
        if form.is_valid():
            form.save()
            messages.success(request, 'Інформацію про дитину успішно додано!')
            return redirect('dashboard')
    else:
        form = DitinaForm()

    dity_list = Ditina.objects.all()

    context = {
        'form': form,
        'dity_list': dity_list,
        'form_submitted': form_submitted,
    }
    return render(request, 'dashboard.html', context)

def home_page_view(request):
    return render(request, 'home.html')

def about_page_view(request):
    return render(request, 'about.html')

def register_page_view(request):
    return render(request, 'register.html')

def login_page_view(requset):
    return render(requset, 'login.html')
