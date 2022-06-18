from django.urls import path
from .views import PostListView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',PostListView.as_view(), name="feeds")
]
