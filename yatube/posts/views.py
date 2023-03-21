from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Group, User, Follow, Comment
from .forms import PostForm, CommentForm
from django.views.decorators.cache import cache_page


# @cache_page(20)
def index(request):
    """
    Функция для представления главной страницы
    """

    template = "index/index.html"

    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page_obj': page, 'paginator': paginator}

    return render(request, template, context)


def group_posts(request, slug):
    """
    Функция для представления страницы группы
    """

    template = "group/group.html"

    group = get_object_or_404(Group, slug=slug)

    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {"group": group, 'page_obj': page, 'paginator': paginator}

    return render(request, template, context)


@login_required()
def new_post(request):
    """
    Добавить новый пост, доступно для авторизованного пользователя
    """
    template = "posts/new_post.html"

    form = PostForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        temp_form = form.save(commit=False)
        temp_form.author = request.user
        temp_form.save()
        return redirect('index')

    return render(request, template, {'form': form})


def profile(request, username):
    """
    Профиль пользователя
    """

    template = 'posts/profile.html'

    author = get_object_or_404(User, username=username)

    following = author.following.filter(user=request.user)
    follower = author.follower.filter(user=request.user)

    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'author': author, 'page': page, 'follower': follower, 'following': following}

    return render(request, template, context)


def post_view(request, username, post_id):
    """
    Просмотр поста
    """
    template = 'posts/post_view.html'

    author = get_object_or_404(User, username=username)

    following = author.following.filter(user=request.user)
    follower = author.follower.filter(user=request.user)

    post = author.posts.filter(pk=post_id).first()

    context = {'author': author, 'post': post, 'following': following, 'follower': follower}

    return render(request, template, context)


@login_required()
def post_edit(request, username, post_id):
    """
    Редактирование записи
    """
    template = 'posts/new_post.html'

    author = get_object_or_404(User, username=username)
    post = author.posts.filter(pk=post_id).first()

    if author != request.user:
        return redirect('post', username, post_id)

    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('post', username, post_id)

    return render(request, template, {'form': form, 'post': post})


@login_required()
def add_comment(request, username, post_id):
    """
    Добавление комментария к посту
    """
    template = 'posts/comments.html'

    post = get_object_or_404(Post, pk=post_id)

    items = post.comments.all()

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
    """
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    """
    Страница 500 ошибки
    """
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    """
    Страница с постами авторов, на которых подписан пользователь
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
    """
    follow_author = get_object_or_404(User, username=username)

    if follow_author != request.user and (not request.user.follower.filter(author=follow_author).exists()):
        Follow.objects.create(user=request.user, author=follow_author)

    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    """
    Отписаться от пользователя
    """

    follow_author = get_object_or_404(User, username=username)
    data_follow = request.user.follower.filter(author=follow_author)

    if data_follow.exists():
        data_follow.delete()

    return redirect('profile', username)
