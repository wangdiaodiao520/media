#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import logging
import random
import time
import traceback

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from media_spider.test_all.write_test import common_write_html_test
from media_spider.tools.phantom_js_driver import SeleniumDirverFactory
from media_spider.util.consts import source_settings
from media_spider.util.deploy import DRIVER_FIREFOX_HOME

__author__ = 'zengyang@tv365.net(ZengYang)'


def get_qi_e_response(spider, request):
    response = None
    if request.url == source_settings['qi_e']['login_url']:
        driver_factory = SeleniumDirverFactory()
        driver = driver_factory.get_driver()
        driver.get(request.url)
        elem_email = driver.find_element_by_name('email')
        elem_email.send_keys(request.meta['account']['user_name'])
        elem_pwd = driver.find_element_by_name('password')
        elem_pwd.send_keys(request.meta['account']['pwd'])
        driver.find_element_by_xpath(
            "//div[@class='login-submit']/button[@class='btnLogin btn btn-primary']").click()
        time.sleep(5)
        body = driver.page_source
        cookies = driver.get_cookies()
        account_cookie = {}
        for cookie in cookies:
            if 'name' in cookie.keys() and 'value' in cookie.keys():
                account_cookie[cookie['name']] = cookie['value']
        request.meta['cookie'] = account_cookie
        response = HtmlResponse(url=driver.current_url, body=body.encode('utf-8'))
        driver_factory.quit_driver()
    return response


def get_qq_kandian_response(spider, request):
    response = None
    if request.url == source_settings['qq_kandian']['login_url']:

        while True:
            try:
                driver_factory = SeleniumDirverFactory()
                driver = driver_factory.get_driver()
                driver.get(request.url)
                time.sleep(5)
                driver.find_element_by_xpath("//a[@id='switcher_plogin']").click()
                break
            except:
                traceback.print_exc()
                logging.warn('perhaps more pids for phantomjs or page to be fresh')
                driver_factory.quit_driver()

        elem_email = driver.find_element_by_name('u')
        elem_email.send_keys(request.meta['account']['user_name'])
        elem_pwd = driver.find_element_by_name('p')
        elem_pwd.send_keys(request.meta['account']['pwd'])

        driver.find_element_by_class_name('btn').click()
        time.sleep(5)

        body = driver.page_source
        cookies = driver.get_cookies()
        account_cookie = {}
        for cookie in cookies:
            if 'name' in cookie.keys() and 'value' in cookie.keys():
                account_cookie[cookie['name']] = cookie['value']
        request.meta['cookie'] = account_cookie
        response = HtmlResponse(url=driver.current_url, body=body.encode('utf-8'))
        driver_factory.quit_driver()
    elif request.url[-len('#2'):] == '#2':
        driver_factory = SeleniumDirverFactory()
        driver = driver_factory.get_driver()
        driver.get(request.url)
        body = driver.page_source
        response = HtmlResponse(url=driver.current_url, body=body.encode('utf-8'))
        driver_factory.quit_driver()
    return response


def get_bai_jia_response(spider, request):
    response = None
    if request.url == source_settings['bai_jia']['login_url']:
        driver = webdriver.Firefox(executable_path=DRIVER_FIREFOX_HOME)
        driver.set_page_load_timeout(5)
        try:
            driver.get(request.url)
        except:
            logging.info('time out===>login too fast')
            traceback.print_exc()
            time.sleep(5)
        finally:
            put_login = driver.find_element_by_id('TANGRAM__PSP_4__footerULoginBtn')
            put_login.click()
            time.sleep(random.randint(1, 5))

            name = driver.find_element_by_id('TANGRAM__PSP_4__userName')
            name.send_keys(request.meta['account']['user_name'])
            time.sleep(random.randint(1, 5))

            password = driver.find_element_by_id('TANGRAM__PSP_4__password')
            password.send_keys(request.meta['account']['pwd'])
            time.sleep(random.randint(1, 5))
            enter = driver.find_element_by_id('TANGRAM__PSP_4__submit')
            enter.click()
            time.sleep(5)
            # element = WebDriverWait(driver, 30, 0.5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "client_pages_home")))

        body = driver.page_source
        cookies = driver.get_cookies()
        account_cookie = {}
        for cookie in cookies:
            if 'name' in cookie.keys() and 'value' in cookie.keys():
                account_cookie[cookie['name']] = cookie['value']
        request.meta['cookie'] = account_cookie
        response = HtmlResponse(url=driver.current_url, body=body.encode('utf-8'))
        driver.quit()
    return response


