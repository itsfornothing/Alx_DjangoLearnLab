from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    # Check if user is authenticated and has a profile with 'Admin' role
    if not user.is_authenticated:
        return False
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'



@user_passes_test(is_admin)
def Admin(request):
    # Only Admin role users will reach this point
    context = {
        'message': 'Welcome to the Admin Dashboard',
        'user_role': request.user.userprofile.role if hasattr(request.user, 'userprofile') else 'Unknown'
    }
    return render(request, 'admin_dashboard.html', context)
