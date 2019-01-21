# coding=utf-8
import random

import time

urls = {
    "TPLINK": {  # TPLINK请求地址
        "req_url": "/",
        "req_type": "post",
        "Referer": "",
        "Content-Type": 1,
        "Host": "192.168.0.1",
        "re_try": 10,
        "re_time": 0.01,
        "s_time": 0.1,
        "is_logger": False,
        "is_json": True,
        "httpType": "http"
    },
    "TPds": {  # TPLINK路由器内部切换地址
        "req_url": "/stok={}/ds",
        "req_type": "post",
        "Referer": "",
        "Content-Type": 1,
        "Host": "192.168.0.1",
        "re_try": 10,
        "re_time": 0.01,
        "s_time": 0.1,
        "is_logger": False,
        "is_json": True,
        "httpType": "http"
    },
    "xiaomiHome": {  # 小米路由器登录
        "req_url": "/cgi-bin/luci/web",
        "req_type": "get",
        "Referer": "",
        "Content-Type": 1,
        "Host": "192.168.31.1",
        "re_try": 10,
        "re_time": 0.01,
        "s_time": 0.1,
        "is_logger": False,
        "is_json": False,
        "httpType": "http"
    },
    "xiaomi": {  # 小米路由器登录
        "req_url": "/cgi-bin/luci/api/xqsystem/login",
        "req_type": "post",
        "Referer": "",
        "Content-Type": 1,
        "Host": "192.168.31.1",
        "re_try": 10,
        "re_time": 0.01,
        "s_time": 0.1,
        "is_logger": False,
        "is_json": True,
        "httpType": "http"
    },
}