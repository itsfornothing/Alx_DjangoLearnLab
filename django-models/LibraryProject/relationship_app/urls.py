from django.contrib import admin
from django.urls import path

from .views import list_books, LibraryDetailView

urlpatterns = [
    path('', list_books, name='list_books'),
    path('library/', list_books.as_view(), name='library_detail'),
    ]
