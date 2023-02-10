from django.db import models
from django.contrib.auth import get_user_model

# модель User импортируется именно таким способом
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
    text: текстовое поле поста.

    pub_date: дата публикации поста, тип DateTimeField, текст "date published" это заголовок поля в интерфейсе
    администратора. auto_now_add говорит, что при создании новой записи автоматически будет подставлено текущее время и
    дата.

    author: ссылка на автора поста, на модель User; Внешний ключ к Первичному ключу модели Users;
    on_delete=models.CASCADE означает, что если в таблице Users удаляется пользователь, то и из таблицы Posts удаляться
    все посты этого пользователя;
    это поле ссылается на автора поста, на модель User, и для этого поля указано свойство related_name="posts";
    Т.е. в каждом объекте модели User автоматически будет создано свойство с таким же названием (posts), и в нём будут
    храниться ссылки на все объекты модели Post, которые ссылаются на объект User. На практике это означает, что
    в объекте записи есть поле author, в котором хранится ссылка на автора(например, admin), а в объекте пользователя
    admin появилось поле posts, в котором хранятся ссылки на все посты этого автора. И теперь можно получить список
    постов автора, обратившись к его свойству posts.

    group: ссылка на группу, на модель Group
    """
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.SET_NULL, related_name="posts")

    # модель автоматически сортируется по свежести даты публикации, "-" означает DESC
    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
