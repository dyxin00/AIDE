#!/usr/bin/env python
# coding=utf-8

import sys
reload(sys)  
sys.setdefaultencoding('utf8')   

import requests
from bs import BeautifulSoup

class Data_capture():

   
    __req_session = requests.Session()

    def __init__(self, username, passcode, **kwargs):

        self.__username = username
        self.__passcode = passcode
        
