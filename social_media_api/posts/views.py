from rest_framework.generics import GenericAPIView
from accounts.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from django.core.paginator import Paginator
from rest_framework import viewsets



class CreatePostView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostDetailView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()


    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, author=request.user)
            p = Paginator(post, 2)
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
        

class CreateCommentView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()


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


class CommentDetailView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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

            return Response({'msg': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)        
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        

class PostTitleSearchView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, title):
        try:
            post = Post.objects.filter(title__icontains=title)
            serializer = PostSerializer(post, many=True, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
