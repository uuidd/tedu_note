from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import Note


def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'user_name' not in request.session or 'uid' not in request.session:
            # 检查cookies
            c_user_name = request.COOKIES.get('user_name')
            c_uid = request.COOKIES.get('uid')
            if not c_user_name or not c_uid:
                return HttpResponseRedirect('/user/login/')
            else:
                # 回写session
                request.session['user_name'] = c_user_name
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)

    return wrap


@check_login
def list_view(request):
    notes = Note.objects.filter(is_active=True)
    return render(request, 'note/list_note.html', locals())


@check_login
def add_view(request):
    if request.method == 'GET':
        return render(request, 'note/add_note.html')
    elif request.method == 'POST':
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content, user_id=uid)
        return HttpResponseRedirect('/note/all/')


def update_view(request, note_id):
    try:
        note = Note.objects.get(id=note_id, is_active=True)
    except Exception as e:
        print('--update note is error %s' % e)
        return HttpResponse('Note does not exist')
    if request.method == 'GET':
        return render(request, 'note/update_note.html', locals())
    elif request.method == 'POST':
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.save()
        return HttpResponseRedirect('/note/all/')


def delete_view(request):
    try:
        note = Note.objects.get(id=request.GET.get('note_id'), is_active=True)
    except Exception as e:
        print('--delete note is error %s' % e)
        return HttpResponse('Note does not exist')
    note.is_active = False
    note.save()
    return HttpResponseRedirect('/note/all/')