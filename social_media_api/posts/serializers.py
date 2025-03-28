from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = ['post', 'author', 'content', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        
        return super().create(validated_data)
         
    

class UnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'liked_by']

    def create(self, validated_data):
        post = Post.objects.get(pk=self.context['post_id'])

        if Like.objects.filter(liked_by=self.context['request'].user).exists():
            unlike = Like.objects.filter(post=post)
            unlike.liked_by.remove()
            unlike.save()

        return post
