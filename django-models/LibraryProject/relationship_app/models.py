from django.db import models

# Create your models here.

class Author(models.Model):
    title = models.CharField(max_length=200)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')


class Library(models.Model):
    title = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='library')


class Librarian(models.Model):
    title = models.CharField(max_length=200)
    library = models.OneToOneField(Library, related_name='librarian')