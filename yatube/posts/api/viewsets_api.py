from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Comment
from posts.api.serializer import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from posts.api.permissions import IsAuthor
from rest_framework.pagination import PageNumberPagination


class PostViewSet(ModelViewSet):
    """
    Viewset содержит весь тот же функционал, что у view-функции и veiew-классов в views_api.py + действия с комментариями
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthor,)  # ограничение на уровне всего viewset'а
    pagination_class = PageNumberPagination  # пагинация ответа на api запросы, макс. число указано в settings.py

    # в POST запросе при сохранении нового поста дописываем в поле author текущего пользователя
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST'], detail=False)  # TODO: надо прокинуть post
    def post_comment(self, request, id):
        post = Post.objects.get(id=id)
        serializer = CommentSerializer(Comment, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # получение всех комментариев к посту
    @action(methods=['GET'], detail=False)
    def get_comments(self, request, id):
        post = Post.objects.get(id=id)
        comments = post.comments.all()
        return Response(CommentSerializer(comments, many=True).data)

    @action(methods=['GET'], detail=False)
    def get_comment(self, request, id, comment_id):
        comment = Comment.objects.get(id=comment_id)
        return Response(CommentSerializer(comment).data)

    @action(methods=['PUT'], detail=False)
    def put_comment(self, request, id, comment_id):
        comment = Comment.objects.get(id=comment_id)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=False)
    def delete_comment(self, request, id, comment_id):
        comment = Comment.objects.get(id=comment_id)

        # данный viewset основан на модели Post и проверка ограничений происходит только на посты,
        # поэтому также указываем ограничения на объект comment
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
