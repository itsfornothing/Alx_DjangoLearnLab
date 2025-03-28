from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

Token.objects.create
get_user_model().objects.create_user

class RegisterationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True,required=True)
    bio = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'bio', 'profile_picture']


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


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['followers', 'following']


    def validate(self, data):
        request_user = self.context['request'].user

        try:
            user_to_follow = CustomUser.objects.filter(username=data['username'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        
        if request_user == user_to_follow:
            raise serializers.ValidationError("You cannot follow yourself.")
        
        if request_user.following.filter(id=user_to_follow.id).exists():
            raise serializers.ValidationError("You are already following this user.")
        
    def create(self, validated_data):
        user = CustomUser.objects.filter(username=validated_data['username'])
        you = self.context['request'].user

        you.following.add(user)
        you.save()

        user.followers.add(you)
        user.save()

class UnfollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['followers', 'following']

    def validate(self, data):
        request_user = self.context['request'].user

        try:
            user_to_unfollow = CustomUser.objects.filter(username=data['username'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        
        if not request_user.following.filter(id=user_to_unfollow.id).exists():
            raise serializers.ValidationError("You are not following this user.")

    def create(self, validated_data):
        user = CustomUser.objects.filter(username=validated_data['username'])
        you = self.context['request'].user

        you.following.remove(user)
        you.save()

        user.followers.remove(you)
        user.save()
