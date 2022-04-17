import numpy as np
import random


def cal_re(results, nets, grid_num):
    wl = 0
    con = np.zeros((grid_num, grid_num))
    for net in nets:
        left = grid_num-1
        right = 0
        up = grid_num-1
        down = 0
        for i in net:
            left = min(left, results[i][1])
            right = max(right, results[i][1])
            up = min(up, results[i][0])
            down = max(down, results[i][0])
        wn = int(right-left+1)
        hn = int(down-up+1)
        dn = (wn+hn) / (wn*hn)
        con[up:down+1, left:right+1] += dn
        wl += wn + hn
    con = list(con.flatten())
    con.sort(reverse=True)
    return (-np.mean(con[:grid_num]) - (wl-34000)*0.1)*0.2

class individual:
    def __init__(self, pur, eval):
        self.pur = pur
        self.eval = eval

def PMX(indiv1, indiv2, nets, grid_num, macro_num):
    count1 = macro_num
    count2 = macro_num
    pur1 = indiv1.pur.copy()
    pur2 = indiv2.pur.copy()
    for i in range(len(pur1)):
        if pur1[i] == -1:
            pur1[i] = count1
            count1 += 1
        if pur2[i] == -1:
            pur2[i] = count2
            count2 += 1
    a, b = random.sample(list(range(len(pur1))),k=2)
    start = min(a, b)
    end = max(a, b)
    segment = pur1[start:end].copy()
    pur = [-2 for i in range(grid_num*grid_num)]
    pur[start:end] = segment
    for i in range(start,end):
        if pur2[i] in segment:
            continue
        z = pur1[i]
        idx = pur2.index(z)
        while idx >= start and idx < end:
            z = pur1[idx]
            idx = pur2.index(z)
        pur[idx] = pur2[i]
    for i in range(len(pur)):
        if pur[i] == -2:
            pur[i] = pur2[i]
    #print(pur)
    for i in range(len(pur)):
        if pur[i] >= macro_num:
            pur[i] = -1
    son = individual(pur, -9999)
    return son

def EX(indiv1, indiv2, nets, grid_num, macro_num):
    count1 = macro_num
    count2 = macro_num
    pur1 = indiv1.pur.copy()
    pur2 = indiv2.pur.copy()
    for i in range(len(pur1)):
        if pur1[i] == -1:
            pur1[i] = count1
            count1 += 1
        if pur2[i] == -1:
            pur2[i] = count2
            count2 += 1
    edge_list = []
    for _ in range(len(pur1)):
        edge_list.append([])
    for idx in range(len(pur1)):
        edge_list[pur1[idx]].append(pur1[idx-1])
        edge_list[pur1[idx]].append(pur1[(idx+1)%len(pur1)])
        edge_list[pur2[idx]].append(pur2[idx-1])
        edge_list[pur2[idx]].append(pur2[(idx+1)%len(pur1)])
    unplaced = list(range(len(pur1)))
    pur = []
    for i in range(len(pur1)):
        if pur == []:
            idx = random.choice(list(range(len(pur1))))
            for item in edge_list:
                while idx in item:
                    item.remove(idx)
            pur.append(idx)
            unplaced.remove(idx)
        else:
            last_idx = pur[-1]

            working_list = edge_list[last_idx].copy()
            working_set = set(working_list)
            if len(working_list) == len(working_set):
                working_list.sort(key=lambda x:len(set(edge_list[x])))
                if working_list == []:
                    idx = random.choice(unplaced)
                else:
                    idx = working_list[0]
                for item in edge_list:
                    while idx in item:
                        item.remove(idx)
                pur.append(idx)
                unplaced.remove(idx)
            else:
                for item in working_set:
                    working_list.remove(item)  
                if working_list == []:      
                    idx = random.choice(unplaced)
                else: 
                    idx = working_list[0]
                for item in edge_list:
                    while idx in item:
                        item.remove(idx)
                pur.append(idx)
                unplaced.remove(idx)
    son = individual(pur, -9999)
    return son

