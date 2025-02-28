from django.contrib import admin
from .models import Book, CustomUser
# Register your models here.
  
admin.site.register(Book)
admin.site.register(CustomUser)



class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'publication_year')
  search_fields = ('title', 'author')
  list_filter = ('publication_year')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'admin', 'staff', "date_of_birth", "profile_photo")
    search_fields = ('username', 'email')
    list_filter = ('username')
