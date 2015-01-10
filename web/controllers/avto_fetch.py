import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from web.components.parser import Parser


@login_required(login_url='/auth/login')
def index(req):
    p = Parser()
    p.parse()
    return HttpResponse(json.dumps({}), content_type="application/json")
