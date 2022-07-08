from fileinput import filename
from tabnanny import verbose
from turtle import title
from django.db import models
from django.utils import timezone

from django.db.models.signals import post_save
from django.utils.text import slugify
from django.urls import reverse
import uuid

from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return 'user_{0}/{0}'.format(instance.user.id, filename)

class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name_plural="Tags"
    
    def get_absolute_url(self):
        return reverse("tags", args=[self.Tag])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pictures = models.ImageField(upload_to=user_directory_path,verbose_name="Picture", null=False)
    caption = models.TextField(max_length=1500,verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("postdetail", args=[str(self.id)])

    

class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User,on_delete=models.CASCADE, related_name='following')

class Stream(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    date = models.DateTimeField()


    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    posts= models.ForeignKey(Posts, on_delete=models.CASCADE,related_name="post_likes")


post_save.connect(Stream.add_post,sender=Posts)

    
