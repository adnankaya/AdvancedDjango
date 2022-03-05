from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from django.db import connection
# internal
from .serializers import (AuthorSerializer,
                          BookSerializer,
                          BookDetailedSerializer,
                          PublisherSerializer, StoreSerializer)
from .models import Author, Book, Publisher, Store
from .pagination import BasePageNumberPagination
from .utils import query_debugger
from .mixins import MultiSerializerViewSetMixin


class BaseViewset(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    pagination_class = BasePageNumberPagination


class AuthorViewset(BaseViewset):
    serializer_class = AuthorSerializer

    def get_queryset(self):
        return Author.objects.all().order_by('-pk')


class PublisherViewset(BaseViewset):
    serializer_class = PublisherSerializer

    def get_queryset(self):
        return Publisher.objects.all().order_by('-pk')


class BookViewset(MultiSerializerViewSetMixin, BaseViewset):
    serializer_class = BookSerializer

    serializer_action_classes = {
        'retrieve': BookDetailedSerializer,
    }

    def get_queryset(self):
        if self.action == 'retrieve':
            return self.get_queryset_for_retrieve_action()

        qs = Book.objects.prefetch_related('authors').order_by('-pubdate')
        return qs

    @staticmethod
    def get_queryset_for_retrieve_action():
        qs = Book.objects.select_related(
            'publisher').prefetch_related(
            'authors', 'store_set',
            'store_set__books'
        )
        return qs

    @query_debugger
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class StoreViewset(BaseViewset):
    serializer_class = StoreSerializer

    def get_queryset(self):
        queryset = Store.objects.all()
        qs = self.get_serializer_class().setup_eager_loading(queryset)
        return qs

    @query_debugger
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
