
from django.http import HttpResponse
from django.utils import simplejson
from link_jw import DataCapture
from resolve import is_login, Lesson
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

def login_jw(request):

    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        captcha = request.GET.get('captcha')
        data_capture = request.session.get('data_capture')

        if data_capture == None:
            '''701 is data captcha session do not exist'''
            response = {'status' : '701'}
            return HttpResponse(simplejson.dumps(response))
        result = data_capture.login(username, password, captcha)
        status = is_login(result);

        request.session['status'] = status
        return HttpResponse(simplejson.dumps({'status' : status}))
    return HttpResponse('hehe')


def get_lesson(request):

    if request.session.get('status') == 200:
        data_capture = request.session.get('data_capture')

        lesson = Lesson(data_capture.get_lesson_html())
        response = lesson.get_lesson()
        return HttpResponse(simplejson.dumps(response))

    return HttpResponse(simplejson.dumps({'status' : 600}))

