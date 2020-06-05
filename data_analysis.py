import sys
import numpy as np
import pandas as pd
import random
from optimal_action import optimal_return
from myStrategy import myStrategy
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def rdi(a):#randint
    return random.randint(a[0], a[1])

def pft_Esitmate(daily_data, start_day, const):

    opt_profit = optimal_return(daily_data, 500000.0) #find the maximum profit of each day
    capital = opt_profit[start_day - 1] #initialize the capital
    org_capital = capital
    holds = 0
    transFee = 100 #pay transFee in each transcection
    data_value = daily_data['open'].values
    opt_rate = 0 #save the 
    for i in range(start_day, len(data_value)):
        cur_price = data_value[i]
        action = myStrategy(daily_data[0:i], None, cur_price, const) #strategy decision model
        if action == 1: #buy all
            if capital >= transFee:
                holds += (capital - transFee) / cur_price
                capital = 0
        elif action == -1: #sell all
            new_holds = holds * cur_price - transFee
            if new_holds >= 0:
                capital += new_holds
                holds = 0
        else: #do nothing
            pass
    now_capital = capital if capital else holds * cur_price - transFee #
    opt_rate += (now_capital / opt_profit[i]) #find the ratio to optimal profit
    try:
        return opt_rate / (len(data_value) - start_day) #average ratio to optima profit
    except:
        return None

def sort_gene(a):
    return a[0]

def plot_data(plt, data):
  x = [p[0] for p in data]
  y = [p[1] for p in data]
  plt.plot(x, y, '-o')

def GA_Training(daily_data, generation_scale, test_round, start_day, const_range):
    max_pft = 0
    max_const = None
    const_num = len(const_range)
    survive_set = []#survived gene
    avg_pft_set = []#average profit of each round
    max_pft_set = []#max profit of each round
    #create the first generation
    for i in range(generation_scale):
        new_gene = []
        for j in range(const_num):
            new_gene.append(rdi(const_range[j]))
        new_pft = pft_Esitmate(daily_data, start_day, new_gene)
        survive_set.append([new_pft, new_gene])
    #start to traing, test_round rounds
    for rd in range(test_round):
        print('Round ', rd)
        for creature in survive_set:
            print('survived creature:', creature)
        new_set = survive_set.copy() #elite classic, preserve all creatures in parent geneartion
        #crossover
        for i in range(generation_scale):
            for j in range(i + 1, generation_scale):
                ng = []
                for k in range(const_num): #inherit both parent's gene in possibilities of 0.5
                    ng.append(survive_set[i][1][k]) if rdi([1, 10]) <= 5  \
                    else ng.append(survive_set[j][1][k])
                new_pft = pft_Esitmate(daily_data, start_day, ng) #calculate the fitness function
                print('new creature:', new_pft, ng)
                new_set.append([new_pft, ng])
        #selection, find the top {generation_scale} creatures
        new_set.sort(key = sort_gene, reverse = True)
        pft_value = [a[0] for a in new_set[0:generation_scale]]
        #find the average profit and the max profit
        avg_pft_set.append([rd, sum(pft_value) / len(pft_value)])
        max_pft_set.append([rd, max(pft_value)])
        if new_set[0][0] > max_pft:
            max_pft = new_set[0][0]
            max_const = new_set[0][1]
        #new survive set
        survive_set = new_set[0:generation_scale]
        print('now max pft = ', max_pft, max_const)
        #mutation
        for i in range(1, generation_scale):
            for j in range(const_num): #mutation in the possibilities of 1/10
                if rdi([1, 100]) <= 10: survive_set[i][1][j] = rdi(const_range[j])

    return avg_pft_set, max_pft_set

def global_trends(daily_data):
    data_value = daily_data['open'].values
    dv = []
    up_trend = 0
    down_trend = 0
    for i in range(1, len(data_value)):
        dt = data_value[i] - data_value[i-1]
        dv.append(dt)
        if dt < 0 and dt < down_trend:
            down_trend = dt
        if dt > 0 and dt > up_trend:
            up_trend = dt;
    return down_trend, up_trend, dv


def main():
    filename = sys.argv[1]
    daily_data = pd.read_csv(filename)
    u, l, dv = global_trends(daily_data[2008:-1])
    print(u, l)
    n, bins, patches = plt.hist(x=dv, bins=100, color='#0504aa',
                            alpha=0.7, rwidth=0.7)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('disparity')
    plt.ylabel('Frequency')
    plt.show()

    #ga method
    '''
    generation_scale = 4
    test_round = 2000
    start_day = 2008#2008#2022
    const_range = [[1, 20], [21, 50], [1, 20], [21, 50], [0, 300], [0, 300], [0, 1], \
                   [0, 8], [0, 300], [0, 300], [0, 1], [0, 8], [0, 100], [0, 100]]
    avg_pft_set, max_pft_set = GA_Training(daily_data, generation_scale, \
                                           test_round, start_day, const_range)
    print(avg_pft_set)
    print('\n')
    print(max_pft_set)
    plot_data(plt, avg_pft_set)
    plot_data(plt, max_pft_set)
    plt.show()
    '''

main()






