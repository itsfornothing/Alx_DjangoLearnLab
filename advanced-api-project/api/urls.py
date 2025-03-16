from django.urls import path
from .views import *

urlpatterns = [
    path('books/', BookListView.as_view(), name='list_books'),
    path('books/<str:note_id>', BookDetailView.as_view(), name='detail_books'),
    path('books/create', BookCreate.as_view(), name='all_books'),
    path('books/update/<int:book_id>', BookUpdate.as_view(), name='all_books'),
    path('books/delete', BookDelete.as_view(), name='all_books'),
    
]
