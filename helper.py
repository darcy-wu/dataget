# -*- coding: utf-8 -*-
import datetime

data_path = '/home/darcy/data'

# bar path {
bar_path = '%s/bar' % data_path
index_1d_path = '%s/index.1d' % bar_path
stock_1d_path = '%s/stock.1d' % bar_path
day_all_path  = '%s/day_all' % bar_path
# }

# tick path {
tick_path = '%s/tick' % data_path
# }

info_path = '%s/info' % data_path


default_start = (datetime.datetime.today() - datetime.timedelta(weeks=20)).strftime('%Y-%m-%d')
default_end = datetime.datetime.today().strftime('%Y-%m-%d')

