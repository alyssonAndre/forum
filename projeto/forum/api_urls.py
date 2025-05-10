from django.urls import path
from .api import *

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post_retrieve_update_destroy'),
    path('posts/<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='comment_list_create'),
    path('posts/<int:post_id>/like/', LikePostAPIView.as_view(), name='post_like'),
    path('posts/<int:post_id>/dislike/', DislikePostAPIView.as_view(), name='post_dislike'),
]
