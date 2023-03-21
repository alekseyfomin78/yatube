from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    """
    Модель Group.

    title: имя группы.
    slug: уникальный адрес группы, часть URL.
    description: описание сообщества.

    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Модель Post.
    text: текстовое поле поста
    pub_date: дата публикации поста
    author: ссылка на автора поста, на модель User
    group: ссылка на группу, на модель Group
    image: изображение
    """
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.SET_NULL, related_name="posts")
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель комментария

    post: ссылка на пост, к которому оставлен комментарий
    author: ссылка на автора комментария
    text: текст комментария
    created: автоматически подставляемые дата и время публикации комментария
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField("date created", auto_now_add=True)

    class Meta:
        ordering = ["-created"]


class Follow(models.Model):
    """
    Модель подписки на авторов

    user: ссылка на объект пользователя, который подписывается
    author: ссылка на объект пользователя, на которого подписываются
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

