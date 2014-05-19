from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from jw.models import Account
from jw.link_jw import DataCapture
from jw.resolve import is_login, Lesson
from jw.models import Curriculum
#from django.shortcuts import redirect, render

def index(request):
    '''index'''

    data_capture = DataCapture()
    request.session['data_capture'] = data_capture

    response = {'status' : '200'}

    return HttpResponse(simplejson.dumps(response))


def captcha(request):
    ''' Get captcha '''

    ''''''
    a = request.session.get('a', 0)
    request.session['a'] = a + 1
    print a + 1

    data_capture = request.session.get('data_capture', DataCapture())
    request.session['data_capture'] = data_capture
    image = data_capture.get_captcha()
    response = HttpResponse(image, mimetype='image/png')
    #response['Content-Disposition'] = 'attachment; filename=captcha.png'
    response['Content-Disposition'] = 'inline; filename=captcha.png'
    return response

def __login_jw(request, s_id, s_passcode, captcha):

    data_capture = request.session.get('data_capture')
    if data_capture == None:
        #701 is data capture session do not exist
        return 701
    result = data_capture.login(s_id, s_passcode, captcha)
    status = is_login(result)
    request.session['status'] = status

    return status

def login_jw(request):

    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        s_passcode = request.POST.get('s_passcode')
        captcha = request.POST.get('captcha')
        status = __login_jw(request, s_id, s_passcode, captcha)
        return HttpResponse(simplejson.dumps({'status' : status}))
    return HttpResponse(simplejson.dumps({"status" : 'hehe'}))

def login_client(request):

    if request.method == 'POST':
        username = request.POST.get('usernanme')
        c_passcode = request.POST.get('c_passcode')
        
        account = authenticate(username=username, password=c_passcode)

        if isinstance(account, User):
            login(request, account)
            return HttpResponse(simplejson.dumps({'status' : 200}))

        return HttpResponse(simplejson.dumps({'status' : 600}))

    return HttpResponse(simplejson.dumps({"status" : 'hehe'}))

def get_lesson(request):
    '''Get lessons'''

    if request.session.get('status') == 200:
        data_capture = request.session.get('data_capture')
        lesson = Lesson(data_capture.get_lesson_html())
        response = lesson.get_lesson()
        return HttpResponse(simplejson.dumps(response))

    return HttpResponse(simplejson.dumps({'status' : 600}))

def registration(request):

    if request.method == 'POST':
        sex = request.POST.get('sex')
        s_id = request.POST.get('s_id')
        s_passcode = request.POST.get('s_passcode')
        captcha = request.POST.get('captcha')
        c_passcode = request.POST.get('c_passcode')

        if User.objects.filter(username=s_id).exists():
            return HttpResponse(simplejson.dumps({'status' : 201}))

        status = __login_jw(request, s_id, s_passcode, captcha)
        if status == 200:

            user = User.objects.create_user(s_id,
                    'lennon@thebeatles.com', c_passcode)
            account = Account.objects.create(user=user, student_id=s_id,
                    student_passcode=s_passcode, sex=sex)
            account.save()
        return HttpResponse(simplejson.dumps({'status' : status}))
    return HttpResponse(simplejson.dumps({"status" : 'hehe'}))

'''
        sex = 1
        s_id = 201140705003
        s_passcode = 'xin1003'
        c_passcode = 123

'''
