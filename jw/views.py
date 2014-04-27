
from django.http import HttpResponse
from django.utils import simplejson
from lesson import DataCapture
#from django.shortcuts import redirect, render

def index(request):
    '''index'''

    data_capture = DataCapture()
    if 'a' in request.session:
        request.session['a'] += 1
    else:
        request.session['a'] = 0

    print request.session['a']
    #print request.session
    image = data_capture.get_captcha()
    #resonse = {'status' : '200', 'image' : image}
    #return HttpResponse(simplejson.dumps(resonse))
    response = HttpResponse(image, mimetype='image/png')
    #response['Content-Disposition'] = 'attachment; filename=captcha.png'

    response['Content-Disposition'] = 'inline; filename=captcha.png'
    return response


def captcha(request):
    pass

