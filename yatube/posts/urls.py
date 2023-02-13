from django.urls import path

from . import views

urlpatterns = [
    # адрес главной страницы
    path(route="", view=views.index, name="index"),

    # адрес страницы группы
    path(route="group/<slug:slug>/", view=views.group_posts, name="group_list"),

    # адрес страницы создания новой записи
    path(route="new/", view=views.new_post, name="new_post"),

    # Профайл пользователя
    path('<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
]
