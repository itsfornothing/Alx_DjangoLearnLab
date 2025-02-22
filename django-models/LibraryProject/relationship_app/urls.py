from django.contrib import admin
from django.urls import path

from relationship_app import views


urlpatterns = [
    path('', views.all_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetail.as_view(), name='library_detail'),
]

