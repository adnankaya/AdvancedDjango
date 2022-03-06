from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from model_mommy import mommy
import random
# internals
from app.management.commands.create_data import Command as CreateDataCommand
from app.models import Author, Book, Publisher, Store


class BaseTestCase(TestCase):
    url_api_prefix = '/api/v1/'

    def setUp(self) -> None:
        self.client = APIClient()


class AuthorViewsetTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        CreateDataCommand.create_authors()

    def test_list_authors(self):
        endpoint = f'{self.url_api_prefix}authors/'
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('count'), 100)
        self.assertEqual(res_data.get('current_page'), 1)
        self.assertEqual(res_data.get('total_pages'), 10)

    def test_retrieve_author(self):
        pk = 4
        endpoint = f'{self.url_api_prefix}authors/{pk}/'
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), f'Author{pk}')

    def test_update_author(self):
        pk = 4
        age = 4444
        updated_name = f'Author{age}'
        payload = {'name': updated_name, 'age': age}
        endpoint = f'{self.url_api_prefix}authors/{pk}/'
        res = self.client.put(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), updated_name)
        self.assertEqual(res_data.get('age'), age)

    def test_post_author(self):
        author_name = 'Author999'
        author_age = 99
        payload = {'name': author_name, 'age': author_age}
        endpoint = f'{self.url_api_prefix}authors/'
        res = self.client.post(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), author_name)
        self.assertEqual(res_data.get('age'), author_age)


class PublisherViewsetTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        CreateDataCommand.create_publishers()

    def test_list_publishers(self):
        endpoint = f'{self.url_api_prefix}publishers/'
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('count'), 100)
        self.assertEqual(res_data.get('current_page'), 1)
        self.assertEqual(res_data.get('total_pages'), 10)

    def test_retrieve_publisher(self):
        pk = 4
        endpoint = f'{self.url_api_prefix}publishers/{pk}/'
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), f'Publisher{pk}')

    def test_update_publisher(self):
        pk = 4
        updated_name = f'Publisher'
        payload = {'name': updated_name}
        endpoint = f'{self.url_api_prefix}publishers/{pk}/'
        res = self.client.put(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), updated_name)

    def test_post_publisher(self):
        publisher_name = 'Publisher999'
        payload = {'name': publisher_name}
        endpoint = f'{self.url_api_prefix}publishers/'
        res = self.client.post(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), publisher_name)


class SearchBookViewsetTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        CreateDataCommand.create_authors()
        CreateDataCommand.create_publishers()
        CreateDataCommand.create_books(1, 101)

    def test_search_books_by_name(self):
        queries = ['Book1', 'Took1', 'Author1',
                   'Buthur1', 'Publisher1', 'Xoblisher1']
        for query in queries:
            endpoint = f'{self.url_api_prefix}search-books/{query}/'
            res = self.client.get(endpoint)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            res_data = res.json()
            self.assertTrue(len(res_data.get('results')) > 0)


class BookViewsetTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        CreateDataCommand.create_authors()
        CreateDataCommand.create_publishers()
        CreateDataCommand.create_books(1, 101)

    def test_list_books(self):
        endpoint = f'{self.url_api_prefix}books/'
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('count'), 100)
        self.assertEqual(res_data.get('current_page'), 1)
        self.assertEqual(res_data.get('total_pages'), 10)

    def test_retrieve_book(self):
        pk = 4
        endpoint = f'{self.url_api_prefix}books/{pk}/'
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), f'Book{pk}')

    def test_update_book(self):
        pk = 4
        publisher = CreateDataCommand.get_random_publisher()
        book_name = 'Book999'
        book = {
            'name': book_name,
            'pages': random.randint(150, 450),
            'price': CreateDataCommand.generate_random_decimal_numbers(),
            'rating': random.randrange(1, 5),
            'pubdate': CreateDataCommand.generate_random_date(),
            'publisher': publisher.pk,
            'authors': CreateDataCommand.get_random_authors()
        }

        payload = {**book}
        endpoint = f'{self.url_api_prefix}books/{pk}/'
        res = self.client.put(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), book_name)

    def test_post_book(self):
        publisher = CreateDataCommand.get_random_publisher()
        book_name = 'Book999'
        book = {
            'name': book_name,
            'pages': random.randint(150, 450),
            'price': CreateDataCommand.generate_random_decimal_numbers(),
            'rating': random.randrange(1, 5),
            'pubdate': CreateDataCommand.generate_random_date(),
            'publisher': publisher.pk,
            'authors': CreateDataCommand.get_random_authors()
        }

        payload = {**book}
        endpoint = f'{self.url_api_prefix}books/'
        res = self.client.post(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), book_name)


class StoreViewsetTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        CreateDataCommand.create_authors()
        CreateDataCommand.create_publishers()
        CreateDataCommand.create_books(1, 101)
        CreateDataCommand.create_stores()

    def test_list_stores(self):
        endpoint = f'{self.url_api_prefix}stores/'
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('count'), 100)
        self.assertEqual(res_data.get('current_page'), 1)
        self.assertEqual(res_data.get('total_pages'), 10)

    def test_retrieve_store(self):
        pk = 4
        endpoint = f'{self.url_api_prefix}stores/{pk}/'
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), f'Store{pk}')

    def test_update_store(self):
        pk = 4
        updated_name = f'Store'
        payload = {'name': updated_name,
                   'books': CreateDataCommand.get_random_books()}
        endpoint = f'{self.url_api_prefix}stores/{pk}/'
        res = self.client.put(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), updated_name)

    def test_post_store(self):
        store_name = 'Store999'
        payload = {'name': store_name,
                   'books': CreateDataCommand.get_random_books()}
        endpoint = f'{self.url_api_prefix}stores/'
        res = self.client.post(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_data = res.json()
        self.assertEqual(res_data.get('name'), store_name)
