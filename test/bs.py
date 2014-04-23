#coding=utf-8

from bs4 import BeautifulSoup
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')

f = open("htmlBASE",'r')
try:
    html = f.read()
finally:
    f.close();

soup = BeautifulSoup(html.encode('utf8'), 'lxml', from_encoding='utf8')


tag = soup.find(id='timetable')
tag = tag.find_all('tr', class_ = 'infolist_hr_common')

test = tag[0].find(id='1-1')

nn  = str(test).split('<br/>')
for var in nn:
    print var

n = nn[0].split(';')[2]

print n[:-3]


#pattern = re.compile(r'<td (.+?)>(.+?)</td>')

#print  pattern.match(str(test)).group()
    
#print test

#print str(test).split('<br/>')


#split('<br/>')
'''
for var in tag:
    for vvv in var.find_all(id=True):
        print vvv.find_all(text=True)
    
        print '..........................................' 
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
'''
#print tag
#print soup.prettify()
#tag =  soup.find_all("tr", class_=re.compile('list_*'))

#print type(tag)

#for td in tag:
#    print td.find_all(text = re.compile("\S"))
    #a = td.a
    #print a
    #print a.string
    #print type(a)


'''
print soup.a.attrs
#print soup.prettify()
#print soup.title.string

tag = soup.find_all('a')
for link in tag :
    print link.get('href')
'''
