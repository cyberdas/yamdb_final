from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug') 
    search_fields = ('name',) 
    list_filter = ('name',) 
    empty_value_display = '-пусто-'

class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug') 
    search_fields = ('name',) 
    list_filter = ('name',) 
    empty_value_display = '-пусто-'

class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category') 
    search_fields = ('name',) 
    list_filter = ('name',) 
    empty_value_display = '-пусто-'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'score', 'title') 
    search_fields = ('pk', 'text', 'author') 
    list_filter = ('author', 'pub_date') 
    empty_value_display = '-пусто-'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'review') 
    search_fields = ('pk', 'text', 'author') 
    list_filter = ('author', 'pub_date') 
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
