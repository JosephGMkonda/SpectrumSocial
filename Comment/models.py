from django.db import models
from PostFeed.models import Posts
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
