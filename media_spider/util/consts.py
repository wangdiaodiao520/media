#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

TEST_API = 'http://pre-online.17getfun.com'
USE_API = 'http://www.17getfun.com'

all_pages = {
    'index_page': {
        'date': '',
        'data': {
            'platformId': -1,
            'accountId': -1,
            'logtime': -1,
            'fanCount': -1,
            'readCount': -1,
            'pvCount': -1,
            'contentCount': -1,
            'commentCount': -1,
            'collectCount': -1,
            'shareCount': -1,
            'likeCount': -1,
            'income': -1.0,
            'radia': -1.0,
            'dailies': [

            ]
        }
    },
    'user_page': {
        'date': '',
        'data': {
            'platformId': -1,
            'accountId': -1,
            'logtime': -1,
            'getCount': -1,
            'loseCount': -1,
            'gdCount': -1,
            'totalCount': -1
        }
    },
    'income_page': {
        'date': '',
        'data': {
            'platformId': -1,
            'accountId': -1,
            'logtime': -1,
            'income': -1.0,
            'allowance': -1.0,
            'total': -1.0
        }
    },
    'content_page': {
        'date': '',
        'data': {
            'platformId': -1,
            'accountId': -1,
            'title': -1,
            'readUser': -1,
            'readCount': -1,
            'pvCount': -1,
            'commentCount': -1,
            'collectCount': -1,
            'shareCount': -1,
            'likeCount': -1,
            'type': -1,
            'dailies': [
                {
                    'logtime': -1,
                    'readUser': -1,
                    'readCount': -1,
                    'pvCount': -1,
                    'commentCount': -1,
                    'collectCount': -1,
                    'shareCount': -1,
                    'likeCount': -1
                }
            ]
        }
    }
}

api_url_mapping = {
    'index_pages': TEST_API + '/api/weMedia/indexDataForCrawlNew',
    'user_pages': TEST_API + '/api/weMedia/readerDataForCrawlNew',
    'income_pages': TEST_API + '/api/weMedia/incomeDataForCrawlNew',
    'content_pages': TEST_API + '/api/weMedia/contentDataForCrawlNew',
}

source_settings = {
    'qi_e': {
        'login_url': 'https://om.qq.com/userAuth/index#1',
        'pages': {'index_page': '', 'user_page': '', 'income_page': '', 'content_page': '1'},
        'qi_e_account': [

        ]
    },
    'qq_kandian': {
        'login_url': 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=717054801&'
                     'daid=296&s_url=https://kandian.mp.qq.com&style=33&hide_title_bar=1&fontcolor=ffffff'
                     '&enable_qlogin=0&self_regurl=http://zc.qq.com/chs/index.html#1',
        'pages': {'index_page': '', 'user_page': '', 'income_page': '', 'content_page': '1'},
        'qq_kandian_account': [
            {'user_name': '210963672', 'pwd': 'getfun666', 'accountId': 14, 'platformId': 5, 'name_use': '盖饭爱生活'},
            {'user_name': '212640179', 'pwd': 'getfun666', 'accountId': 12, 'platformId': 5, 'name_use': '盖饭谈历史'},
        ]
    },
    'bai_jia': {
        'login_url': 'http://baijiahao.baidu.com/builder/app/login',
        'pages': {'index_page': '', 'user_page': '', 'income_page': '', 'content_page': '1'},
        'bai_jia_account': [

        ]
    },
    'dayu': {
        'login_url': 'https://mp.dayu.com/',
        'pages': {'index_page': '', 'user_page': '', 'income_page': '', 'content_page': '1'},
        'dayu_account': [

        ]
    },
    'yidian': {
        'login_url': 'https://mp.yidianzixun.com',
        'pages': {'index_page': '', 'user_page': '', 'income_page': '', 'content_page': '1'},
        'yidian_account': [

        ]
    },
    'totiao': {
        'login_url': 'https://sso.toutiao.com/',
        'pages': {'index_page': '', 'user_page': '', 'income_page': '', 'content_page': '1'},
        'dayu_account': [
            {'user_name': '349134876@qq.com', 'pwd': 'Mgt19920406', 'accountId': -11, 'platformId': 9,
             'name_use': '18062615140'},
            {'user_name': 'getfun17@qq.com', 'pwd': 'GETfun2015***', 'accountId': -22, 'platformId': 9,
             'name_use': '18064077270'},
        ]
    }
}

