from django.urls import path
from .views import (
       CatlogHome,
       NewPost,
       PostDetail,
       UpdatePost,
       DeletePost,
      )


urlpatterns = [
    path('',CatlogHome.as_view() , name='catlog'),
    path('post/new/',NewPost.as_view() , name='new_post'),
    path('post/<int:pk>',PostDetail.as_view(),name='post_detail'),
    path('post/update/<int:pk>',UpdatePost.as_view(),name='update_post'),
    path('post/delete/<int:pk>',DeletePost.as_view(),name='delete_post'),


]
