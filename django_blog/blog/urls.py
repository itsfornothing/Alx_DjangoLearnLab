from django.urls import path
from . import views
from .views import BlogListView, BlogDetailView, BlogCreate, PostUpdateView, PostDeleteView, PostByTagListView

urlpatterns = [
    path('posts/', BlogListView.as_view(), name='home_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('posts/new/', BlogCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('post/comments/new/', BlogDetailView.as_view(), name='new_comment'),
    path('post/<int:pk>/comments/update/', BlogDetailView.as_view(), name='edit_comment'),
    path('post/<int:pk>/comments/delete/', BlogDetailView.as_view(), name='delete_comment'),

    path('post/tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='post_detail'),
    path('post/search/', views.search_view, name='post_detail'),
    ]
