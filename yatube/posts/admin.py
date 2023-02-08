from django.contrib import admin
from .models import Post, Group


# чтобы на сайте админа ("localhost:8000/admin/") модель Post отображалась так как мы хотим,
# создатим конфигурацию для модели Post
class PostAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке, "pk" - первычный ключ поста
    list_display = ("pk", "text", "pub_date", "author")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",)
    # добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"  # это свойство сработает для всех колонок: где пусто - там будет эта строка


class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    search_fields = ("title",)
    empty_value_display = "-пусто-"


# при регистрации модели Post источником конфигурации для неё назначаем класс PostAdmin
admin.site.register(Post, PostAdmin)

admin.site.register(Group, GroupAdmin)


