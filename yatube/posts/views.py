from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Group, User, Follow, Comment
from .forms import PostForm, CommentForm
from django.views.decorators.cache import cache_page


# @cache_page(20)  # кэширование страницы, обновление(запрос к БД и т.д) страницы происходит раз в 20 сек.
def index(request):
    """
    Функция для представления главной страницы.

    :param request:
    :return: шаблон главной страницы, содержащий все посты
    """

    template = "index/index.html"

    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением

    context = {'page_obj': page, 'paginator': paginator}

    return render(request, template, context)


def group_posts(request, slug):
    """
    Функция для представления страницы группы.

    :param request:
    :param slug: название группы

    :return: шаблон страницы группы, содержащий посты только заданной группы
    """

    template = "group/group.html"

    # функция get_object_or_404 получает по заданным критериям объект из базы данных или возвращает сообщение об ошибке,
    # если объект не найден
    group = get_object_or_404(Group, slug=slug)

    post_list = group.posts.all()  # используем related_name модели Group
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением

    context = {"group": group, 'page_obj': page, 'paginator': paginator}

    return render(request, template, context)


@login_required()
def new_post(request):
    """
    Добавить новую запись, доступно для авторизованного пользователя.

    :return: в случае успешной валидации формы перенаправление на главную страницу и сохранение данных из форма в БД,
    иначе страница не меняется и данные не сохраняются
    """
    template = "posts/new_post.html"

    # определяем форму и получаем данные введеные пользователем
    form = PostForm(request.POST or None, files=request.FILES or None)

    # если данные в форме валидны, то сохраняем данные в БД и перенаправляем пользователя
    if form.is_valid():
        temp_form = form.save(commit=False)  # не сохраняем форму в БД, т.к. еще нужно добавить пользователя в форму
        temp_form.author = request.user  # добавляем текущего пользователя в форму
        temp_form.save()  # сохраняем форму в БД
        # в случае успешной валидации перенаправляем на главную страницу
        return redirect('index')

    return render(request, template, {'form': form})


def profile(request, username):
    """
    Профиль пользователя.

    :param request:
    :param username:
    :return: страница профиль пользователя и записи этого пользователя
    """

    template = 'posts/profile.html'

    author = get_object_or_404(User, username=username)

    following = author.following.filter(user=request.user)  # подписчики
    follower = author.follower.filter(user=request.user)  # свои подписки

    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'author': author, 'page': page, 'follower': follower, 'following': following}

    return render(request, template, context)


def post_view(request, username, post_id):
    """
    Просмотр записи пользователя.

    :param request:
    :param username:
    :param post_id:
    :return: страница записи, содержащая полную информацию об этой записи
    """
    template = 'posts/post_view.html'

    author = get_object_or_404(User, username=username)

    following = author.following.filter(user=request.user)  # подписчики
    follower = author.follower.filter(user=request.user)  # свои подписки

    post = author.posts.filter(pk=post_id).first()

    context = {'author': author, 'post': post, 'following': following, 'follower': follower}

    return render(request, template, context)


@login_required()
def post_edit(request, username, post_id):
    """
    Редактирование записи.

    :param request:
    :param username:
    :param post_id:
    :return: если текущий пользователь - это автор записи, то возвращается страница редактирования записи, иначе
    страница просмотра записи
    """
    template = 'posts/new_post.html'

    author = get_object_or_404(User, username=username)
    post = author.posts.filter(pk=post_id).first()

    # проверка что текущий пользователь - это автор записи
    if author != request.user:
        return redirect('post', username, post_id)

    # определяем форму и получаем данные введенные пользователем
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)

    # если данные в форме валидны, то сохраняем данные в БД и перенаправляем пользователя
    if form.is_valid():
        form.save()
        return redirect('post', username, post_id)

    return render(request, template, {'form': form, 'post': post})


@login_required()
def add_comment(request, username, post_id):
    """
    Добавление комментария к посту

    :param request:
    :param post_id:
    :return:
    """
    template = 'posts/comments.html'

    post = get_object_or_404(Post, pk=post_id)

    items = post.comments.all()  # комметарии к посту

    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        form.save()
        return redirect('post', username=post.author.username, post_id=post_id)

    return render(request, template, {'form': form, 'post': post, 'items': items})


def page_not_found(request, exception):
    """
    Страница 404 ошибки

    :param request:
    :param exception:
    :return:
    """
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    """
    Страница 500 ошибки

    :param request:
    :return:
    """
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    """
    Страница с постами авторов, на которых подписан пользователь

    :param request:
    :return:
    """
    template = 'posts/follow.html'

    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page_obj': page}

    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """
    Подписаться на пользователя

    :param request:
    :param username:
    :return:
    """
    follow_author = get_object_or_404(User, username=username)

    if follow_author != request.user and (not request.user.follower.filter(author=follow_author).exists()):
        Follow.objects.create(user=request.user, author=follow_author)  # создаем подписчика в БД

    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    """
    Отписаться от пользователя

    :param request:
    :param username:
    :return:
    """

    follow_author = get_object_or_404(User, username=username)
    data_follow = request.user.follower.filter(author=follow_author)

    if data_follow.exists():
        data_follow.delete()  # удаляем подписчика из БД

    return redirect('profile', username)
