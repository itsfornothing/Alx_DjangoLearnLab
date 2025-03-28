from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    tags = TaggableManager()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)



