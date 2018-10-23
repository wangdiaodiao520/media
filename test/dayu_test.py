#!/usr/bin/python
# coding=utf8
from data import login_data
import os
import time
import random
import threading
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def get_dayu_response(login_name,login_pwd):
    url = 'https://mp.dayu.com/'
    driver = webdriver.Firefox()#(executable_path=DRIVER_FIREFOX_HOME)
    #iedriver ='C:\IEDriverServer.exe' #iedriver路径
    #os.environ["webdriver.ie.driver"] = iedriver #设置环境变量
    #driver = webdriver.Ie()
    driver.get(url)

    elementi = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(elementi)
    elem_phone = driver.find_element_by_id('login_name')
    elem_phone.send_keys(login_name)
    time.sleep(1)
    elem_pwd = driver.find_element_by_id('password')
    elem_pwd.send_keys(login_pwd)
    
    time.sleep(3)
    move_slider(driver)

    while True:
        try:
            driver.find_element_by_id("submit_btn").click()
            break
        except:
            continue

    while True:
        try:
            driver.switch_to.default_content()
            cookies = driver.get_cookies()
            break
        except:
            continue


    print cookies
    driver.quit()
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
                    continue
            # 目前只碰到3种情况：成功（请在在下方输入验证码,请点击图）；无响应（请按住滑块拖动)；失败（哎呀，失败了，请刷新）
            if text.text.startswith(u'验证通过'):
                break
            elif text.text.startswith(u'哎呀，出错了，点击刷新再来一次'):
                driver.find_element_by_xpath("//span[@class='nc-lang-cnt']/a").click()
                pass
        except Exception as e:
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

if __name__ == "__main__":

    user = login_data['dayu']['account']
    for i in user:
        login_name = i['user_name']
        login_pwd = i['pwd']
        get_dayu_response(login_name,login_pwd)
        
    
