#!/usr/bin/python3
# -*- coding: utf-8 -*-
import urllib.request
import json
import time
from datetime import datetime
import pandas as pd
import re
import os
import tquant as tt
import tushare as ts
import dataget.helper as helper
import dataget.info as info
import time

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
    page = 0
    per_size = 150
    ticks = []
    total = 0
    for _ in range(1000): # 最多取一千次
        rsp = _get_jrjimg_tick(symbol, page, per_size)
        if total == 0:
            total = rsp['Page']['A3']
            print('total = %d' % total)
        print('len ticks = %d' % len(ticks))
        for r in rsp['DetailData']:
            t = {}
            t['price'] = r['A1']
            t['volume'] = r['A2']
            t['amount'] = r['A3']
            t['date'] = datetime.today().strftime('%Y%m%d') + ' ' + r['A5']
            if r['A6'] == '1':
                t['type'] = '买盘'
            else:
                t['type'] = '卖盘'
            #ret['detail'].append(t)
            ticks.append(t)
        if len(ticks) < total:
            page += 1
        else:
            break
    df = pd.DataFrame(ticks)
    df.index = pd.DatetimeIndex(df.date)
    del df.date
    return df

def get_hist_tick(symbol, date):
    """
        获取历史tick数据，2009年以后的数据。
        ex：dg.tick.get_hist_tick('000002', '2015-09-09')
    Return
    --------
    DataFrame
        date   : 日期时间
        amount : 成交额
        price  : 成交价
        type   : 买卖盘
        volume : 成交手
    """
    df =  tt.get_tick_history(symbol, date)
    if df:
        df.rename(columns={'close': 'price', 'vol': 'volume'}, inplace=True)
        del df['code']
    return df

def get_today_tick2(symbol):
    df = ts.get_today_ticks('000002')
    del df.pchange
    del df.change
    df.index = pd.DatetimeIndex(df.time)
    del df.time
    return df

def update_db_tick(symbol, date):
    print('update tick %s@%s' % (symbol, date), end='')
    df =  tt.get_tick_history(symbol, date)
    if type(df) == pd.core.frame.DataFrame and len(df):
        df.rename(columns={'close': 'price', 'vol': 'volume'}, inplace=True)
        os.makedirs('%s/%s' % (helper.tick_path, date), exist_ok=True)
        s = _tick_file(symbol, date)
        df.sort_index().to_csv(s, encoding='utf-8')
        print(' ok', end='')
        print(' %s' % datetime.now().time())
        return True
    else:
        print(' failed', end='')
        print(' %s' % datetime.now().time())
        return False

def get(symbol, date=''):
    if date == '':
        date = datetime.today().strftime('%Y-%m-%d')
    s = _tick_file(symbol, date)
    if not os.path.exists(s):
        if not update_db_tick(symbol, date):
            return None
        return pd.read_csv(s, index_col='date', date_parser=lambda x : pd.Timestamp(x))

def update_db_tick_auto(start_symbol='', date='', sleep=5):
    fail_list = []
    if date == '':
        date = datetime.today().strftime('%Y-%m-%d')
    ok = 0
    symbols = info.get_symbol_list()
    total = len(symbols)
    count = 0
    for code in symbols:
        count += 1
        if ok == 0:
            if start_symbol == '':
                ok = 1
            elif start_symbol == code:
                ok = 1
        else:
            s = _tick_file(code, date)
            if not os.path.exists(s):
                if not update_db_tick(code, date) :
                    fail_list.append(code)
                time.sleep(sleep)
        print('process %30f%%' % (count/total*100))
    return fail_list

def _tick_file(symbol, date):
    return '%s/%s/%s.csv' % (helper.tick_path, date, symbol)


