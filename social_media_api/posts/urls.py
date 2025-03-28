from django.urls import path
from .views import CreatePostView, CreateCommentView, PostDetailView, CommentDetailView, PostTitleSearchView, FeedView, LikeView, UnlikeView

urlpatterns = [
    path('posts/', CreatePostView.as_view(), name='create_post'),
    path('comments/', CreateCommentView.as_view(), name='create_comment'),
    path('post/<int:post_id>', PostDetailView.as_view(), name='post_detail'),
    path('comment/<int:comment_id>', CommentDetailView.as_view(), name='comment_detail'),
    path('post/search/title/<str:title>', PostTitleSearchView.as_view(), name='note_by_title'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', LikeView.as_view(), name='liked'),
    path('posts/<int:pk>/unlike/', UnlikeView.as_view(), name='unliked'),

]
