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
         

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'liked_by']


    def validate(self, data):
        if Like.objects.filter(liked_by=self.context['request'].user).exists():
            raise serializers.ValidationError({'username': 'You already liked the post.'})
        return data
    
    def create(self, validated_data):
        post = Post.objects.get(pk=self.context['post_id'])
        like = Like(
            post=post,
            liked_by=self.context['request'].user)
        like.save()

        notification = Notification(
                recipient=validated_data['post'].author,
                actor=self.context['request'].user,
                verb="liked your post.",
                target_content_type=validated_data['post'],
                target_object_id=validated_data['post'].id

            )
        notification.save()

        return like
    

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
