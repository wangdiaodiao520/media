#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import time

__author__ = 'zengyang@tv365.net(ZengYang)'

end_time = str(time.time() - 24 * 60 * 60 * 1)[:10]
end_time_13 =  str(int(round(time.time()*1000)) - 24 * 60 * 60 * 1000 * 1)

timeStamp = 1381419600
otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(timeStamp))
