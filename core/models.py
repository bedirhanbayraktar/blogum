from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Blog(models.Model):
    title = models.CharField(max_length=100)
    comment = models.TextField()
    image_file1 = models.ImageField(upload_to='resimler/')
    image_file2 = models.ImageField(upload_to='resimler/', blank=True, null=True)  # İkinci resim alanı (zorunlu değil)
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    categories = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return self.title



