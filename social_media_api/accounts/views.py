import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.conf import settings
from .serializers import RegisterationSerializer, LoginSerializer, FollowSerializer, UnfollowSerializer
from accounts.authentication import JWTAuthentication


def generate_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.now(timezone.utc) + timedelta(hours=24),
        'iat': datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = generate_token(user)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = generate_token(user)
            return Response({'token': token}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class FollowView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    
    def post(self, request, user_id):
        serializer = FollowSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UnfollowView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    
    def post(self, request, user_id):
        serializer = UnfollowSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
