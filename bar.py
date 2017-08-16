#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tushare as ts

def get_1day_bar(symbol, start):
    return ts.get_h_data(symbol, start)

def get_all_1day_bar(start_symbol = ''):
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
            df = get_1day_bar(code, start)
            df.to_csv('1d/%s.csv' % code)
