#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

__author__ = 'zengyang@tv365.net(ZengYang)'

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.by import By

def get_track():

    track = []
    current = 0
    mid = 500 * 4 / 5
    t = 0.2
    v = 0
    while current < 500:
        if current < mid:
            a = 3
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


def get_track1(distance=300):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 0.2
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
    ActionChains(driver).click_and_hold(slider).perform()
    for x in track:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    time.sleep(0.1)
    ActionChains(driver).release().perform()


driver = webdriver.Firefox(executable_path='/Users/tv365/geckodriver')
driver.get('https://mp.dayu.com/')

iframe = driver.find_element_by_tag_name('iframe')
driver.switch_to_frame(iframe)
user = driver.find_element_by_id('login_name')
user.send_keys('getfunlife@163.com')
passwd = driver.find_element_by_id('password')
passwd.send_keys('gf12345678')

action = ActionChains(driver)
slide = driver.find_element_by_xpath(r'//*[@id="nc_1_n1z"]')
action.click_and_hold(slide).perform()
# action.move_by_offset(2,0)
tmp = get_track1()
move_to_gap(driver, slide, tmp)


