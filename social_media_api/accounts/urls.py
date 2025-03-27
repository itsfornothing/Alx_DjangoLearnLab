from django.urls import path
from .views import LoginView, RegisterView, FollowView, UnfollowView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('login/', LoginView.as_view(), name="login"),
    path('follow/<int:user_id>/', FollowView.as_view(), name="follow"),
    path('unfollow/<int:user_id>/', UnfollowView.as_view(), name="unfollow"),
]

