from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.generics import get_object_or_404

from .filters import TitlesFilter
from .models import Category, Genre, Title, Review, Comment
from .mixins import PermissionMixin
from .permissions import IsAdminUserOrReadOnly, IsAdminOrAuthor
from .serializers import CategoriesSerializer, GenresSerializer, ListTitlesSerializer, DetailsTitlesSerializer, ReviewsSerializer, CommentsSerializer

class CreatListDestroyViewSet(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    pass
  

class CategoriesViewSet(CreatListDestroyViewSet):

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class GenresViewSet(CreatListDestroyViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return DetailsTitlesSerializer
        return ListTitlesSerializer

    def get_queryset(self):
        queryset = Title.objects.annotate(rating = Avg('reviews__score'))
        return queryset

class ReviewsViewSet(PermissionMixin):

    serializer_class = ReviewsSerializer

    def get_queryset(self):
        reviews = Review.objects.filter(title=self.kwargs.get('title_id'))
        return reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(PermissionMixin):

    serializer_class = CommentsSerializer


    def get_queryset(self):
        comments = Comment.objects.filter(review=self.kwargs.get('review_id'))
        return comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
