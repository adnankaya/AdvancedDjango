import abc
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework import status, response
from elasticsearch_dsl import Q
# internals
from app.serializers import BookDetailedSerializer, BookSearchSerializer, BookSerializer
from app.documents import BookDocument


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        '''returns Q() expression'''

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            res = search.execute()

            print(
                f'Found {res.hits.total} hit(s) for query: "{query}"')

            results = self.paginate_queryset(res, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            context = {'error': str(e)}
            return response.Response(context, status=status.HTTP_404_NOT_FOUND)


class SearchBooks(PaginatedElasticSearchAPIView):
    serializer_class = BookSearchSerializer
    document_class = BookDocument

    def generate_q_expression(self, query):
        return Q(
            'multi_match', 
            query=query, 
            fields=[
                'name', 'authors', 'publisher',

            ], 
            fuzziness='auto',
        )
