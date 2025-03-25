from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Create a new user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Create an auth token for the user
        Token.objects.create(user=user)
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
