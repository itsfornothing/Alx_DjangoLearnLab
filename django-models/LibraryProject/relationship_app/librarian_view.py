# librarian_view.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian.html', {'message': 'Welcome to Librarian Dashboard'})
