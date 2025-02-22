from .models import Author, Book, Library, Librarian

books = Library.objects.get(name=library_name)
books.all()

author = Author.objects.get(name=author_name)

Book.objects.filter(author=author)
                   
Librarian.objects.prefetch_related('librarian')
