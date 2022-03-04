from rest_framework import routers
from django.urls import path, include

# internals
from app.views import (AuthorViewset, BookViewset,
                       PublisherViewset, StoreViewset)

router = routers.DefaultRouter()

router.register('books', BookViewset, basename='books')
router.register('stores', StoreViewset, basename='stores')
router.register('authors', AuthorViewset, basename='authors')
router.register('publishers', PublisherViewset, basename='publishers')


urlpatterns = [
    path('', include(router.urls))
]
