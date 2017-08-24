# -*- coding: utf-8 -*-
#import pandas as pd
#import tushare as ts
import tquant as tt

def get_all_info():
    df = tt.get_shse()
    df.to_csv('shse.csv', encoding='utf-8')
    df = tt.get_szse()
    df.to_csv('szse.csv', encoding='utf-8')
    df = tt.get_szse()
    df.to_csv('szse.csv', encoding='utf-8')
    df = tt.get_index()
    df.to_csv('index.csv', encoding='utf-8')

