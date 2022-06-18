from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(null=True, blank = True, upload_to = "images/")
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.body
