import numpy as np
import individual as id
import function as fn
import sys
import copy
import os
import csv
from config import Config as cf
import pandas as pd

if os.path.exists("results"):
    pass
else:
    os.mkdir("results")

if os.path.exists("results"+os.sep+"position"):
    pass
else:
    os.mkdir("results"+os.sep+"position")

# if os.path.exists("results"+os.sep+"tmp"):
#     pass
# else:
#     os.mkdir("results"+os.sep+"tmp")

results = open("results" + os.sep + "results.csv", "w")
results_writer = csv.writer(results, lineterminator="\n")

def env_change(eval):
    if eval < cf.get_evaluation()/2:
        function = "rastrigin"
    else:
        function = "schwefel"

    return function

def fitness_update(fitness,best,improvement):
    if best > fitness:
        best = fitness
    improvement.append(best)
    return best,improvement

def main():
    all = pd.DataFrame()
    for trial in range(cf.get_trial()):
        np.random.seed(trial)

        if os.path.exists("results" + os.sep + "position" + os.sep + str(trial)):
            pass
        else:
            os.mkdir("results" + os.sep + "position" + os.sep + str(trial))

        # if os.path.exists("results" + os.sep + "tmp" + os.sep + str(trial)):
        #     pass
        # else:
        #     os.mkdir("results" + os.sep + "tmp" + os.sep + str(trial))

        offline = 0
        eval = 0
        iteration = 0
        function = "rastrigin"
        BestFitness = 10000

        results_list = [] # fitness list
        # de_list1 = [] # population list
        # de_list2 = [] 
        de_all_list = []
        improvement = []

        """Generate Initial Population"""
        for _ in range(cf.get_population_size()):
            individual = id.Individual(function)
            de_all_list.append(individual)
            eval += 1
            BestFitness, improvement= fitness_update(fn.calculation(individual.get_position(),function),BestFitness,improvement)
            
        """Sort Array"""
        de_all_list =  sorted(de_all_list, key=lambda ID : ID.get_fitness())

        """"split list into two list"""
        split_index = (int)(cf.get_population_ratio()*cf.get_population_size())
        de_list1 = de_all_list[:split_index]
        de_list2 = de_all_list[split_index:]

        """Find Initial Best"""
        BestPosition = de_list1[0].get_position() # Best Solution
        BestFitness = fn.calculation(BestPosition,function)

        """↓↓↓Main Loop↓↓↓"""
        # for iteration in range(cf.get_iteration()):
        while eval < cf.get_evaluation():
            if cf.get_evaluation()-eval < cf.get_population_size():
                break

            pos = open("results" + os.sep + "position" + os.sep + str(trial) + os.sep + str(iteration).zfill(6) + ".csv", "w")
            pos_writer = csv.writer(pos, lineterminator="\n")

            # tmp = open("results" + os.sep + "tmp" + os.sep + str(trial) + os.sep + str(iteration).zfill(6) + ".csv", "w")
            # tmp_writer = csv.writer(tmp, lineterminator="\n")

            # """Write tmp position"""
            # for i in range (len(de_list)):
            #     tmp_writer.writerow(de_list[i].get_position())

            """list copy"""
            # tmp_list = copy.deepcopy(de_list)
            tmp_list1 = copy.deepcopy(de_list1)
            tmp_list2 = copy.deepcopy(de_list2)

            """Generate New Solutions"""
            for i in range(len(tmp_list1)):
                candidate = copy.deepcopy(tmp_list1[i])

                # DE動作
                candidate.global_1(i,de_list1)
                # 評価値の確認
                candidate.set_fitness(fn.calculation(candidate.get_position(),function))
                tmp_list1[i].set_fitness(fn.calculation(tmp_list1[i].get_position(),function))

                if candidate.get_fitness() < tmp_list1[i].get_fitness():
                    tmp_list1[i] = copy.deepcopy(candidate)
                eval += 1
                function = env_change(eval)
                BestFitness, improvement= fitness_update(fn.calculation(tmp_list1[i].get_position(),function),BestFitness,improvement)

            for i in range(len(tmp_list2)):
                candidate = copy.deepcopy(tmp_list2[i])

                # DE動作
                candidate.local_neighborhood(i,de_list2)
                # 評価値の確認
                candidate.set_fitness(fn.calculation(candidate.get_position(),function))
                tmp_list2[i].set_fitness(fn.calculation(tmp_list2[i].get_position(),function))

                if candidate.get_fitness() < tmp_list2[i].get_fitness():
                    tmp_list2[i] = copy.deepcopy(candidate)
                eval += 1
                function = env_change(eval)
                BestFitness, improvement= fitness_update(fn.calculation(tmp_list2[i].get_position(),function),BestFitness,improvement)
            
            """check exclusionable solution"""
            for i in range(len(tmp_list2)):
                current_distance = 0
                for j in range(len(tmp_list2)):
                    if i == j:
                        continue 
                    for dim in range(cf.get_dimension()):
                        current_distance = current_distance + (tmp_list2[i].get_position()[dim] - tmp_list2[j].get_position()[dim])**2
                    current_distance =  np.sqrt(current_distance)
                    if current_distance < cf.get_exclusion_dist():
                        if tmp_list2[i].get_fitness() > tmp_list2[j].get_fitness():
                            tmp_list2[i].init(function)
                            BestFitness, improvement= fitness_update(fn.calculation(tmp_list2[i].get_position(),function),BestFitness,improvement)
                        else:
                            tmp_list2[j].init(function)
                            BestFitness, improvement= fitness_update(fn.calculation(tmp_list2[j].get_position(),function),BestFitness,improvement)
                        eval += 1
                        function = env_change(eval)
                        
            
            """Sort Array"""
            de_all_list = tmp_list1 + tmp_list2
            # de_all_list.append(tmp_list2) # 型がリストになってしまう
            # 上位A%で切り分け
            de_all_list = sorted(de_all_list, key=lambda ID: ID.get_fitness())
            split_index = (int)(cf.get_population_ratio()*cf.get_population_size())
            de_list1 = de_all_list[:split_index]
            de_list2 = de_all_list[split_index:]

            # 前iteration の position
            BestFitness = fn.calculation(BestPosition,function)

            #Less is better
            """Rank and Find the Current Best"""
            if de_list1[0].get_fitness() < BestFitness:
                BestPosition = de_list1[0].get_position()
                BestFitness = fn.calculation(BestPosition,function)
            
            """Write Moved Position"""
            for i in range (len(de_list1)):
                pos_writer.writerow(de_list1[i].get_position())
            for i in range (len(de_list2)):
                pos_writer.writerow(de_list2[i].get_position())

            # # File Close
            pos.close()
            # tmp.close()

            sys.stdout.write("\r Trial:%3d , Iteration:%7d, Evaluation:%7d, BestFitness:%.4f" % (trial , iteration, eval, BestFitness))
            results_list.append(str(BestFitness))
            offline = offline + BestFitness
            iteration += 1

        results_list.append("")
        results_list.append(str(offline/cf.get_iteration()))
        results_writer.writerow(results_list)
        all = pd.DataFrame(improvement)
        all.to_csv("./results/fitness_by_evaluation/trial"+str(trial)+".csv")
        

if __name__ == '__main__':
    main()
    results.close()