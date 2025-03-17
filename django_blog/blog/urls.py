from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    ]
