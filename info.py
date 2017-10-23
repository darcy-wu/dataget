# -*- coding: utf-8 -*-
import pandas as pd
import tushare as ts
import tquant as tt
from dataget.helper import *

def update_db_all_info():
    df = tt.get_shse()
    df.to_csv('%s/shse.csv' % info_path, encoding='utf-8')
    df = tt.get_szse()
    df.to_csv('%s/szse.csv' % info_path, encoding='utf-8')
    df = tt.get_index()
    df.to_csv('%s/index.csv' % info_path, encoding='utf-8')

def get_symbol_list(index=False):
    if index:
        df = pd.read_csv('%s/index.csv' % info_path, dtype={'symbol' : 'O'})
        symbols =  df[df['is_active'] == 1]['symbol']
    else:
        df = pd.read_csv('%s/shse.csv' % info_path, dtype={'symbol' : 'O'})
        sh_symbols = df[df['is_active'] == 1]['symbol']
        df = pd.read_csv('%s/szse.csv' % info_path, dtype={'symbol' : 'O'})
        sz_symbols = df[df['is_active'] == 1]['symbol']
        symbols = sh_symbols.append(sz_symbols)
    return sorted(symbols)


