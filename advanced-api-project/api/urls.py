from django.urls import path, include
from .views import *

urlpatterns = [
    path('books/', BookList.as_view(), name='all_books'),
    path('books/<int:book_id>', BookDetail.as_view(), name='all_books'),
    path('books/create', BookCreate.as_view(), name='all_books'),
    path('books/update/<int:book_id>', BookUpdate.as_view(), name='all_books'),
    path('books/delete', BookDelete.as_view(), name='all_books'),
    
]
