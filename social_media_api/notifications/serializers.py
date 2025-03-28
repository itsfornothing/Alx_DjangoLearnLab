from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['recipient', 'actor', 'verb', 'target_content_type', 'target_object_id', 'target', 'timestamp']