from celery import shared_task
# internals
from .models import Author, Book


@shared_task
def count_authors():
    return f"Author Count: {Author.objects.count()}"


@shared_task
def get_book_ratings():

    qs = Book.objects.filter(rating__gt=3.99)[:3]

    return dict(qs.values_list('name', 'rating'))
