from rest_framework import serializers
from .models import Book, Author
from datetime import timezone, datetime


# Serializer for the Author model
# This serializer converts the Author model instance into JSON format and vice versa.
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


# Serializer for the Book model
# This serializer converts the Book model instance into JSON format and vice versa.
class BookSerializer(serializers.ModelSerializer):
    # this is nested serializer
    author = AuthorSerializer()

    class Meta:
        model = Author
        fields = ['id', 'title', 'publication_year', 'author']
        
    # Custom validation method for the publication_year field
    # Ensures that the publication year is not set in the future
    def validate_publication_year(self, value):
        if datetime.now.date() < value:
            raise serializers.ValidationError("publication_year date cannot be in the Future.")
        return value
