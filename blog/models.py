from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    followers = models.ManyToManyField('User', blank=True)
    exclude_posts = models.ManyToManyField('Post', blank=True)
    follow = models.ManyToManyField('Category', related_name='follow', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.name


class Post(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250)
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=300)
    image = models.ImageField(upload_to='room/', blank=True, null=True)
    description = RichTextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    like = models.ManyToManyField(User, related_name='like', blank=True)
    favourites = models.ManyToManyField(
        User, related_name='favourite', default=None, blank=True)
    views = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-updated', '-created']

    
    @property
    def getReplies(self):
        return Comment.objects.filter(parent=self).reverse()
    

    @property
    def is_parent(self):
        if self.parent is None:
            return True

    def __str__(self):
        return self.body
