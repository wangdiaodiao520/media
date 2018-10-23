#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import threading

import signal
import traceback

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from media_spider.util.deploy import DRIVER_HOME


class SeleniumDirverFactory(object):
    _instance_lock = threading.Lock()
    _driver_phantomjs = ''

    def __new__(cls, *args, **kwargs):
        if not hasattr(SeleniumDirverFactory, "_instance"):
            with SeleniumDirverFactory._instance_lock:
                if not hasattr(SeleniumDirverFactory, "_instance"):
                    SeleniumDirverFactory._instance = object.__new__(cls)
        return SeleniumDirverFactory._instance

    def __init__(self):
        pass

    def get_driver(self, name='phantomjs', loadImages=False):
        # todo:
        if name == 'phantomjs':
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
            )
            dcap["phantomjs.page.settings.loadImages"] = loadImages
            self._instance_lock.acquire()
            if self._driver_phantomjs == '':
                self._driver_phantomjs = webdriver.PhantomJS(desired_capabilities=dcap,
                                                             executable_path=DRIVER_HOME)
            self._instance_lock.release()
            return self._driver_phantomjs

    def close_driver(self, name='phantomjs'):
        self._instance_lock.acquire()
        if self._driver_phantomjs != '':
            self._driver_phantomjs.close()
        self._instance_lock.release()
        pass

    def quit_driver(self, name='phantomjs'):
        self._instance_lock.acquire()
        if self._driver_phantomjs != '':
            # driver.close() and driver.quit() killed the node process but not the phantomjs child process it spawned
            self._driver_phantomjs.service.process.send_signal(signal.SIGTERM)  # kill the specific phantomjs child proc
            # todo:ugly here
            try:
                self._driver_phantomjs.quit()  # quit the node proc
            except OSError:
                traceback.print_exc()
            except:
                traceback.print_exc()
            self._driver_phantomjs = ''
        self._instance_lock.release()
        pass
