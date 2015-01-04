from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context


def index(req):
    t = get_template('index.html')
    return HttpResponse(t.render(Context()))
