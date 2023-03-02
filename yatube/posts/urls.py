from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from . import views_class_based
from . import views_api
from . import viewsets_api

urlpatterns = [
    # главная страница
    # path(route="", view=views.index, name="index"),
    path(route='', view=views_class_based.PostsListView.as_view(), name='index'),

    # страница группы
    # path(route="group/<slug:slug>/", view=views.group_posts, name="group"),
    path(route="group/<slug:slug>/", view=views_class_based.GroupPostsListView.as_view(), name="group"),

    # страница создания новой записи
    # path(route="new/", view=views.new_post, name="new_post"),
    path(route="new/", view=views_class_based.NewPostCreateView.as_view(), name="new_post"),

    # страница с постами пользователей, на которых подписан пользователь
    # path("follow/", views.follow_index, name="follow_index"),
    path("follow/", views_class_based.FollowPostsListView.as_view(), name="follow_index"),

    # Профайл пользователя
    # path('<str:username>/', views.profile, name='profile'),
    path('<str:slug>/', views_class_based.ProfileDetailView.as_view(), name='profile'),

    path("<str:username>/follow/", views.profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),

    # Просмотр поста
    # path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/', views_class_based.PostDetailView.as_view(), name='post'),

    # Редактирование поста
    # path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('<str:username>/<int:post_id>/edit/', views_class_based.PostEditView.as_view(), name='post_edit'),

    # Добавление комментария
    path("<str:username>/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    # path("<str:username>/<int:post_id>/comment/", views_class_based.AddCommentView.as_view(), name="add_comment"),
]

# API
urlpatterns += [
    # получение токена
    path(route=r'api/v1/api-token-auth/', view=obtain_auth_token),

    # маршруты для viewset'ов
    # маршрут для получения комментариев к посту, в actions - get запрос обрабатывает функция get_comments и т.д.
    path(route=r'api/v1/posts/<int:id>/comment/', view=viewsets_api.PostViewSet.as_view(
        actions={
            'post': 'post_comment',
            'get': 'get_comments',
        })),

    path(route=r'api/v1/posts/<int:id>/comment/<int:comment_id>/', view=viewsets_api.PostViewSet.as_view(
        actions={
            'get': 'get_comment',
            'put': 'put_comment',
            'delete': 'delete_comment',
        })),

    # маршруты для view-функций и view-классов
    # path(route=r'api/v1/posts/', view=views_api.api_posts),
    # path(route=r'api/v1/posts/<int:id>/', view=views_api.api_posts_detail),  # view функция
    # path(route=r'api/v1/posts/<int:id>/', view=views_api.APIPostDetail.as_view()),
]
