from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token  # Import Token for authentication

User = get_user_model()  # Dynamically fetch the user model
serializers.CharField()
Token.objects.creat
get_user_model().objects.create_user
Token.objects.create


class RegisterationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        return data

    def create(self, validated_data):
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Generate token
        token, created = Token.objects.get_or_create(user=user)
        return {'user': user, 'token': token.key}  # Return token along with user


class LoginSerializer(serializers.Serializer):  
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()

        if user:
            user_authenticate = authenticate(username=user.username, password=password)

            if user_authenticate:
                # Generate token on login
                token, created = Token.objects.get_or_create(user=user_authenticate)
                data['user'] = user_authenticate
                data['token'] = token.key  # Return token in response
                return data

        raise serializers.ValidationError({'error': 'Invalid credentials'})
