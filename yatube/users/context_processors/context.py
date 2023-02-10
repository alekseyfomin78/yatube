import datetime as dt


def year(request):
    """ Добавляем переменную с текущим годом"""
    actual_year = dt.datetime.now().year
    return {'year': actual_year}
