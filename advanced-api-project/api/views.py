from django.shortcuts import render
from rest_framework import generics, filters
from .serializers import BookSerializer
from .models import Book
from rest_framework.response import Response
from rest_framework import status
from .models import Author
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework


# Create your views here.
class BookListView(generics.ListView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Book.objects.all()

        # Filtering
        filter_backends = [rest_framework.DjangoFilterBackend]
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        # Searching
        search_fields = ['title', 'publication_year', 'author']
        search_backend = filters.SearchFilter()
        queryset = search_backend.filter_queryset(self.request, queryset, self)

        # Ordering
        order_backend = filters.OrderingFilter()
        queryset = order_backend.filter_queryset(self.request, queryset, self)

        return queryset



class BookDetailView(generics.DetailView):
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
        


class BookCreateView(generics.CreateView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateView):
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



class BookDeleteView(generics.DeleteView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
