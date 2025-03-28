from rest_framework.generics import GenericAPIView
from accounts.authentication import JWTAuthentication
from rest_framework import permissions
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from rest_framework import viewsets



class CreatePostView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()


    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostDetailView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, author=request.user)
            serializer = PostSerializer(post, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Post.DoesNotExist:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        
    
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, author=request.user)
            serializer = PostSerializer(post, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Post updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PostSerializer.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, author=request.user)
            post.delete()

            return Response({'msg': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)        
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        

class CreateCommentView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        all_posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(all_posts, many=True, context={'request': request}) 

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class CommentDetailView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
            serializer = CommentSerializer(comment, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
    
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
            serializer = CommentSerializer(comment, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Comment updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
            comment.delete()

            return Response({'msg': 'Comment deleted successfully'}, status=status.HTTP_200_OK)        
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        

class PostTitleSearchView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, title):
        post = Post.objects.filter(title__icontains=title)

        if not post.exists():
            return Response({"error": "No posts found with the given title"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
        

class FeedView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        try:
            following_users = request.user.following.all()
            posts = Post.objects.filter(author__in=following_users).order_by('-created_at')


            return Response(posts, status=status.HTTP_200_OK)
        
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
            


class LikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        generics = generics.get_object_or_404(Post, pk=post_id)


        if Like.objects.filter(liked_by=request.user, post=post).exists():
            return Response({"error": 'You already liked the post.'}, status=status.HTTP_400_BAD_REQUEST)
        
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked your post.",
                    target_content_type=ContentType.objects.get_for_model(post),
                    target_object_id=post.id

                )
        
        return Response({'msg': 'You like the post.'}, status=status.HTTP_200_OK)


class UnlikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        generics = generics.get_object_or_404(Post, pk=post_id)

        if not Like.objects.filter(liked_by=request.user, post=post).exists():
            return Response({"error": 'You canot unlike this post.'}, status=status.HTTP_400_BAD_REQUEST)
        
        unlike = Like.objects.filter(liked_by=request.user, post=post)
        unlike.liked_by.remove()
        unlike.save()
        
        return Response({'msg': 'You unlike the post.'}, status=status.HTTP_200_OK)
