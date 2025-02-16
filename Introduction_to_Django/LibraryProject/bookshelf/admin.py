from django.contrib import admin
from .models import Book
# Register your models here.

class BookAdmin(admin.AdminModel):
  list_display = ('title', 'author', 'published_date')
  earch_fields = ('title', 'author')
  
admin.site.register(Book)

