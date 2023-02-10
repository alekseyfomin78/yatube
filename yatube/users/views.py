from django.views.generic import CreateView
from .forms import CreationForm

#  функция reverse_lazy позволяет получить URL по параметру "name" функции path()
from django.urls import reverse_lazy


# класс представления регистрации
class SignUp(CreateView):
    # Всё это чем-то похоже на вызов функции render() во view-функции

    form_class = CreationForm  # определяем форму регистрации

    # перенаправление пользователя после успешной отправки формы
    success_url = reverse_lazy("login")  # где login — это параметр "name" в path()

    # имя шаблона, куда будет передана переменная form с объектом HTML-формы.
    template_name = "signup.html"
