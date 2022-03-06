from rest_framework import serializers

# internal
from .models import Author, Book, Publisher, Store


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'age')


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('id', 'name')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name', 'pages', 'price',
                  'rating', 'authors', 'publisher',
                  'pubdate',
                  )

class BookSearchSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer(many=False)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'books')

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.prefetch_related('books').order_by('-pk')


class BookDetailedSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()
    authors = AuthorSerializer(many=True)
    store_set = StoreSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'pages', 'price',
                  'rating', 'authors', 'publisher',
                  'pubdate', 'store_set',
                  )

    # @staticmethod # NOTE we could use this method too!
    # def setup_eager_loading(queryset):
    #     queryset = queryset.select_related(
    #         'publisher').prefetch_related(
    #         'authors', 'store_set', 'store_set__books'
    #         )

    #     return queryset
