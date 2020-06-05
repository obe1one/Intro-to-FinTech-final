import sys

valid_month = 99999999
trade_time_early = 84500
trade_time_night = 134500
max_number = 10 ** 20

def legal_trade(data):

    global valid_month
    if not (data[1][0] == 'T' and data[1][1] == 'X'): return False
    if '/' in data[2]: return False
    if int(data[2]) > valid_month: return False
    else: valid_month = int(data[2])
    if not trade_time_night >= int(data[3]) >= trade_time_early: return False
    return True

filename = sys.argv[1]
fp = open(filename, 'r', encoding = 'big5')

cont = fp.readline()
cont = fp.readline().split(',')
num = 0

tx_high = -1 * max_number
tx_low = max_number
tx_open = None
tx_close = None

while cont[0]:

    if legal_trade(cont):
        if int(cont[2]) < valid_month: valid_month = int(cont[2])
        tx_close = int(cont[4])
        if not tx_open: tx_open = tx_close
        if tx_close > tx_high: tx_high = tx_close
        if tx_close < tx_low: tx_low = tx_close
    cont = fp.readline().split(',')

print(tx_open, tx_high, tx_low, tx_close)
