from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Group, User, Follow, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404, reverse
from django.core.paginator import Paginator


class PostsListView(ListView):
    """
    Главная страница, вывод всех постов, аналог view функции index
    """
    model = Post
    template_name = 'index/index.html'
    paginate_by = 10
    # в context по умолчанию передадутся: paginator, page_obj - страница, object_list - посты


class GroupPostsListView(ListView):
    """
    Cтраница группы, вывод всех постов группы, аналог view функции group_posts
    """
    template_name = "group/group.html"
    paginate_by = 10

    # переопределим запрос к БД, чтобы получать посты конкретной группы (slug)
    def get_queryset(self):
        self.group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return self.group.posts.all()

    # добавим в context переменную group
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['group'] = self.group
        return context


class NewPostCreateView(LoginRequiredMixin, CreateView):
    """
    Страница добавления нового поста, аналог view функции new_post
    """
    model = Post
    template_name = "posts/new_post.html"
    form_class = PostForm

    def form_valid(self, form):
        temp_form = form.save(commit=False)
        temp_form.author = self.request.user
        temp_form.save()
        return super().form_valid(form)

    def get_success_url(self):  # в случае валидности формы перенаправляем пользователя на главную страницу
        return reverse('index')


class ProfileDetailView(DetailView):
    """
    Профиль пользователя, аналог view функции profile
    """
    model = User
    template_name = 'posts/profile.html'
    slug_field = 'username'  # detailview нужно передать либо pk, либо slug, поэтому переопределим переменную на 'username'
    context_object_name = 'author'  # переопределим переменную контекста с object на author

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        following = self.object.following.filter(user=self.request.user)
        follower = self.object.follower.filter(user=self.request.user)
        context['following'] = following
        context['follower'] = follower

        post_list = self.object.posts.all()
        paginator = Paginator(post_list, 10)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return context


class PostDetailView(DetailView):
    """
    Страница просмотра поста, аналог view функции post_view
    """
    model = Post
    template_name = 'posts/post_view.html'

    # в path нужно передать два параметра, переопределяем их
    slug_field = 'username'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        author = self.object.author
        following = author.following.filter(user=self.request.user)
        follower = author.follower.filter(user=self.request.user)
        context['author'] = author
        context['follower'] = follower
        context['following'] = following
        return context


class PostEditView(LoginRequiredMixin, UpdateView):
    """
    Страница редактирования поста, аналог view функции post_edit
    """
    model = Post
    template_name = 'posts/new_post.html'
    form_class = PostForm

    # в path нужно передать два параметра, переопределяем их
    slug_field = 'username'
    pk_url_kwarg = 'post_id'

    # переопределяем запрос к БД, чтобы получать посты созданные только текущим пользователем
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    # в случае валидности формы перенаправляем пользователя на страницу поста
    def get_success_url(self):
        return reverse('post', kwargs={'username': self.request.user, 'post_id': self.object.id})


# class AddCommentView(LoginRequiredMixin, CreateView):
#     """
#     Страница добавления комментария к посту, аналог view функции add_comment
#     """
#     model = Comment
#     template_name = 'posts/comments.html'
#     form_class = CommentForm
#
#     slug_field = 'username'
#     pk_url_kwarg = 'post_id'
#
#     def get_slug_field(self):
#         q = super().get_slug_field()
#         print('slug', q)
#         return q
#
#     def get_queryset(self):
#         q = super().get_queryset()
#         print(q)
#         return q
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(object_list=object_list, **kwargs)
#         #context['post'] = self.object.post
#         print('context: ', context)
#         return context
#
#     def form_valid(self, form):
#         temp_form = form.save(commit=False)
#         temp_form.author = self.request.user
#         #temp_form.post =
#         temp_form.save()
#         return super().form_valid(form)


class FollowPostsListView(LoginRequiredMixin, ListView):
    """
    Страница с постами авторов, на которых подписан пользователь, аналог view функции follow_index
    """
    model = Post
    template_name = 'posts/follow.html'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(author__following__user=self.request.user)
