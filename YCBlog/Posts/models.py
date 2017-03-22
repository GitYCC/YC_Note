from django.db import models
import markdown2, urllib
from django.core.cache import cache

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField(blank=True)
    file = models.URLField(max_length=500,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    post_time = models.DateTimeField()
    isPublic = models.BooleanField()
    kind = models.CharField(max_length=200)
    tags = models.CharField(max_length=500,blank=True)
    author = models.CharField(max_length=200)
    front_board = models.URLField(max_length=500,blank=True)

    def save(self, *args, **kwargs):
        self._refresh_memcached()
        self._content_complement()
        super(Post, self).save(*args, **kwargs) 

    def _content_complement(self):
        if not self.content and self.file:
            text = urllib.request.urlopen(self.file).read().decode("utf-8") 
            html = markdown2.markdown(text,extras=['fenced-code-blocks'])  
            self.content = html
    
    def _refresh_memcached(self):
        if self.kind == "Coding":
            cache.delete("coding_posts")
        elif self.kind == "Reading":
            cache.delete("reading_posts")
        elif self.kind == "Living":
            cache.delete("living_posts")