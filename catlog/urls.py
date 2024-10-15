from django.urls import path
from .views import catlog_home, NewPost

urlpatterns = [
    path('',catlog_home , name='catlog'),
    path('post/new/',NewPost.as_view() , name='newpost'),
]
