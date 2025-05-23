from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('about', views.about_page_view, name='about'),
    path('login', views.login_page_view, name='login'),
    path('register', views.register_page_view, name='register'),
    path('dashboard', views.dashboard_page_view, name='dashboard'),
    path('dashboard/edit/<int:ditina_id>/', views.edit_ditina_view, name='edit_ditina'),
    path('dashboard/delete/<int:ditina_id>/', views.delete_ditina_view, name='delete_ditina'),
]
