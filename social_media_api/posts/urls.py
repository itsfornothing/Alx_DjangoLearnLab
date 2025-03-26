from django.urls import path
from .views import CreatePostView, CreateCommentView, PostDetailView, CommentDetailView, PostTitleSearchView

urlpatterns = [
    path('posts/', CreatePostView.as_view(), name='create_post'),
    path('comments/', CreateCommentView.as_view(), name='create_comment'),
    path('post/<int:post_id>', PostDetailView.as_view(), name='post_by_id'),
    path('comment/<int:comment_id>', CommentDetailView.as_view(), name='post_by_id'),
    path('post/search/title/<str:title>', PostTitleSearchView.as_view(), name='note_by_title'),
]