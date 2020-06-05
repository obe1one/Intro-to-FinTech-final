import sys
import numpy as np
import pandas as pd
import random

'''
MA ---> long/short term
highest/lowest ---> long term/short term/historical <-> highest/lowest
candle chart ---> H - L
RSI ---> long/short term
consecutive up/down
'''
#historical highest: 12682
#historical lowest: 2560
#ohlcv_daily.csv/ohlcv_minutely.csv
INF = 10000000000000001
historical_high = 12682
historical_low = 2560

def calc_ma(trading_data, ma_len, cur_price):
    data_value = trading_data['open'].values
    data_value = np.append(data_value, [cur_price])
    data_len = len(data_value)
    total = 0
    ma_set = []
    for i in range(data_len):
        total += data_value[i]
        if i + 1 < ma_len:
            ma_set.append(None)
        else:
            if i + 1 == ma_len:
                ma_set.append(total / ma_len)
            else:
                total -= data_value[i - ma_len]
                ma_set.append(total / ma_len)
    return ma_set

def calc_rsi(trading_data, rsi_period, cur_price):
    data_value = trading_data['open'].values
    data_value = np.append(data_value, [cur_price])
    data_len = len(data_value)
    smdu = 0
    smdd = 0
    rsi_set = [None]
    for i in range(1, data_len):
        new_addition = data_value[i] - data_value[i-1]
        if new_addition >= 0:
            smdu += new_addition
        else:
            smdd -= new_addition
        if i + 1 < rsi_period:
            rsi_set.append(None)
        else:
            if i + 1 == rsi_period:
                rsi_set.append(float(smdu / (smdu + smdd)))
            else:
                old_addition = data_value[i - rsi_period + 1] - data_value[i - rsi_period]
                if old_addition >= 0:
                    smdu -= old_addition
                else:
                    smdd += old_addition
                rsi_set.append(float(smdu / (smdd + smdu)))
    return rsi_set

def consecutive_trend(trading_data, cur_price):#guarentee data size >= 2, True (1) means upward, false (0) means downward
    data_value = trading_data['open'].values
    data_value = np.append(data_value, [cur_price])
    data_len = len(data_value)
    consecutive_days = 0
    data_trend = 1 if data_value[-1] >= data_value[-2] else 0
    for i in range(data_len-1, 0, -1):
        if data_trend == 1 and data_value[i] < data_value[i-1]:
            return data_trend, consecutive_days
        if data_trend == 0 and data_value[i] >= data_value[i-1]:
            return data_trend, consecutive_days
        consecutive_days += 1
    return data_trend, consecutive_days

def find_local_min_max(trading_data):
    data_value = trading_data['open'].values
    data_len = len(data_value)
    local_min = INF
    local_max = -1
    for i in range(data_len):
        if data_value[i] > local_max:
            local_max = data_value[i]
        if data_value[i] < local_min:
            local_min = data_value[i]
    return local_min, local_max

def kd_indicator(trading_data, cur_price):
    data_value = trading_data['open'].values
    data_value = np.append(data_value, [cur_price])
    data_len = len(data_value)
    k_set = [0.5] * 9
    d_set = [0.5] * 9
    for i in range(9, data_len):
        prev_max = data_value[i-8:i+1].max()
        prev_min = data_value[i-8:i+1].min()
        rsv = (data_value[i] - prev_min) / (prev_max - prev_min)
        k_set.append(rsv / 3 + 2 * k_set[-1] / 3)
        d_set.append(k_set[-1] / 3 + 2 * d_set[-1] / 3)
    return k_set, d_set





#ma: 0.01934439
#rsi: 0.01306203
#start in 1500: 0.15657583188952875 [15, 27, 4, 23, 277, 76, 1, 6, 210, 34, 1, 8]
#start in 2000: 0.016774193338182936 [19, 28, 6, 47, 133, 22, 1, 8, 134, 129, 1, 1]
#start in 2010: 0.013742772990723653 [6, 25, 14, 29, 210, 53, 0, 5, 150, 107, 0, 8] 0.0207
#start in 2010: 0.012959587071177706 [5, 31, 17, 28, 209, 36, 0, 8, 170, 10, 0, 6] 0.01689
#start in 2010: 0.014810956710343966 [11, 36, 6, 48, 283, 101, 0, 8, 190, 104, 1, 2] 0.01987
''' after change '''
#start in 2010: 0.15801345511333767 [17, 29, 9, 27, 223, 82, 0, 6, 130, 70, 0, 2] 0.01986236
#start in 2010: 0.162933330844775 [7, 23, 10, 30, 206, 102, 0, 7, 126, 290, 1, 2] 0.01986236
#const_range = [[1, 20], [21, 50], [1, 20], [21, 50], [0, 300], [0, 300], [0, 1], \
#[0, 8], [0, 300], [0, 300], [0, 1], [0, 8], [0, 100], [0, 100]]

 #0.19551682921924862 [4, 48, 18, 46, 203, 244, 0, 8, 213, 215, 1, 6, 71, 14]
def myStrategy(daily_data, minutely_data, cur_price, cont = [4, 48, 18, 46, 203, 244, 0, 8, 213, 215, 1, 6, 71, 14]):
    tar_data = daily_data.tail(100)
    short_ma = calc_ma(tar_data, cont[0], cur_price)
    long_ma = calc_ma(tar_data, cont[1], cur_price)
    short_rsi = calc_rsi(tar_data, cont[2], cur_price)
    long_rsi = calc_rsi(tar_data, cont[3], cur_price)
    trends = consecutive_trend(tar_data, cur_price)
    kd_idx = kd_indicator(tar_data, cur_price)
    
    if short_ma[-1] + cont[4] > long_ma[-1] and short_rsi[-1] + cont[5] / 300 > long_rsi[-1] \
       and trends[0] == cont[6] and trends[1] <= cont[7] and kd_idx[0][-1] < kd_idx[1][-1] < cont[12]:
       return 1
    if short_ma[-1] - cont[8] < long_ma[-1] and short_rsi[-1] + cont[9] / 300 < long_rsi[-1] \
       and trends[0] == cont[10] and trends[1] <= cont[11] and kd_idx[0][-1] > kd_idx[1][-1] > cont[13]:
       return -1
    return 0
'''
def myStrategy(daily_data, minutely_data, cur_price, cont = [3, 46, 10, 39, 29, 161, 0, 0, 55, 7, 0, 3]):
    a = kd_indicator(daily_data, cur_price)
    if a[0][-1] > a[1][-1] > 80: return -1
    if a[0][-1] < a[1][-1] < 20: return 1
    return 0
'''