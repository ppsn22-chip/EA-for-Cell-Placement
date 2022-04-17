import time
import csv
import random
import argparse
from ea_operators import PMX, swap, init, insert, scramble, inversion, CX, OX, EX

def get_args():
    parser = argparse.ArgumentParser(description='RL')
    parser.add_argument(
        '--crossover', default='PMX', help='crossover operator to use: PMX | CX | OX | EX')
    parser.add_argument(
        '--mutation', default='swap', help='mutation operator to use: swap | scramble | inversion | insert')
    parser.add_argument(
        '--popsize', default=10, help='size of the population')
    parser.add_argument(
        '--max_eval', default=50000, help='evaluation budget')
    parser.add_argument(
        '--grid_num', default=32, help='number of grids')
    parser.add_argument(
        '--draw_layout', default=False, help='wheather draw the final layout')
    parser.add_argument(
        '--save_data', default=False, help='whether save intermediate result')
    parser.add_argument(
        '--netlist_dir', default="n_edges_710.dat", help='directory of netlist')    
    parser.add_argument(
        '--save_dir', default="result.csv", help='directory of saved data')
    parser.add_argument(
        '--macro_num', default=710, help='number of macros to place')
    args = parser.parse_args()
    return args


class individual:
    def __init__(self, pur, eval):
        self.pur = pur
        self.eval = eval
  


if __name__ == "__main__":
    args = get_args()
    popsize = args.popsize
    grid_num = args.grid_num
    max_eval = args.max_eval
    macro_num = args.macro_num
    data = []
    f = open(args.netlist_dir, "r")
    for line in f:
        nets = eval(line)
    pop = init(popsize, nets, grid_num, macro_num)
    eval_time = 0
    glob_best = -9999
    switch = {'PMX': PMX,
              'CX': CX,
              'EX': EX,
              'OX': OX,
              'swap': swap,
              'insert': insert,
              'inversion': inversion,
              'scramble': scramble}
    for _ in range(max_eval):
        sons = []
        for i in range(popsize):
            indiv1 = random.choice(pop)
            indiv2 = random.choice(pop)
            son = switch.get(args.crossover)(indiv1, indiv2, nets, grid_num, macro_num)
            son = switch.get(args.mutation)(son, nets, grid_num, macro_num)
            if son.eval > glob_best:
                glob_best = son.eval
            eval_time += 1
            data.append([glob_best,eval_time,time.time()])
            sons.append(son)
        pop += sons
        pop = sorted(pop, key = lambda x: x.eval, reverse = True)
        pop = pop[:popsize]
        print(_, pop[0].eval)


    if args.save_data:
        csvFile = open(args.save_dir, "w")
        writer = csv.writer(csvFile)
        for item in data:
            writer.writerow(item)
        csvFile.close()
    