from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import SignUpView
import views.register

from .views import list_books, LibraryDetailView

urlpatterns = [
    path('', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', RegisterView.as_view(), name='signup'), 
