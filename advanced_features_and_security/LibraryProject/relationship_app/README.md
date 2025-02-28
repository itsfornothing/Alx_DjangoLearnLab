Managing Permissions and Groups in Django

Overview
This document outlines how to implement and manage permissions and groups in Django to control access to different parts of the application securely.

Step 1: Define Custom Permissions in Models
To define custom permissions, modify the Meta class of the model:

from django.db import models
from django.contrib.auth.models import User

class MyModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        permissions = [
            ("can_view", "Can view records"),
            ("can_create", "Can create records"),
            ("can_edit", "Can edit records"),
            ("can_delete", "Can delete records"),
        ]


Key Points:
✔ The permissions list defines custom permissions.
✔ Django automatically adds default add, change, delete, and view permissions.
✔ These permissions will appear in the Django admin panel under user permissions.

Step 2: Create and Configure Groups
To set up user groups and assign permissions:

Using Django Admin Panel:
Go to Admin Panel (/admin/).
Navigate to "Groups" and create:
Admins
Editors
Viewers
Assign permissions to each group:
Admins: can_view, can_create, can_edit, can_delete
Editors: can_view, can_create, can_edit
Viewers: can_view
Using Django Shell:
Alternatively, configure groups via shell:

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from myapp.models import MyModel

content_type = ContentType.objects.get_for_model(MyModel)

# Create groups
admins = Group.objects.create(name="Admins")
editors = Group.objects.create(name="Editors")
viewers = Group.objects.create(name="Viewers")

# Assign permissions
permissions = Permission.objects.filter(content_type=content_type)
admins.permissions.set(permissions)
editors.permissions.set(permissions.exclude(codename="can_delete"))
viewers.permissions.set(permissions.filter(codename="can_view"))


Step 3: Enforce Permissions in Views
Use Django's @permission_required decorator to enforce access control.

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('myapp.can_edit', raise_exception=True)
def edit_view(request):
    return render(request, 'myapp/edit_page.html')

@permission_required('myapp.can_create', raise_exception=True)
def create_view(request):
    return render(request, 'myapp/create_page.html')

@permission_required('myapp.can_view', raise_exception=True)
def view_page(request):
    return render(request, 'myapp/view_page.html')

Key Points:
✔ Users without permission will receive a 403 Forbidden error.
✔ raise_exception=True ensures unauthorized users get a permission error instead of redirecting to login.
✔ Django also provides user.has_perm('myapp.can_edit') for checking permissions in templates or custom logic.

Step 4: Test Permissions
Testing Approach:
Create test users via /admin/ or Django shell.
Assign users to Admins, Editors, or Viewers groups.
Log in as different users and try accessing views:
A Viewer should only see the view page.
An Editor should be able to view, create, and edit but not delete.
An Admin should have full access.

Step 5: Documentation & Notes
Important Notes:
Use @permission_required to enforce permission checks in views.
Groups should be assigned using Django Admin or via scripts.
Permissions should be explicitly defined in the Meta class of models.