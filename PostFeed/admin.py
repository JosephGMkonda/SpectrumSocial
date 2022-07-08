from ctypes.wintypes import tagSIZE
from django.contrib import admin
from .models import Posts, Follow, Tag, Stream

admin.site.register(Posts)
admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Stream)

# Register your models here.
