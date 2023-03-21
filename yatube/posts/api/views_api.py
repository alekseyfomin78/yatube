from posts.models import Post
from posts.api.serializer import PostSerializer
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from posts.api.permissions import IsAuthor
from rest_framework.pagination import PageNumberPagination
from posts.api.filters import PostFilter

# api view функции
# получение всех записей, либо создание новой записи
# @api_view(['GET', 'POST'])
# def api_posts(request):
#     if request.method == 'GET':
#         post = Post.objects.all()
#         serializer = PostSerializer(post, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         if request.user.is_authenticated:
#             serializer = PostSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(author=request.user)  # при сохранении поста в БД в author указываем текущего пользователя
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(status=status.HTTP_403_FORBIDDEN)


# view класс аналогичный view функции api_posts
class APIPosts(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]  # фильтрация по полю text
    search_fields = ['text', ]
    filterset_class = PostFilter  # фильтрация по диапазону дат публикации постов

    permission_classes = (IsAuthor,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# получение конкретной записи, её обновление или удаление
# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def api_posts_detail(request, id):
#     post = Post.objects.filter(pk=id).first()
#
#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT' or request.method == 'PATCH':
#         if request.user == post.author:
#             serializer = PostSerializer(post, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(status=status.HTTP_403_FORBIDDEN)
#
#     elif request.method == 'DELETE':
#         if request.user == post.author:
#             post.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(status=status.HTTP_403_FORBIDDEN)


# api view класс, аналогичный api_posts_detail функции
class APIPostDetail(APIView):
    def get(self, request, id):
        post = Post.objects.filter(pk=id).first()
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, id):
        post = Post.objects.filter(pk=id).first()

        if request.user == post.author:
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, id):
        post = Post.objects.filter(pk=id).first()

        if request.user == post.author:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
