from rest_framework import serializers

from .models import Category, Genre, Title, Review, Comment

class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ListTitlesSerializer(serializers.ModelSerializer):

    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.FloatField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')
        read_only_fields = ('id',)

class DetailsTitlesSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    genre = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='slug',
        queryset=Genre.objects.all())

    rating = serializers.FloatField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')
        read_only_fields = ('id',)


class ReviewsSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        read_only_fields = ('pub_date',)

    def validate(self, data):
        if self.context['request'].method == "POST":
            user = self.context['request'].user
            title = self.context['request'].parser_context['kwargs']['title_id']
            if Review.objects.filter(author=user, title=title).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв к этому произведению')
        return data


class CommentsSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
