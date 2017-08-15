#!/usr/bin/python3
# -*- coding: utf-8 -*-
import urllib.request
import json
import datetime
import time
import pandas as pd
import re
import math


def _get_data(url):
    time.sleep(0.1)
    headers = {'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
               }
    data = None
    req = urllib.request.Request(url, data, headers)
    ret = urllib.request.urlopen(req)
    return ret

def _get_jrjimg_tick(symbol, page, size):
    url = 'http://qmx.jrjimg.cn/mx.do?code=%s&page=%d&size=%d' % (symbol, page, size)
    VAR = _get_data(url).read().decode('gbk').split('\r\n')
    var = re.sub(r'([a-zA-Z]+\d*):', r'"\1":', ''.join(VAR))
    var = re.sub(r'^.*=', '', var)
    var = json.loads(var)
    return  var

def _get_today_tick_num(symbol):
    VAR = _get_jrjimg_tick(symbol, page=1, size=1)
    return VAR['Page']['A3']

def get_today_tick(symbol):
    per_size = 150 # max is 150
    tick_num = _get_today_tick_num(symbol)

    ticks = []
    for i in range(math.ceil(tick_num / per_size)):
        rsp = _get_jrjimg_tick(symbol, i+1, per_size)

        #ret = {}
        #ret['code'] = rsp['Summary']['A2']
        #ret['name'] = rsp['Summary']['A3']
        #ret['page'] = rsp['Page']['A3']
        #ret['detail'] = []
        for r in rsp['DetailData']:
            t = {}
            t['成交价']   = r['A1']
            t['成交手']   = r['A2']
            t['成交额']   = r['A3']
            t['成交时间'] = r['A5']
            t['成交方向'] = r['A6']
            #ret['detail'].append(t)
            ticks.append(t)
        #ticks.append(ret)

    return pd.DataFrame(ticks)


