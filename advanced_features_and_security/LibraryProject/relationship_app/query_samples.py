import django
import os

# Set up Django environment for standalone script execution
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# ✅ Query 1: Get all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)  # Uses the related_name 'books' from ForeignKey

# ✅ Query 2: List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()  # Uses the related_name 'libraries' from ManyToManyField

# ✅ Query 3: Retrieve the librarian for a library
def get_librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)  # Uses the related_name 'librarian' from OneToOneField

# Sample Usage
if __name__ == "__main__":
    print("Books by J.K. Rowling:", get_books_by_author("J.K. Rowling"))
    print("Books in Central Library:", get_books_in_library("Central Library"))
    print("Librarian of Central Library:", get_librarian_of_library("Central Library"))
