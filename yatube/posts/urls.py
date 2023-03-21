from django.urls import path
from . import views
from . import views_class_based


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

    # профайл пользователя
    # path('<str:username>/', views.profile, name='profile'),
    path('<str:slug>/', views_class_based.ProfileDetailView.as_view(), name='profile'),

    path("<str:username>/follow/", views.profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),

    # просмотр поста
    # path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/', views_class_based.PostDetailView.as_view(), name='post'),

    # редактирование поста
    # path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('<str:username>/<int:post_id>/edit/', views_class_based.PostEditView.as_view(), name='post_edit'),

    # добавление комментария
    path("<str:username>/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    # path("<str:username>/<int:post_id>/comment/", views_class_based.AddCommentView.as_view(), name="add_comment"),
]
