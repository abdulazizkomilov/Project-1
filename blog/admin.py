from django.contrib import admin
from .models import Post, Category, Comment, User

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)