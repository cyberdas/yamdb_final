from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User

class Category(models.Model):

    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):

    name = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    genre = models.ManyToManyField(
        Genre,
        related_name='genres'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class Review(models.Model):

    text = models.TextField()
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return str(self.id)


class Comment(models.Model):

    review = models.ForeignKey(Review,on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации комментария', auto_now_add=True)

    def __str__(self):
        return str(self.id)