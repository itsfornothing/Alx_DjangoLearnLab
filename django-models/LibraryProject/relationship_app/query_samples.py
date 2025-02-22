from .models import Author, Book, Library, Librarian

Author.objects.prefetch_related('books')

Library.objects.prefetch_related('library')

Librarian.objects.prefetch_related('librarian')
