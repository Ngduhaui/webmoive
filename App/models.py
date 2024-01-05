from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    # Add additional fields
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # You can add other fields as needed
    
    def __str__(self):
        return self.username
    
class Genre(models.Model):
    genreID = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    movieID = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    releaseDate = models.DateField()
    duration = models.DurationField()
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    genreID = models.ForeignKey(Genre, on_delete=models.CASCADE, db_column='genreID', related_name='movies')

    def __int__(self):
        return self.movieID
    
    @property
    def imageURl(self):
        try:
            return self.thumbnail.url
        except:
            return ""

class Comment(models.Model):
    commentID = models.AutoField(primary_key=True, unique=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='username', related_name='Comment')
    movieID = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movieID', related_name='Comment')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        # Cập nhật thời gian mỗi lần lưu
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.commentID)
    
    

