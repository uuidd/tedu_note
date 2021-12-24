from django.shortcuts import render


# Create your views here.
from user.views import is_login


def index_view(request):
    if is_login(request):
        print(locals())
        return render(request, 'index/index2.html', locals())
    else:
        return render(request, "index/index.html")
