import sys
import numpy as np
import pandas as pd
#from projectEval import rrEstimate

def optimal_return(dailyOhlcv, init_capital):

    capital = init_capital
    holds = 0.0
    capitalOrig=capital
    transFee = 100
    openPricev = dailyOhlcv["open"].values
    clearPrice = dailyOhlcv.iloc[-3]["close"]
    closePrice = dailyOhlcv["close"].values

    max_holds = [0]
    max_cash = [500000.0]
    opt_action = []

    for i in range(len(openPricev)):

        new_cash = max_holds[-1] * openPricev[i] - transFee
        if new_cash > max_cash[-1]:
            max_cash.append(new_cash)
        else:
            max_cash.append(max_cash[-1])

        new_holds = (max_cash[-1] - transFee) / openPricev[i]
        if new_holds > max_holds[-1]:
            max_holds.append(new_holds)
        else:
            max_holds.append(max_holds[-1])

        opt_action.append(max(max_cash[-1], max_holds[-1] * openPricev[i] - transFee))
    return opt_action
'''
def main():
    filename = sys.argv[1]
    dailyOhlcv = pd.read_csv(filename)
    opt_action = optimal_return(dailyOhlcv, 500000.0)
    for data in opt_action:
        print(data)

main()
'''