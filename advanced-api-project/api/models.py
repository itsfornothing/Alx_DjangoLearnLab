from django.db import models

# this modelis used to store author names
class Author(models.Model):
    name = models.CharField(max_length=100)


# this modelis used to store books dtails
class Book(models.Model):
    title = models.CharField(max_length=124)
    publication_year = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)