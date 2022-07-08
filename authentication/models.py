import profile
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#creating user profile and merging it with the user 
# the class taking user model build in django and add some fields

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    profile_info = models.TextField(max_length=150, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to=user_directory_path,blank=True,null=True, verbose_name='pictures')

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)    