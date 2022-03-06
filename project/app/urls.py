from rest_framework import routers
from django.urls import path, include

# internals
from app.views import (AuthorViewset, BookViewset,
                       PublisherViewset, StoreViewset)
from app.elastic_views import SearchBooks

router = routers.DefaultRouter()

router.register('books', BookViewset, basename='books')
router.register('stores', StoreViewset, basename='stores')
router.register('authors', AuthorViewset, basename='authors')
router.register('publishers', PublisherViewset, basename='publishers')


urlpatterns = [
    path('', include(router.urls)),
    path('search-books/<str:query>/', SearchBooks.as_view()),
]
