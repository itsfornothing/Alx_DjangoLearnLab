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
from django.contrib.auth.decorators import permission_required



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
    # Check if user is authenticated and has a profile with 'Admin' role
    if not user.is_authenticated:
        return False
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

# Combine login_required and user_passes_test for better security
@login_required
@user_passes_test(is_admin, login_url='/login/')
def Admin(request):
    # Only Admin role users will reach this point
    context = {
        'message': 'Welcome to the Admin Dashboard',
        'user_role': request.user.userprofile.role if hasattr(request.user, 'userprofile') else 'Unknown'
    }
    return render(request, 'admin_dashboard.html', context)

@user_passes_test(lambda user: user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian')
def librarian_view(request):
    return render(request, 'relationship_app/librarian.html')

@user_passes_test(lambda user: user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member')
def member_view(request):
    return render(request, 'relationship_app/member.html')



@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Assuming you have a book list view
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/delete_book.html', {'book': book})

