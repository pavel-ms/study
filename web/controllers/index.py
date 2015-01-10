from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from web.models import Car


@login_required(login_url='/auth/login')
def index(req):
    cars = Car.objects.all()
    return render(req, 'index.html', {"cars": cars})
