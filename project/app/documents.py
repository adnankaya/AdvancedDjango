from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
# internals
from app.models import Book, Author, Publisher


@registry.register_document
class BookDocument(Document):
    authors = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'age': fields.IntegerField(),
    })
    publisher = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    class Index:
        name = 'books'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Book
        fields = ['name',
                  ]
        # Optional: to ensure the Book will be re-saved when Author or Publisher is updated
        related_models = [Publisher, Author]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super().get_queryset().select_related('publisher')

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Book instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, (Author, Publisher)):
            return related_instance.book_set.all()
