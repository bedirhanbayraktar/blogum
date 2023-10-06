from django.contrib import admin
from .models import Post, Blog, Category

admin.site.register(Post)
admin.site.register(Blog)
admin.site.register(Category)