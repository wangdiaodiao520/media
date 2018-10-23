#!/usr/bin/python
# coding=utf8
from data import login_data

import time
import random
import threading
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait



def get_bai_jia_response(login_name,login_pwd):
    url = 'http://baijiahao.baidu.com/builder/app/login'
    driver = webdriver.Firefox()#(executable_path=)
    driver.set_page_load_timeout(5)
    try:
        driver.get(url)
    except:
        time.sleep(3)

        put_login = driver.find_element_by_id('TANGRAM__PSP_4__footerULoginBtn')
        put_login.click()
        time.sleep(random.randint(1, 3))

        name = driver.find_element_by_id('TANGRAM__PSP_4__userName')
        name.send_keys(login_name)
        time.sleep(random.randint(1, 5))

        password = driver.find_element_by_id('TANGRAM__PSP_4__password')
        password.send_keys(login_pwd)
        time.sleep(random.randint(1, 5))
        enter = driver.find_element_by_id('TANGRAM__PSP_4__submit')
        enter.click()
        time.sleep(5)
        # element = WebDriverWait(driver, 30, 0.5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "client_pages_home")))

        cookies = driver.get_cookies()
        print "拿到cookies",cookies
        driver.quit()


if __name__ == "__main__":

    user = login_data['baijia']['account']
    while True:
        for i in user:
            login_name = i['user_name']
            login_pwd = i['pwd']
            get_bai_jia_response(login_name,login_pwd)
        
        
    
