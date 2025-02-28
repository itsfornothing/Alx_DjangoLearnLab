from django.contrib import admin
from .models import Author, Book, Library, Librarian, CustomUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(CustomUser)

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'admin', 'staff', "date_of_birth", "profile_photo"]


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