use_account = [
    {'user_name': '349134876@qq.com', 'pwd': 'mgt19920406', 'accountId': 13, 'platformId': 6, 'name_use': '盖饭奇趣'},
    {'user_name': '3026412373@qq.com', 'pwd': 'getfun666', 'accountId': 14, 'platformId': 6, 'name_use': '盖饭爱生活'},

    {'user_name': '210963672', 'pwd': 'getfun666', 'accountId': 14, 'platformId': 5, 'name_use': '盖饭爱生活'},
    {'user_name': '212640179', 'pwd': 'getfun666', 'accountId': 12, 'platformId': 5, 'name_use': '盖饭谈历史'},

    {'user_name': 'fzq@17getfun.com', 'pwd': 'gaifan2018', 'accountId': -3, 'platformId': 6, 'name_test': '盖饭好车'},

    {'user_name': '2314498174', 'pwd': 'getfun666', 'accountId': -3, 'platformId': 5, 'name_test': '盖饭好车'},
    {'user_name': '3152844751', 'pwd': 'getfun666', 'accountId': -2, 'platformId': 5, 'name_test': '盖饭好车'},

    {'user_name': '18811496361', 'pwd': 'gf12345678', 'accountId': -1, 'platformId': 7, 'name_test': '盖饭好物'},
    {'user_name': 'getfunauto@163.com', 'pwd': 'gaifan2017', 'accountId': -2, 'platformId': 7, 'name_test': '盖饭汽车'},
    {'user_name': '13349936392', 'pwd': 'getfun666', 'accountId': 3, 'platformId': 7, 'name_use': '盖饭娱乐'},
    {'user_name': '18186469376', 'pwd': '1haozhuanan', 'accountId': 16, 'platformId': 7, 'name_use': '加拿大必读'},

    {'user_name': 'getfunlife@163.com', 'pwd': 'gf12345678', 'accountId': -1, 'platformId': 2, 'name_test': '盖饭好物'},
    {'user_name': '15927620827', 'pwd': 'getfun666', 'accountId': 14, 'platformId': 2, 'name_use': '盖饭爱生活'},
    {'user_name': 'dingliping@17getfun.com', 'pwd': 'getfun666', 'accountId': 12, 'platformId': 2, 'name_use': '盖饭谈历史'},
    {'user_name': 'vsmodellife@163.com', 'pwd': 'VSmodel2015***', 'accountId': 4, 'platformId': 2, 'name_use': '超美时尚社'},

    {'user_name': 'getfunlife@163.com', 'pwd': 'gf12345678', 'accountId': -1, 'platformId': 8, 'name_test': '盖饭好物'},
    {'user_name': 'yuluozhong@17getfun.com', 'pwd': 'getfun666', 'accountId': 14, 'platformId': 8, 'name_use': '盖饭爱生活'},
    {'user_name': 'haowenjie@17getfun.com', 'pwd': 'getfun666', 'accountId': 12, 'platformId': 8, 'name_use': '盖饭谈历史'},
    {'user_name': 'xunuo@17getfun.com', 'pwd': 'getfun666', 'accountId': 11, 'platformId': 8, 'name_use': '娱乐君的日常'},

    {'user_name': '18811496361', 'pwd': 'gf12345678', 'accountId': -1, 'platformId': 9, 'name_test': '盖饭好物'},
    {'user_name': 'getfunauto@163.com', 'pwd': 'gaifan2017', 'accountId': -2, 'platformId': 9, 'name_test': '盖饭汽车'},
    {'user_name': 'fzq@17getfun.com', 'pwd': 'gaifan2018', 'accountId': -3, 'platformId': 9, 'name_test': '盖饭好车'},

]
