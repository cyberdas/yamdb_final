from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet, ReviewsViewSet, CommentsViewSet

router = DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentsViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),   
]