from .models import Author, Book, Library, Librarian

Library.objects.get(name=library_name)
books.all()

Library.objects.prefetch_related('library')

Librarian.objects.prefetch_related('librarian')
