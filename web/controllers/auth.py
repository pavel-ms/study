from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as user_login, logout as user_logout


def login(req):
    """
    Функция отрисовывает форму авторизации для пользователя.
    Если запрос типа пост и в нем содержатся поля username и password, то
    пытается авторизовать пользователя и в случае успешной авторизации
    редиректит его на главную страницу
    @link http://solutoire.com/2009/02/26/django-series-1-a-custom-login-page/
    """
    err = False
    if req.POST:
        username = req.POST['username']
        password = req.POST['password']
        usr = authenticate(username=username, password=password)
        if usr is not None:
            if usr.is_active:
                user_login(req, usr)
                return HttpResponseRedirect('/')
            else:
                err = 'Данные пользователь не активен!'
        else:
            err = 'Такого пользователя не существует!'
    return render(req, 'login.html', dictionary={"err": err})


def logout(req):
    """
    Функция удалает у пользователя cookie авторизации
    соответственно его разлогинивает
    """
    user_logout(req)
    return HttpResponseRedirect('/auth/login')