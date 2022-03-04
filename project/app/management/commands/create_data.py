from typing import Any, Optional
from django.core.management.base import BaseCommand
from django.db import transaction
import random
import decimal
import datetime
# internal
from app.models import Author, Book, Publisher, Store


class Command(BaseCommand):
    help = 'Creates the data(Author, Book, Publisher, Store) to store in database'

    @staticmethod
    def generate_random_decimal_numbers():
        return decimal.Decimal(random.randrange(10000))/100

    @staticmethod
    def generate_random_date():
        return datetime.date(random.randint(1900, 2020), random.randint(1, 12), random.randint(1, 28))

    @staticmethod
    def get_random_authors():
        all_authors = Author.objects.values_list('id', flat=True)
        return random.sample(list(all_authors), random.randint(1, 4))

    @staticmethod
    def get_random_books():
        all_books = Book.objects.values_list('id', flat=True)
        return random.sample(list(all_books), random.randint(1, 10))

    @staticmethod
    def get_random_publisher():
        count = Publisher.objects.count()
        return Publisher.objects.all()[random.randint(0, count - 1)]

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write(self.style.SUCCESS('Process started...'))

        # Delete existence
        Author.objects.all().delete()
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Store.objects.all().delete()

        with transaction.atomic():
            # Create Authors
            for i in range(1, 101):
                Author.objects.create(
                    name=f'Author{i}', age=random.randint(30, 90))

            # Create Publishers
            for i in range(1, 101):
                Publisher.objects.create(name=f'Publisher{i}')

            # Create Books
            book_start = 1
            book_end = 1001
            for i in range(book_start, book_end):
                book = Book(name=f'Book{i}',
                            pages=random.randint(150, 450),
                            price=self.generate_random_decimal_numbers(),
                            rating=random.randrange(1, 5),
                            pubdate=self.generate_random_date(),
                            publisher=self.get_random_publisher()
                            )
                book.save()
                book.authors.add(*self.get_random_authors())

            # Create Stores
            for i in range(1, 101):
                store = Store(name=f'Store{i}')
                store.save()
                store.books.add(*self.get_random_books())

        self.stdout.write(self.style.SUCCESS('Process finished...'))
