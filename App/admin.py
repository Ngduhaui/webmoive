from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Genre, Movie, Comment

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('genreID', 'name')
    
class MovieAdmin(admin.ModelAdmin):
    list_display = ('movieID', 'title', 'genreID', 'releaseDate')
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentID', 'movieID', 'username', 'content', 'created_at')

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Comment, CommentAdmin)
