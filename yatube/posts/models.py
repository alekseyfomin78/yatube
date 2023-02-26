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

    image: изображение, аргумент upload_to указывает, куда должны загружаться пользовательские файлы,
    Путь к директории для загрузки изображений указывается относительно адреса в параметре конфигурации MEDIA_ROOT,
    который должен содержать полный путь к директории и не должен совпадать с директорией STATIC_ROOT
    """
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.SET_NULL, related_name="posts")
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    # модель автоматически сортируется по свежести даты публикации, "-" означает DESC
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

