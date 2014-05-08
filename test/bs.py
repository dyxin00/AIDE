#coding=utf-8

from bs4 import BeautifulSoup
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
f = open("html", 'r')
try:
    html = f.read()
finally:
    f.close();
'''
class Lesson():

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

    def is_login(self):
        if self.__eliminate_gaps(self.soup.title.string) == '用户登录':

            return False
        return True

    def get_lesson(self):

        if not self.is_login():
            return None

        lesson = []
        tag_list = self.soup.find(class_='infolist_tab')
        tag_lesson = tag_list.find_all(class_='infolist_common')
        for i in xrange(0, len(tag_lesson)):
            lesson += self.__get_lesson(tag_lesson[i])

        return lesson

    def __get_lesson(self, lesson_html):
        '''lesson'''
        lesson_list = []

        result = lesson_html.find_all(class_='infolist')
        name = self.__eliminate_gaps(result[0].string)
        data = lesson_html.find('table').find_all('td')

        for i in xrange(0, len(data), 4):
            lesson_dict = {}
            lesson_dict['lesson_name'] = name
            lesson_dict['week'] = self.__eliminate_gaps(data[i+1].string)
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

def aaaa(html):

    lesson = Lesson(html)
    dd = lesson.get_lesson()


    for d in dd:
         for k, v in d.items():
             print k + ' ' + v
         print 
if __name__ == '__main__':
    pass
