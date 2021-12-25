import hashlib

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from .models import User


def reg_view(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        user_name = request.POST['user_name']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        if password_1 != password_2:
            return HttpResponse('两次密码输入不一致')
        old_users = User.objects.filter(user_name=user_name)
        if old_users:
            return HttpResponse('用户名已注册')
        m = hashlib.md5()
        m.update(password_1.encode())  # 输入字节码
        password_m = m.hexdigest()
        # 防止并发注册导致的出错， 重复插入 唯一索引并发写入的问题
        try:
            user = User.objects.create(user_name=user_name, password=password_m)
            request.session['user_name'] = user_name
            request.session['uid'] = user.id
            return HttpResponseRedirect('/index')
        except Exception as e:
            print('--create user error %s' % e)
            return HttpResponse('用户名已注册')


def login_view(request):
    if request.method == 'GET':
        if is_login(request):
            return HttpResponseRedirect('/index')
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        user_name = request.POST['user_name']
        password = request.POST['password']
        try:
            user_info = User.objects.get(user_name=user_name)
            m = hashlib.md5()
            m.update(password.encode())
            if user_info.password == m.hexdigest():
                request.session['user_name'] = user_name
                request.session['uid'] = user_info.id
                resp = HttpResponseRedirect('/index')
                if 'remember' in request.POST:
                    resp.set_cookie('user_name', user_name, 3600 * 24 * 3)
                    resp.set_cookie('uid', user_info.id, 3600 * 24 * 3)
                return resp

            else:
                return HttpResponse('用户名或密码错误')
        except Exception as e:
            print('--login user error %s' % e)
            return HttpResponse('用户名或密码错误')


def is_login(request):
    if request.session.get('user_name') and request.session.get('uid'):
        return True
    c_user_name = request.COOKIES.get('user_name')
    c_uid = request.COOKIES.get('uid')
    if c_user_name and c_uid:
        # 此方法可能会session劫持，cookies伪造等问题
        request.session['user_name'] = c_user_name
        request.session['uid'] = c_uid
        return True
    return False


def logout_view(request):
    if request.session.get('user_name'):
        del request.session['user_name']
    if request.session.get('uid'):
        del request.session['uid']
    resp = HttpResponseRedirect('/index')
    if request.COOKIES.get('user_name'):
        resp.delete_cookie('user_name')
    if request.COOKIES.get('uid'):
        resp.delete_cookie('uid')
    return resp
