#!/usr/bin/env python
# encoding: utf-8

import time
import hashlib
import unittest
import requests

def get_date():
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

def get_md5(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()

def get_header(method,url,length,user,user_pwd):
    headers = {}
    date=get_date()
    sign = get_md5(method+'&'+url+'&'+date+'&'+length+'&'+get_md5(user_pwd))
    auth = "UpYun "+user+":" +sign
    headers['Host']='v0.api.upyun.com'
    headers['Date'] = date
    headers['Authorization'] = auth
    if length!='0':
        headers['Content-Length']= length
    return headers

def get(url,header=''):
    res=requests.get(url,headers=header)
    return res

def post(url,header='',data=''):
    res=requests.post(url,headers=header,data=data)
    return res

class cz_test(unittest.TestCase):
    def setUp(self):
        self.host='http://v0.api.upyun.com'
        self.USER='chenzhi'
        self.BUCKET='/hustcz/'
        self.USER_PWD='chenzhi123'
        self.file=''

    def tearDown(self):
        pass

    def test_get(self):
        self.header=get_header('GET',self.BUCKET+self.file,'0',self.USER,self.USER_PWD)
        self.res=get(self.host+self.BUCKET+self.file,self.header)
        self.assertEqual(self.res.status_code,200)

    def test_post(self):
        self.file='a.txt'
        self.data='123456789'
        self.header=get_header('POST',self.BUCKET+self.file,str(len(self.data)),self.USER,self.USER_PWD)
        self.res=post(self.host+self.BUCKET+self.file,self.header,self.data)
        self.assertEqual(self.res.status_code,200)

if __name__=='__main__':
    unittest.main()
