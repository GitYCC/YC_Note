from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField(blank=True)
    file = models.URLField(max_length=200,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    post_time = models.DateTimeField()
    isPublic = models.BooleanField()
    kind = models.CharField(max_length=200)
    tags = models.CharField(max_length=500,blank=True)
    author = models.CharField(max_length=200)
    front_board = models.URLField(max_length=200,blank=True)
