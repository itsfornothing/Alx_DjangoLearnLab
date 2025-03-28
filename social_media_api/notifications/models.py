from django.db import models
from accounts.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)  
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True) # fkey that stores metadata about all the models in your project
    target_object_id = models.PositiveIntegerField(null=True, blank=True)# This field stores the primary key (ID) of the object being referenced.
    target = GenericForeignKey('target_content_type', 'target_object_id')# combines target_content_type and target_object_id to create a reference to any object in your database.
    timestamp = models.DateTimeField(auto_now_add=True)
    