from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    """
    Функция для представления главной страницы.

    :param request:
    :return: шаблон главной страницы, в который объединяет 10 свежих по дате публикации постов в один общий текст
    """
    # select всех записей модели Post, сортируем по дате (знак "-" означает DESC, сначала большие даты, т.е.
    # самые свежие) и выводим топ10
    latest = Post.objects.all()[:11]
    template = "index.html"
    context = {"posts": latest}

    return render(
        request,  # первый аргумент всегда request
        template,  # файл шаблона, который будет показан пользователю
        context,  # передача данных в шаблон, осуществляется через словарь
    )


def group_posts(request, slug):
    """
    Функция для представления страницы группы.

    :param request:
    :param slug: название группы

    :return: шаблон страницы группы, в который вставляет топ12 свежих по дате публикации постов конкретно заданной группы
    """

    # функция get_object_or_404 получает по заданным критериям объект из базы данных или возвращает сообщение об ошибке,
    # если объект не найден
    group = get_object_or_404(Group, slug=slug)

    # Метод .filter позволяет ограничить поиск по критериям. Это аналог добавления условия WHERE group_id = {group_id}
    # posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    posts = group.posts.all()[:12]  # используем related_name модели Group

    template = "group.html"
    context = {"group": group, "posts": posts}

    return render(request, template, context)

