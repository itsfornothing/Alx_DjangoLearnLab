from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Book, Author
from rest_framework import status


class NoteApiTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='belachew')
        self.book0 = Book.objects.create(
            title='yzehna',
            author = self.author,
            publication_year = '2020-03-20'
        )

        self.book1 = Book.objects.create(
            title='another book',
            author=self.author,
            publication_year='2021-05-15'
        )
        self.url = reverse('list_books', kwargs={"note_id": self.note.pk})

    def test_get_note(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], self.book1.title)
        self.assertEqual(response.data[1]['title'], self.book2.title)

        self.assertEqual(response.data[0]['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data[1]['publication_year'], self.book2.publication_year)
