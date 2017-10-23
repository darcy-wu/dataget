# -*- coding: utf-8 -*-
import tushare as ts
import pandas as pd
from dataget.helper import *
import dataget.info as info
import os
import time
from datetime import datetime
from datetime import timedelta

#def write_db_all_stock_1day(start_symbol = '', end = ''):
#    symbols = ts.get_stock_basics()
#    ok = 0
#    if end == '':
#        end = datetime.today().strftime('%Y-%m-%d')
#    for code in symbols.index:
#        if start_symbol == '':
#            ok = 1
#        elif start_symbol == code:
#            ok = 1
#        if ok:
#            start = str(symbols.loc[code]['timeToMarket'])
#            if start == '0':
#                continue
#            if len(start) == 8:
#                start = start[0:4] + '-' + start[4:6] + '-' + start[6:]
#            print('do %s, start = %s' % (code, start))
#            df = ts.get_h_data(code, start=start, end=end, index=False)
#            df.to_csv('%s/stock.1d/%s.csv' % (bar_path, code), encoding='utf-8')
#
#def write_db_all_index_1day(index_path = '', start_symbol = '', end = ''):
#    df = pd.read_csv(index_path)
#    ok = 0
#    if end == '':
#        end = datetime.today().strftime('%Y-%m-%d')
#    for symbol in df.symbol:
#        code = symbol.split('.')[1]
#        if start_symbol == '':
#            ok = 1
#        elif start_symbol == code:
#            ok = 1
#        if ok:
#            start = '1999-01-01'
#            print('do %s, start = %s' % (code, start))
#            df = ts.get_h_data(code, start=start, end=end, index=True)
#            df.to_csv('%s/index.1d/%s.csv' % (bar_path, code), encoding='utf-8')

def write_db_all_1d(start_symbol='', end='', index=False):
    if index:
        path = index_1d_path
    else:
        path = stock_1d_path

    symbols = info.get_symbol_list(index)
    ok = 0
    start = '1999-01-01'
    if end == '':
        end = datetime.today().strftime('%Y-%m-%d')
    for code in symbols:
        if start_symbol == '':
            ok = 1
        elif start_symbol == code:
            ok = 1
        if ok:
            df = ts.get_h_data(code, start=start, end=end, index=index)
            df.to_csv('%s/%s.csv' % (path, code), encoding='utf-8')

def update_db_all_1d(start_symbol='', end='', index=False, sleep=2):
    if index:
        path = index_1d_path
    else:
        path = stock_1d_path
    symbols = info.get_symbol_list(index)
    ok = 0
    for code in symbols:
        if start_symbol == '':
            ok = 1
        elif start_symbol == code:
            ok = 1
        if ok:
            update_db_1d(code, end=end, index=index)
            time.sleep(sleep)


def update_db_1d_auto(start_symbol='', end='', index=False, sleep_step=5):
    if index:
        path = index_1d_path
    else:
        path = stock_1d_path
    ok = 0
    symbols = info.get_symbol_list(index)
    total = len(symbols)
    count = 0
    for code in symbols:
        count += 1
        if start_symbol == '':
            ok = 1
        elif start_symbol == code:
            ok = 1
        if ok:
            fail_num = 1
            while 1:
                delay = sleep_step*fail_num
                try:
                    if delay >= 60:
                        delay = 60
                    print('delay %d' % delay)
                    time.sleep(delay)
                    update_db_1d(code, end=end, index=index)
                except :
                    fail_num *= 2
                    if delay >= 60:
                        print('update %s failed' % code)
                        break
                else:
                    print('update %s finish, process %3.0f%%' % (code, count/total*100))
                    break

def update_db_1d(code, end = '', index=False):
    if index:
        path = index_1d_path
    else:
        path = stock_1d_path

    csv = '%s/%s.csv' % (path, code)
    if end == '':
        end = datetime.today().strftime('%Y-%m-%d')
    if os.path.exists(csv):
        with open(csv) as f:
            lines = f.readlines()
            for i in range(len(lines)-1, -1, -1):
                if lines[i] != '\n':
                    start = datetime.strptime(lines[i].split(',')[0], '%Y-%m-%d')
                    break
            start += timedelta(1)
            start = start.strftime('%Y-%m-%d')
            f.close()
        print('update %s from %s to %s' % (code, start, end))
        df = ts.get_h_data(code, start=start, end=end, index=index)
        if len(df):
            df.sort_index().to_csv(csv, header=False, mode='a', encoding='utf-8')
            print('finish stock: %s' % code)
        else:
            print('s: %s get 0 length' % code)
    else:
        print('do %s' % code)
        df = ts.get_h_data(code, start='2017-08-15', end=end, index=index)
        if len(df):
            df.sort_index().to_csv(csv, encoding='utf-8')
        else:
            print('s: %s get 0 length' % code)


def get_1d(symbol, index=False):
    if index:
        s = '%s/%s.csv' % (index_1d_path, symbol)
    else:
        s = '%s/%s.csv' % (stock_1d_path, symbol)

    if os.path.exists(s):
        return pd.read_csv(s, index_col='date', date_parser=lambda x : pd.Timestamp(x))
    else:
        print('ERROR: can not find %s\n use update_all_1d to update db' % s)

def update_db_day_all(date=''):
    df = ts.get_day_all(date)
    df.to_csv('%s/%s.csv' % (day_all_path, date), encoding='utf-8')

def get_day_all(date=''):
    if date == '':
        date = datetime.today().strftime('%Y-%m-%d')
    s = '%s/%s.csv' % (day_all_path, date)

    if os.path.exists(s):
        return pd.read_csv(s, index_col=0, dtype={'code': 'O'})
    else:
        return None



