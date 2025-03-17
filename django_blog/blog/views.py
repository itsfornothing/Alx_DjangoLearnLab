from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .form import UserForm
from django.contrib.auth.decorators import login_required



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Please provide both email and password!")
            return render(request, 'login.html')
        
        try:
            user_instance = User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(request, "Please register! You don't have an account.")
            return render(request, 'blog/login.html')

        user = authenticate(request, username=user_instance.username, password=password)
        if user:
            login(request, user)
            return redirect('home_page')
        
        messages.error(request, 'Invalid Credential!')

    return render(request, 'blog/login.html')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, "Username is already taken, please enter another.")

            elif User.objects.filter(email__iexact=email).exists():
                messages.error(request, "You already have an account, please login instead!")

            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                login(request, user)
                return redirect('home_page')
    else:
        form = UserForm()

    return render(request, 'blog/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):

    return render(request, 'blog/profile.html')
