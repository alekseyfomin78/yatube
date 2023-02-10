from django import template
# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


# добавляем фильтр, который применяем в html шаблоне, фильтр добавляет css class к элементам формы
@register.filter
def addclass(field, css):
        return field.as_widget(attrs={"class": css})