def get_toutiao_response(spider, request):
    # todo:
    response = None
    return response


def get_dayu_response(spider, request):
    response = None
    if request.url == source_settings['dayu']['login_url']:
        driver = webdriver.Firefox(executable_path=DRIVER_FIREFOX_HOME)
        driver.get(request.url)

        elementi = driver.find_element_by_tag_name('iframe')
        driver.switch_to.frame(elementi)
        elem_phone = driver.find_element_by_id('login_name')
        elem_phone.send_keys(request.meta['account']['user_name'])
        elem_pwd = driver.find_element_by_id('password')
        elem_pwd.send_keys(request.meta['account']['pwd'])

        move_slider(driver)

        while True:
            try:
                driver.find_element_by_id("submit_btn").click()
                break
            except:
                logging.info('button not find')
                traceback.print_exc()
                continue

        while True:
            try:
                driver.switch_to.default_content()
                cookies = driver.get_cookies()
                break
            except:
                logging.info('get_cookies not find')
                traceback.print_exc()
                continue

        account_cookie = {}
        for cookie in cookies:
            if 'name' in cookie.keys() and 'value' in cookie.keys():
                account_cookie[cookie['name']] = cookie['value']
        request.meta['cookie'] = account_cookie
        response = HtmlResponse(url=driver.current_url)
        driver.quit()
    return response


def get_yidian_response(spider, request):
    response = None
    if request.url == source_settings['yidian']['login_url']:
        driver_factory = SeleniumDirverFactory()
        driver = driver_factory.get_driver(loadImages=True)
        driver.set_window_size(1440, 800)
        driver.get(request.url)
        time.sleep(2)
        #common_write_html_test(driver.page_source.encode('utf-8'))
        driver.find_element_by_xpath("//div[@class='inner-content']//a[1]").click()
        time.sleep(5)

        elem_phone = driver.find_element_by_xpath("//div[@class='inner-content']//div[@class='input-list']/input[1]")
        elem_phone.send_keys(request.meta['account']['user_name'])
        elem_pwd = driver.find_element_by_xpath("//div[@class='inner-content']//div[@class='input-list']/input[2]")
        elem_pwd.send_keys(request.meta['account']['pwd'])

        driver.find_element_by_xpath(
            "//div[@class='inner-content']//button[@class='mp-btn mp-btn-large mp-btn-primary s-button']").click()
        time.sleep(5)

        body = driver.page_source
        cookies = driver.get_cookies()
        account_cookie = {}
        for cookie in cookies:
            if 'name' in cookie.keys() and 'value' in cookie.keys():
                account_cookie[cookie['name']] = cookie['value']
        request.meta['cookie'] = account_cookie
        response = HtmlResponse(url=driver.current_url, body=body.encode('utf-8'))
        driver_factory.quit_driver()
    return response


def move_slider(driver):
    while True:
        try:
            # 定位滑块元素
            slider = driver.find_element_by_xpath("//span[@id='nc_1_n1z']")
            track = get_track()
            move_to_gap(driver, slider, track)
            # 查看是否认证成功，获取text值
            while True:
                try:
                    text = driver.find_element_by_xpath("//span[@class='nc-lang-cnt']")
                    break
                except:
                    logging.info('text not find')
                    traceback.print_exc()
                    continue
            # 目前只碰到3种情况：成功（请在在下方输入验证码,请点击图）；无响应（请按住滑块拖动)；失败（哎呀，失败了，请刷新）
            if text.text.startswith(u'验证通过'):
                logging.info('slider over success')
                break
            elif text.text.startswith(u'哎呀，出错了，点击刷新再来一次'):
                driver.find_element_by_xpath("//span[@class='nc-lang-cnt']/a").click()
                pass
        except Exception as e:
            traceback.print_exc()
            logging.error('slider over failed error')
            time.sleep(5)


def get_track(distance=200):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 0.2
    t = 0.9
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


def move_to_gap(driver, slider, track):
    try:
        ActionChains(driver).click_and_hold(slider).perform()
        for x in track:
            ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.1)
        ActionChains(driver).release().perform()
    except:
        traceback.print_exc()
