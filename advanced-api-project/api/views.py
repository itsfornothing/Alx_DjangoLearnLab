from django.shortcuts import render
from rest_framework import generics
from .serializers import BookSerializer
from .models import Book
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


# Create your views here.
class BookList(generics.ListView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDetail(generics.DetailView):
    queryset = Book.objects.get()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        try:
            note = Book.objects.get(id=book_id)
            serializer = self.serializer_class(note, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        


class BookCreate(generics.CreateView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdate(generics.UpdateView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, note_id):
        try:
            note = Book.objects.get(id=note_id, owner=request.user)
            serializer = self.serializer_class(note, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Book updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)



class BookDelete(generics.DeleteView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
