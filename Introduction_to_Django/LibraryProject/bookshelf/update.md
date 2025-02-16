book1 = Book.objects.filter(title='1984').update(book.title='Nineteen Eighty-Four')
book1.save()

<!-- [<Book: Nineteen Eighty-Four - George Orwell - 1949>] -->