def CX(indiv1, indiv2, nets, grid_num, macro_num):
    count1 = macro_num
    count2 = macro_num
    pur1 = indiv1.pur.copy()
    pur2 = indiv2.pur.copy()
    for i in range(len(pur1)):
        if pur1[i] == -1:
            pur1[i] = count1
            count1 += 1
        if pur2[i] == -1:
            pur2[i] = count2
            count2 += 1
    pur_son1 = [-2 for x in range(grid_num*grid_num)]
    pur_son2 = [-2 for x in range(grid_num*grid_num)]
    count = 0
    idces = list(range(grid_num*grid_num))
    while idces != []:
        reached = []
        idx = idces[0]
        while True:
            reached.append(idx)
            idces.remove(idx)
            r = pur2[idx]
            idx = pur1.index(r)
            if idx in reached:
                break
        for item in reached:
            if count % 2 == 0:
                #print(count)
                pur_son1[item] = pur1[item]
                pur_son2[item] = pur2[item]
            else:
                #print(count)
                pur_son2[item] = pur1[item]
                pur_son1[item] = pur2[item]
        count += 1
    for i in range(len(pur_son1)):
        if pur_son1[i] >= macro_num:
            pur_son1[i] = -1
        if pur_son2[i] >= macro_num:
            pur_son2[i] = -1
    son1 = individual(pur_son1, -9999)
    return son1

def OX(indiv1, indiv2, nets, grid_num, macro_num):
    pur1 = indiv1.pur.copy()
    pur2 = indiv2.pur.copy()
    count1 = macro_num
    count2 = macro_num
    for i in range(len(pur1)):
        if pur1[i] == -1:
            pur1[i] = count1
            count1 += 1
        if pur2[i] == -1:
            pur2[i] = count2
            count2 += 1
    a, b = random.sample(list(range(len(pur1))),k=2)
    start = min(a, b)
    end = max(a, b)
    segment = pur1[start:end].copy()
    #print(segment)
    for item in segment:
        idx = pur2.index(item)
        pur2.pop(idx)
    pur = pur2[:start] + segment + pur2[start:]
    #print(len(pur))
    for i in range(len(pur)):
        if pur[i] >= macro_num:
            pur[i] = -1
    son = individual(pur, -9999)
    return son

def insert(indiv, nets, grid_num, macro_num):
    pur = indiv.pur.copy()
    a, b = random.sample(list(range(grid_num*grid_num)),k=2)
    start = min(a, b)
    end = max(a, b)
    if end - start == 1:
        return indiv
    tmp = pur[end]
    for i in range(end, start+1, -1):
        pur[i] = pur[i-1]
    pur[start+1] = tmp
    eva = evaluation(pur, nets, grid_num, macro_num)
    indiv_new = individual(pur, eva)
    return indiv_new


def swap(indiv, nets, grid_num, macro_num):
    pur = indiv.pur.copy()
    idx1 = random.choice(range(grid_num*grid_num))
    idx2 = random.choice(range(grid_num*grid_num))
    # print(pur[idx1],pur[idx2])
    tmp = pur[idx1]
    pur[idx1] = pur[idx2]
    pur[idx2] = tmp
    # print(pur[idx1],pur[idx2])
    eva = evaluation(pur, nets, grid_num, macro_num)
    indiv_new = individual(pur, eva)
    return indiv_new

def scramble(indiv, nets, grid_num, macro_num):
    pur = indiv.pur.copy()
    backup = pur.copy()
    chosen = []
    for i in range(len(pur)):
        flag = random.random()
        if flag < 3/len(pur):
            chosen.append(i)
    chosen_back = chosen.copy()
    if chosen != []:
        random.shuffle(chosen)
        for i in range(len(chosen)):
            pur[chosen_back[i]] = backup[chosen[i]]
    eva = evaluation(pur, nets, grid_num, macro_num)
    indiv_new = individual(pur, eva)
    return indiv_new

def inversion(indiv, nets, grid_num, macro_num):
    pur = indiv.pur.copy()
    a, b = random.sample(list(range(len(pur))),k=2)
    start = min(a, b)
    end = max(a, b)
    segment = pur[start:end+1].copy()
    for i in range(start, end+1):
        pur[i] = segment[end-i]
    eva = evaluation(pur, nets, grid_num, macro_num)
    indiv_new = individual(pur, eva)
    return indiv_new

def evaluation(pur, nets, grid_num, macro_num): 
    ls = []
    for i in range(macro_num):
        pos = pur.index(i)
        x = pos // grid_num
        y = pos % grid_num
        ls.append([x, y])
    return cal_re(ls, nets, grid_num)

def init(popsize, nets, grid_num, macro_num):
    pop = []
    for i in range(popsize):
        ls = [x for x in range(macro_num)] 
        pos = list(range(grid_num*grid_num))
        pur = [-1 for x in range(grid_num*grid_num)] 
        for node in ls:
            position = random.choice(pos)
            pos.remove(position)
            pur[position] = node
        eva = evaluation(pur, nets, grid_num, macro_num)
        print(eva)
        indiv = individual(pur, eva)
        pop.append(indiv)
    return pop
