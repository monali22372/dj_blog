from django.db import models
from django.utils import timezone
# To set author i.e. user from User Table we need to add below import
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # need author having relation with Users table in Django Database
    author = models.ForeignKey(User, on_delete = models.CASCADE)



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})   


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80) 
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True)

    class Meta:
       ordering = ('created',)

    def str (self):
       return f'Comment by {self.name} on {self.post}'
