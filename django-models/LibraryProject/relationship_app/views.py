from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile



# Create your views here.
def all_books(request):
    books = Book.objects.all() 
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User Not Found....")
            return redirect("home")

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or Password does not match...")

    return render(request, "relationship_app/login.html") 
   

class RegisterView(CreateView):
    form_class = UserCreationForm()
    template_name = "relationship_app/register.html"
    success_url = reverse_lazy("login")



class CustomLogoutView(LogoutView):
    template_name = "relationship_app/logged_out.html"


def is_admin(user):
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'Admin'
    except UserProfile.DoesNotExist:
        return False

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin view
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view
@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view
@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')



