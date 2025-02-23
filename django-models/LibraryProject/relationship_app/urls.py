from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import SignUpView
import views.register
from .admin_view import Admin

from .views import list_books, LibraryDetailView, admin_view, librarian_view, member_view

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"),  
    path("logout/", LogoutView.as_view(template_name="registration/logged_out.html"), name="logout"),  
    path("signup/", SignUpView.as_view(), name="signup"),
    path('Admin/', Admin, name='admins'),
    path('Librarian/', librarian_view, name='librarians'),
    path('Member/', member_view, name='members'),
    path('books/add/', views.add_book, name='add_book'),
    path('add_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('edit_book/<int:pk>/', views.delete_book, name='delete_book'),
]
