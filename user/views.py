import hashlib

from django.http import HttpResponse
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
            return HttpResponse('注册成功')
        except Exception as e:
            print('--create user error %s' % e)
            return HttpResponse('用户名已注册')


def login_view(request):
    if request.method == 'GET':
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
                return HttpResponse('登陆成功')
            else:
                return HttpResponse('用户名或密码错误')
        except Exception as e:
            print('--login user error %s' % e)
            return HttpResponse('用户名或密码错误')


