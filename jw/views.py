
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from jw.models import Account
from jw.link_jw import DataCapture
from jw.resolve import is_login, Lesson_student, get_student_info
from jw.models import Curriculum, Lesson
#from django.shortcuts import redirect, render

def index(request):
    '''index'''

    data_capture = DataCapture()
    request.session['data_capture'] = data_capture
    response = {'status' : '200'}

    return HttpResponse(simplejson.dumps(response))

def captcha(request):
    ''' Get captcha '''

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
        c_id = request.POST.get('c_id')
        c_passcode = request.POST.get('c_passcode')
        user = authenticate(username=c_id, password=c_passcode)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(simplejson.dumps({"status" : '200'}))
            return HttpResponse(simplejson.dumps({"status" : '201'}))
        return HttpResponse(simplejson.dumps({"status" : '404'}))
    return HttpResponse(simplejson.dumps({"status" : 'hehe'}))

def not_logged_in(request):

    return HttpResponse(simplejson.dumps({"status" : '600'}))

@login_required(login_url='not_logged_in')
def student_info(request):
    '''get student info'''
    if request.method == 'GET':
        infos = request.user.account.get_student_info()
        return HttpResponse(simplejson.dumps(infos))
    return HttpResponse(simplejson.dumps({"status" : 'hehe'}))
    
    
@login_required(login_url='not_logged_in')
def get_lesson(request):
    '''Get lessons'''
    if request.method == 'GET':
        year = request.GET.get('year', 2014)
        term_id = request.GET.get('term_id', 1)
        account = request.user.account
        curriculum = Curriculum.objects.filter(year=year,
                             term=term_id, user=account)
        if curriculum.exists():
            lessons = []
            for var in curriculum[0].lesson_set.all():
                lessons.append(var.get_lesson_dict())
            return HttpResponse(simplejson.dumps(lessons))

        curriculum = Curriculum(user=account, year=year, term=term_id)
        curriculum.save()

        if request.session.get('status') == 200:
            data_capture = request.session.get('data_capture')
            lesson_student = Lesson_student(
                    data_capture.get_lesson_html(year, term_id))
            response = lesson_student.get_lesson()
            for var in response:
                lesson_sq = Lesson(curriculum=curriculum, **var)
                lesson_sq.save()
            return HttpResponse(simplejson.dumps(response))

        return HttpResponse(simplejson.dumps({'status' : 600}))
    return HttpResponse(simplejson.dumps({"status" : 'hehe'}))

def registration(request):

    if request.method == 'POST':
        #sex = request.POST.get('sex')
        s_id = request.POST.get('s_id')
        s_passcode = request.POST.get('s_passcode')
        captcha = request.POST.get('captcha')
        c_passcode = request.POST.get('c_passcode')

        if User.objects.filter(username=s_id).exists():
            return HttpResponse(simplejson.dumps({'status' : 210}))

        status = __login_jw(request, s_id, s_passcode, captcha)
        if status == 200:
            data_capture = request.session.get('data_capture')
            info_html = data_capture.get_info_html()
            info_dict = get_student_info(info_html)
            user = User.objects.create_user(s_id,
                    'lennon@thebeatles.com', c_passcode)
            account = Account.objects.create(user=user,
                         student_passcode=s_passcode, **info_dict)
            return redirect('login_client')
        return HttpResponse(simplejson.dumps({'status' : status}))
    return HttpResponse(simplejson.dumps({"status" : 'hehe'}))

'''
        sex = 1
        s_id = 201140705003
        s_passcode = 'xin1003'
        c_passcode = 123
        s_id = '201140705003'
        s_passcode = 'xin1003'
        c_id = '201140705001'
        c_passcode = 'xin'
        c_id = '201240703057'
        c_passcode = 'xin'
        s_id = '201240703057'
        s_passcode = 'ZCBM13579XVN'
        c_passcode = 'xin'
'''
