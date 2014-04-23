#!/usr/bin/env python
# coding=utf-8

import requests
import sys  
  
reload(sys)  
sys.setdefaultencoding('utf8')   

req = requests.Session()
req.get('http://jw.qdu.edu.cn/homepage/index.do')
image = req.get("http://jw.qdu.edu.cn/academic/getCaptcha.do?")

'''
from PIL import Image
from StringIO import StringIO
i = Image.open(StringIO(z.content))
'''

image_file = open("image", "wb")
image_file.write(image.content)
image_file.close()

captcha = input("captcha: ")


username = '201140705003'
passcode = 'xin1003'
payload = {'j_username' : username, 'j_password' : passcode,'j_captcha' : captcha}
req.post('http://jw.qdu.edu.cn/academic/j_acegi_security_check', params = payload)


params = {'id' : '410343', 'yearid':'34', 'termid' : '1', 'timetableType' : 'STUDENT', 'sectionType' : 'BASE'} 
class_html = req.get("http://jw.qdu.edu.cn/academic/manager/coursearrange/showTimetable.do", params = params)
#params = {'yearid':'34', 'termid' : '1'} 
#class_html = req.get('http://jw.qdu.edu.cn/academic/student/currcourse/currcourse.jsdo', params=params)


html = open("htmlBAS", 'w')
html.write(class_html.text)
html.close()
#print class_html.status_code
#print class_html.text
