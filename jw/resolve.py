#coding=utf-8

from bs4 import BeautifulSoup
import re
import sys
#reload(sys) sys.setdefaultencoding('utf8')

'''
f = open("html", 'r')
try:
    html = f.read()
finally:
    f.close();
'''
class Lesson_student(object):

    def __init__(self, html):

        self.html = html
        self.soup = BeautifulSoup(self.html.encode('utf8'),
                                  'lxml', from_encoding='utf8')

    def __eliminate_gaps(self, s):

        return ''.join(s.split())


    def __screening_digital(self, s):

        data = self.__eliminate_gaps(s)
        if '-' in data:
            return data.split('-')
        elif '、' in data:
            return data.split('、')
        else:
            return [data, data]

    def get_lesson(self):


        lessons = []
        tag_list = self.soup.find(class_='infolist_tab')
        tag_lesson = tag_list.find_all(class_='infolist_common')
        for i in xrange(0, len(tag_lesson)):
            lessons += self.__get_lesson(tag_lesson[i])
        lessons = sorted(lessons, key=lambda lesson:
                (lesson['week'], lesson['week_start'], lesson['day_start']))
        return lessons

    def __get_lesson(self, lesson_html):
        '''lesson'''
        lesson_list = []
        week_dict = {'周一' : 1, '周二' : 2, '周三' : 3, '周四' : 4,\
                '周五': 5, '周六' : 6, '周日' : 7}

        result = lesson_html.find_all(class_='infolist')
        name = self.__eliminate_gaps(result[0].string)
        data = lesson_html.find('table').find_all('td')

        for i in xrange(0, len(data), 4):
            lesson_dict = {}
            lesson_dict['lesson_name'] = name
            lesson_dict['week'] = week_dict[self.__eliminate_gaps(
                data[i+1].string).encode('utf-8')]
            lesson_dict['lesson_room'] = self.__eliminate_gaps(data[i+3].string)

            day = self.__screening_digital(data[i+2].string)
            lesson_dict['day_start'] = day[0]
            lesson_dict['day_end'] = day[1]
            weeks = self.__screening_digital(data[i].string)
            if '单周' in weeks[0]:
                lesson_dict['week_start'] = weeks[0][2:]
                lesson_dict['odd_week'] = '1'
            elif '双周' in weeks[0]:
                lesson_dict['week_start'] = weeks[0][2:]
                lesson_dict['odd_week'] = '2'
            else:
                lesson_dict['week_start'] = weeks[0]
                lesson_dict['odd_week'] = '0'

            lesson_dict['week_end'] = weeks[1]

             #处理错误的数据
            if '周' in weeks[1] and '周' in weeks[0] and weeks[1] == weeks[0]:
                lesson_dict['week_start'] = '1'
                lesson_dict['week_end'] = '18'
            lesson_list.append(lesson_dict)
        return lesson_list

def is_login(login_html, *args, **kwargs):
    '''Verify successful landing'''
    soup = BeautifulSoup(login_html.encode('utf8'),
                    'lxml', from_encoding='utf8')

    error = soup.find(id='error')
    if error == None:
        return 200
    error = error.string
    if '用户名' in error:
        return 601
    if '密码' in error:
        return 602
    if '验证码' in error:
        return 603

def get_student_info(info_html):

    '''get info'''

    info_dict = {}
    soup = BeautifulSoup(info_html.encode('utf8'),
                    'lxml', from_encoding='utf8')
    infos = soup.find(class_='form')
    info_tds = infos.find_all('td')

    info_dict['student_id'] = info_tds[0].string
    info_dict['full_name'] = info_tds[1].string
    info_dict['college'] = info_tds[3].string
    info_dict['specialty'] = info_tds[4].string
    info_dict['course'] = info_tds[6].string
    info_dict['school_year'] = info_tds[7].string
    info_dict['team'] = info_tds[8].string

    return info_dict

if __name__ == '__main__':
    get_info(11)
