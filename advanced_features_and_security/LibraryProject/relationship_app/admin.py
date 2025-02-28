from django.contrib import admin
from .models import Author, Book, Library, Librarian, CustomUser

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'admin', 'staff', "date_of_birth", "profile_photo"]

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(CustomUser)
