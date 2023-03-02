from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username', read_only=True)
    permission_classes = [IsAuthenticated]

    class Meta:
        model = Comment
        fields = ('id', 'post', 'text', 'author', 'created')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username', read_only=True)  # source='author.username' - выводит username, а не id
    permission_classes = [IsAuthenticated]  # ограничение - действия могут выполнять только авторизированные юзеры
    comments = CommentSerializer(many=True)  # для получения списка комментариев к каждому посту

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'pub_date', 'comments')

