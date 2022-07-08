from django.urls import path
from PostFeed.views import index,NewPost,PostDetails,tags,like
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',index, name="feeds"),
    path('newpost',NewPost, name='newpost'),
    path('<uuid:post_id>',PostDetails, name='postdetail'),
    path('<uuid:post_id>/like',like, name='postlike')
    # path('tag/<slug:tag_slug>',tags, name='tags')
]
