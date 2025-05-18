from django.urls import path
from . import views
from .views import PostCreateView

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create-post/', PostCreateView.as_view(), name='post_create'),
]
