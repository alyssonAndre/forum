from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post).order_by('-created_at')

    def perform_create(self, serializer):
        post = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post)

class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            user = request.user

            if user in post.likes.all():
                post.likes.remove(user)
                message = 'Like removido'
            else:
                post.likes.add(user)
                post.dislikes.remove(user)
                message = 'Post curtido'
            return Response({
                'message': message,
                'like_count': post.likes.count(),
                'dislike_count': post.dislikes.count()
            })
        except Post.DoesNotExist:
            return Response({'error':'Post não encontrado'}, status=status.HTTP_404_NOT_FOUND)


class DislikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)

            user = request.user

            if user in post.dislikes.all():
                post.dislikes.remove(user)
                message = 'Dislike removido'
            else:
                post.dislikes.add(user)
                post.likes.remove(user)
                message = 'Post descurtido'

            return Response({
                'message': message,
                'like_count': post.like_count(),
                'dislike_count': post.dislike_count()
            })

        except Post.DoesNotExist:
            return Response({'error': 'Post não encontrado'}, status=status.HTTP_404_NOT_FOUND)