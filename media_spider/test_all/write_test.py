#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import csv
import logging

import os

__author__ = 'zengyang@tv365.net(ZengYang)'

def common_write_test(row_data, real_path_file_name, head):
    logging.info('start write one data in %s' % real_path_file_name)
    # if not os.path.isfile(real_path_file_name):
    #     with open(real_path_file_name, 'a') as f:
    #         csv_write = csv.writer(f, dialect='excel')
    #         csv_write.writerow(head)
    with open(real_path_file_name, 'a') as f:
        csv_write = csv.writer(f, dialect='excel')
        csv_write.writerow(row_data)


def common_write_html_test(page_source):
    with open('/Users/tv365/money_more/crawl_money/test.html', 'w') as f:
        f.writelines(page_source)
