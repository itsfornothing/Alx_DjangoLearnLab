book = Book.objects.filter(title="Nineteen Eighty-Four")
book.delete()
<!-- (1, {'bookshelf.Book': 1}) -->


books = Book.objects.all()
print(books)
<QuerySet []>