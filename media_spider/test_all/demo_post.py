#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import base64
import json
import random
import urllib
import urllib2

import time
from telnetlib import EC

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from media_spider.tools.cookie_manager import get_cookie
from media_spider.tools.phantom_js_driver import SeleniumDirverFactory
from media_spider.util.basic_type_converter import from_json_to_string

__author__ = 'zengyang@tv365.net(ZengYang)'


def demo_post1():
    head_dict = {
        'ContentType': 'application/json',
        'user-agent':'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }



    url = 'https://sso.toutiao.com/account_login/'
    data = {
        'account': 'fzq@17getfun.com',
        'password': 'gaifan2018',
        'captcha': '',
        'is_30_days_no_login': 'false'
    }
    data = urllib.urlencode(data)
    req = urllib2.Request(url=url, data=data, headers=head_dict)
    res = urllib2.urlopen(req)
    res = res.read()
    time.sleep(1)
    pass


def demo_post2():
    head_dict = {
        'ContentType': 'application/json',
        'User-Agent':'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Cookie':'BAIDUID=706E057991F17D519A2F66F0CE5623ED:FG=1; BIDUPSID=706E057991F17D519A2F66F0CE5623ED; PSTM=1532352832; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; people=0; H_PS_PSSID=1467_21115_18559_26350_26921_22074; PSINO=1; locale=zh; FP_UID=dbf5ba22343878e982758e57b684c9e9; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDUSS=l6anhJeGpSTml-bHNCTDQ3OGZEWXE1b3JwYXhXcUtlTGh1ZXJsUGpCRFIxWUJiQVFBQUFBJCQAAAAAAAAAAAEAAABvQbjNuMe3ubrDzu8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANFIWVvRSFlbVm'
    }
    url = 'https://baijiahao.baidu.com/builder/author/message/getUnreadNum?'
    req = urllib2.Request(url=url,  headers=head_dict)
    res = urllib2.urlopen(req)
    res = res.read()
    pass


def demo_login():

    browser = webdriver.Firefox(executable_path='/Users/tv365/geckodriver')
    wait = WebDriverWait(browser,5)

    url = "https://baijiahao.baidu.com/builder/app/login"
    browser.get(url)

    # put_login = browser.find_element_by_id('TANGRAM__PSP_4__footerULoginBtn')
    put_login = wait.until(EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_4__footerULoginBtn')))
    put_login.click()

    # name = browser.find_element_by_id('TANGRAM__PSP_4__userName')
    name = wait.until(EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_4__userName')))
    name.send_keys('深情多杀薄情人')

    # password = browser.find_element_by_id('TANGRAM__PSP_4__password')
    password = wait.until(EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_4__password')))
    password.send_keys('wangzhichen')

    # enter = browser.find_element_by_id('TANGRAM__PSP_4__submit')
    enter = wait.until(EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_4__submit')))
    enter.click()

    pass


def demo_login1():

    browser = webdriver.Firefox(executable_path='/Users/tv365/geckodriver')
    browser.set_page_load_timeout(2)

    try:
        url = "https://baijiahao.baidu.com/builder/app/login"
        browser.get(url)
    except TimeoutException:
        put_login = browser.find_element_by_id('TANGRAM__PSP_4__footerULoginBtn')
        time.sleep(random.randint(1,5))
        # put_login = wait.until(EC.presence_of_element_located((By.ID,'TANGRAM__PSP_4__footerULoginBtn')))
        put_login.click()

        name = browser.find_element_by_id('TANGRAM__PSP_4__userName')
        time.sleep(random.randint(1, 5))
        # name = wait.until(EC.presence_of_element_located((By.ID,'TANGRAM__PSP_4__userName')))
        name.send_keys('18811496361')

        password = browser.find_element_by_id('TANGRAM__PSP_4__password')
        time.sleep(random.randint(1, 5))
        # password = wait.until(EC.presence_of_element_located((By.ID,'TANGRAM__PSP_4__password')))
        password.send_keys('gf12345678')

        enter = browser.find_element_by_id('TANGRAM__PSP_4__submit')
        time.sleep(random.randint(1, 5))
        # enter = wait.until(EC.presence_of_element_located((By.ID,'TANGRAM__PSP_4__submit')))
        enter.click()
    pass


def demo_check():
    url = 'https://baijiahao.baidu.com/builder/author/statistic/getFansBasicInfo?start=%s&end=%s&fans_type=new%%2Csum&sort=asc&is_page=0&show_type=chart' % (
        222, 222)
    pass


demo_post1()
# demo_post2()
# demo_login()
# demo_login1()
# demo_check()