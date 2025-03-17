from django.urls import path
from . import views
from .views import BlogListView, BlogDetailView, BlogCreate, PostUpdateView, PostDeleteView

urlpatterns = [
    path('posts/', BlogListView.as_view(), name='home_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('posts/new/', BlogCreate.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    ]
