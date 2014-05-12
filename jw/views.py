
from django.http import HttpResponse
from django.utils import simplejson
from link_jw import DataCapture
from resolve import is_login
#from django.shortcuts import redirect, render

def index(request):
    '''index'''

    data_capture = DataCapture()
    request.session['data_capture'] = data_capture

    response = {'status' : '200'}

    return HttpResponse(simplejson.dumps(response))


def captcha(request):
    ''' Get captcha '''

    data_capture = request.session.get('data_capture', DataCapture())
    request.session['data_capture'] = data_capture
    image = data_capture.get_captcha()
    response = HttpResponse(image, mimetype='image/png')
    #response['Content-Disposition'] = 'attachment; filename=captcha.png'
    response['Content-Disposition'] = 'inline; filename=captcha.png'
    return response

def login_jw(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        captcha = request.POST.get('captcha')
        data_capture = request.session.get('data_capture')

        if data_capture == None:
            '''701 is data captcha session do not exist'''
            response = {'status' : '701'}
            return HttpResponse(simplejson.dumps(response))
        result = data_capture.login(username, password, captcha)
        status = is_login(result);
        return HttpResponse(simplejson.dumps({'status' : status}))
    return HttpResponse('hehe')

