#!/usr/bin/env python
# coding=utf-8

from StringIO import StringIO
import sys
reload(sys)  
sys.setdefaultencoding('utf8')   

import requests
from bs4 import BeautifulSoup

class Data_capture(object):

   
    __home_url = r'http://jw.qdu.edu.cn/homepage/index.do'
    __captcha_url = r'http://jw.qdu.edu.cn/academic/getCaptcha.do?'

    def __init__(self):

       self. __req_session = requests.Session()

    def get_captcha(self):

        self.__req_session.get(Data_capture.__home_url)

        captcha_image = self.__req_session.get(Data_capture.__captcha)

        image_file = open("image", "wb")
        image_file.write(captcha_image.content)
        image_file.close()

        return StringIO(captcha_image.content)

    def login(self, username, passcode, captcha):

        login_url = r'ihttp://jw.qdu.edu.cn/academic/j_acegi_security_check'
        self.__username = username
        self.__passcode = passcode
        self.__captcha = captcha
        payload = {'j_username' : self.__username,
                   'j_password' : self.__passcode,
                   'j_captcha' : self.__captcha}        

        self.__req_session.post(login_url, params = payload)







