from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
# Register your models here.
  
admin.site.register(Book)
admin.site.register(CustomUser, CustomUserAdmin)



class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'publication_year')
  search_fields = ('title', 'author')
  list_filter = ('publication_year')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'admin', 'staff', "date_of_birth", "profile_photo")
    search_fields = ('username', 'email')
    list_filter = ('username')

Editors, created = Group.objects.get_or_create(name ='Editors')
Viewers, created = Group.objects.get_or_create(name ='Viewers')
Admins, created = Group.objects.get_or_create(name ='Admins')

ct = ContentType.objects.get_for_model(Librarian)


Admins_permissions = [
    {'codename': 'can_view', 'name': 'Can View'},
    {'codename': 'can_delete', 'name': 'Can Delete'},
    {'codename': 'can_add', 'name': 'Can Add'},
    {'codename': 'can_edit', 'name': 'Can Edit'}
]

for perm in Admins_permissions:
    permission = Permission.objects.create(
        codename=perm['codename'],
        name=perm['name'],
        content_type=ct
    )
    Admins.permissions.add(permission)



Viewers_permissions = [
    {'codename': 'can_view', 'name': 'Can View'},
]

for perm in Admins_permissions:
    permission = Permission.objects.create(
        codename=perm['codename'],
        name=perm['name'],
        content_type=ct
    )
    Viewers.permissions.add(permission)


Editors_permissions = [
    {'codename': 'can_view', 'name': 'Can View'},
    {'codename': 'can_edit', 'name': 'Can Edit'}
]

for perm in Admins_permissions:
    permission = Permission.objects.create(
        codename=perm['codename'],
        name=perm['name'],
        content_type=ct
    )
    Editors.permissions.add(permission)
