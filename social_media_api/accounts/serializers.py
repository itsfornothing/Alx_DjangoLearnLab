from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate



class RegisterationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']


    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            user_authenticate = authenticate(username=user.username, password=password)

            if user_authenticate:
                data['user'] = user_authenticate
                return data
            
        raise serializers.ValidationError({'error': 'Invalid credentials'})
