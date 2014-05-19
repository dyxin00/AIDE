'''lesson'''
#!/usr/bin/env python
# coding=utf-8

from StringIO import StringIO

from bs4 import BeautifulSoup
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf8')   

class DataCapture(object):
    '''JW'''
    __home_url = r'http://jw.qdu.edu.cn/homepage/index.do'
    __captcha_url = r'http://jw.qdu.edu.cn/academic/getCaptcha.do?'
    def __init__(self):
        self.__username = None
        self.__captcha = None
        self.__passcode = None
        self.__req_session = requests.Session()


    def get_captcha(self):

        '''retrun captcha'''
        self.__req_session.get(DataCapture.__home_url)
        captcha_image = self.__req_session.get(DataCapture.__captcha_url)

        '''
        image_file = open("image", "wb")
        image_file.write(captcha_image.content)
        image_file.close()
        '''
        return StringIO(captcha_image.content)

    def login(self, username, passcode, captcha):

        '''login Jw'''
        login_url = r'http://jw.qdu.edu.cn/academic/j_acegi_security_check'
        self.__username = username
        self.__passcode = passcode
        self.__captcha = captcha
        payload = {'j_username' : self.__username,
                   'j_password' : self.__passcode,
                   'j_captcha' : self.__captcha}

        result = self.__req_session.post(login_url, params=payload)
        if result.status_code != requests.codes.ok:
            result.raise_for_status()
        return result.text

    def get_lesson_html(self, year=2014, term_id=1):

        '''Get html Data'''

        url = 'http://jw.qdu.edu.cn/academic/student/currcourse/currcourse.jsdo'
        year_id = 34
        if year != 2014:
            year_id = int(year) - 2014 + 34
        '''
        params = {'id' : '410343', 'yearid' : year_id,
                  'termid' : trem_id, 'timetableType' : 'STUDENT',
                  'sectionType' : 'BASE'}
        '''
        params = {'year' : year_id, 'term' : term_id}
        __request_html = self.__req_session.get(url, params=params)
        return __request_html.text

if __name__ == '__main__':

    data = DataCapture()
    data.get_captcha()
    cap = input('captcha :' )
    e = data.login('201240703057', 'ZCBM13579XVN', cap)
    import resolve
    print resolve.is_login(e)
    
