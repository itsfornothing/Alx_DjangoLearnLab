from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import NotificationSerializer
from accounts.authentication import JWTAuthentication
from .models import Notification

# Create your views here.
 
class NotificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user)
        serializer = NotificationSerializer(notifications, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
            
