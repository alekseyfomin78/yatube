from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    """
    Функция для представления главной страницы.

    :param request:
    :return: шаблон главной страницы, содержащий все посты
    """

    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением

    template = "index.html"
    context = {'page': page, 'paginator': paginator}

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

    :return: шаблон страницы группы, содержащий посты только заданной группы
    """

    # функция get_object_or_404 получает по заданным критериям объект из базы данных или возвращает сообщение об ошибке,
    # если объект не найден
    group = get_object_or_404(Group, slug=slug)

    post_list = group.posts.all()  # используем related_name модели Group
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением

    template = "group.html"
    context = {"group": group, 'page': page, 'paginator': paginator}

    return render(request, template, context)


@login_required()
def new_post(request):
    """
    Добавить новую запись, доступно для авторизованного пользователя.

    :return: в случае успешной валидации формы перенаправление на главную страницу и сохранение данных из форма в БД,
    иначе страница не меняется и данные не сохраняются
    """
    template = "new_post.html"

    form = PostForm(request.POST or None)

    # валидация формы, в случае успеха сохраняем данные в БД и перенаправляем
    if form.is_valid():
        temp_form = form.save(commit=False)
        temp_form.author = request.user  # получаем текущего пользователя
        temp_form.save()
        # в случае успешной валидации перенаправляем на главную страницу
        return redirect('index')

    return render(request, template, {'form': form})


def profile(request, username):
    """
    Профиль пользователя.

    :param username:
    :return: страница профиль пользователя и записи этого пользователя
    """
    template = 'profile.html'
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'author': author, 'page': page}
    return render(request, template, context)


def post_view(request, username, post_id):
    """
    Просмотр записи пользователя.

    :param username:
    :param post_id:
    :return: страница записи, содержащая полную информацию об этой записи
    """
    template = 'post.html'
    author = get_object_or_404(User, username=username)
    post = author.posts.filter(pk=post_id)
    context = {'author': author, 'post': post}
    return render(request, template, context)


def post_edit(request, username, post_id):
    """
    Редактирование записи.

    :param username:
    :param post_id:
    :return: если текущий пользователь - это автор записи, то возвращается страница редактирования записи, иначе
    страница просмотра записи
    """
    template = 'new_post.html'

    author = get_object_or_404(User, username=username)
    post = author.posts.filter(pk=post_id)
    # проверка что текущий пользователь - это автор записи
    if author != request.user:
        return redirect('post_view', username, post_id)

    form = PostForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('post_view', username, post_id)

    return render(request, template, {'form': form, 'post': post})



