from django.urls import path

from . import views

urlpatterns = [
    # адрес главной страницы
    path(route="", view=views.index, name="index"),

    # адрес страницы группы
    path(route="group/<slug:slug>/", view=views.group_posts, name="group_list"),

    # адрес страницы создания новой записи
    path(route="new/", view=views.new_post, name="new_post"),

    path("follow/", views.follow_index, name="follow_index"),

    # Профайл пользователя
    path('<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path("<username>/<int:post_id>/comment", views.add_comment, name="add_comment"),

    path("<str:username>/follow/", views.profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
]
