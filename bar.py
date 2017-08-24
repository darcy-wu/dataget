# -*- coding: utf-8 -*-
import tushare as ts
import pandas as pd
from dataget.helper import *
import os
from datetime import datetime
from datetime import timedelta

def get_1day_bar(symbol, start, end = '', index=False):
    if end:
        return ts.get_h_data(symbol, start=start, end=end, index=index)
    else:
        return ts.get_h_data(symbol, start=start, index=index)

def write_all_stock_1day(start_symbol = '', end = ''):
    symbols = ts.get_stock_basics()
    ok = 0
    for code in symbols.index:
        if start_symbol == '':
            ok = 1
        elif start_symbol == code:
            ok = 1
        if ok:
            start = str(symbols.loc[code]['timeToMarket'])
            if start == '0':
                continue
            if len(start) == 8:
                start = start[0:4] + '-' + start[4:6] + '-' + start[6:]
            print('do %s, start = %s' % (code, start))
            df = get_1day_bar(code, start=start, end=end)
            df.to_csv('%s/stock.1d/%s.csv' % (bar_path, code), encoding='utf-8')

def write_all_index_1day(index_path = '', start_symbol = '', end = ''):
    df = pd.read_csv(index_path)
    ok = 0
    for symbol in df.symbol:
        code = symbol.split('.')[1]
        if start_symbol == '':
            ok = 1
        elif start_symbol == code:
            ok = 1
        if ok:
            start = '1999-01-01'
            print('do %s, start = %s' % (code, start))
            df = ts.get_h_data(code, start=start, end=end, index=True)
            df.to_csv('%s/index.1d/%s.csv' % (bar_path, code), encoding='utf-8')

def update_all_1d(start_symbol='', end='', index=False):
    if index:
        df = pd.read_csv('%s/index.csv' % info_path, dtype={'symbol' : 'O'})
        path = '%s/index.1d' % bar_path
        symbols = df.symbol
    else:
        path = '%s/stock.1d' % bar_path
        symbols = ts.get_stock_basics().index
    ok = 0
    for code in symbols.sort_values():
        if start_symbol == '':
            ok = 1
        elif start_symbol == code:
            ok = 1
        if ok:
            csv = '%s/%s.csv' % (path, code)
            if os.path.exists(csv):
                print('append %s' % code)
                with open(csv) as f:
                    lines = f.readlines()
                    for i in range(len(lines)-1, -1, -1):
                        if lines[i] != '\n':
                            start = datetime.strptime(lines[i].split(',')[0], '%Y-%m-%d')
                            break
                    start += timedelta(1)
                    start = start.strftime('%Y-%m-%d')
                    f.close()
                df = ts.get_h_data(code, start=start, end=end, index=index)
                if len(df):
                    df.sort_index().to_csv(csv, header=False, mode='a', encoding='utf-8')
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
        s = '%s/index.1d/%s.csv' % (bar_path, symbol)
    else:
        s = '%s/stock.1d/%s.csv' % (bar_path, symbol)

    if os.path.exists(s):
        return pd.read_csv(s, index_col='date', date_parser=lambda x : pd.Timestamp(x))
    else:
        print('ERROR: can not find %s\n use update_all_1d to update db' % s)

