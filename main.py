import numpy as np
import individual as id
import function as fn
import sys
import copy
import os
import csv
from config import Config as cf

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


def main():
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

        results_list = [] # fitness list
        # de_list1 = [] # population list
        # de_list2 = [] 
        de_all_list = []

        """Generate Initial Population"""
        for p in range(cf.get_population_size()):
            de_all_list.append(id.Individual())
        
        """Sort Array"""
        de_all_list =  sorted(de_all_list, key=lambda ID : ID.get_fitness())

        """"split list into two list"""
        split_index = (int)(cf.get_population_ratio()*cf.get_population_size())
        de_list1 = de_all_list[:split_index]
        de_list2 = de_all_list[split_index:]

        """Find Initial Best"""
        BestPosition = de_list1[0].get_position() # Best Solution
        BestFitness = fn.calculation(BestPosition,0)

        """↓↓↓Main Loop↓↓↓"""
        for iteration in range(cf.get_iteration()):

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
                candidate.set_fitness(fn.calculation(candidate.get_position(),iteration))
                tmp_list1[i].set_fitness(fn.calculation(tmp_list1[i].get_position(),iteration))

                if candidate.get_fitness() < tmp_list1[i].get_fitness():
                    tmp_list1[i] = copy.deepcopy(candidate)

            for i in range(len(tmp_list2)):
                candidate = copy.deepcopy(tmp_list2[i])

                # DE動作
                candidate.local_neighborhood(i,de_list2)
                # 評価値の確認
                candidate.set_fitness(fn.calculation(candidate.get_position(),iteration))
                tmp_list2[i].set_fitness(fn.calculation(tmp_list2[i].get_position(),iteration))

                if candidate.get_fitness() < tmp_list2[i].get_fitness():
                    tmp_list2[i] = copy.deepcopy(candidate)
            
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
                            tmp_list2[i].init(iteration)
                        else:
                            tmp_list2[j].init(iteration)
            
            """Sort Array"""
            de_all_list = tmp_list1 + tmp_list2
            # de_all_list.append(tmp_list2) # 型がリストになってしまう
            # 上位A%で切り分け
            de_all_list = sorted(de_all_list, key=lambda ID: ID.get_fitness())
            split_index = (int)(cf.get_population_ratio()*cf.get_population_size())
            de_list1 = de_all_list[:split_index]
            de_list2 = de_all_list[split_index:]

            # 前iteration の position
            BestFitness = fn.calculation(BestPosition,iteration)

            #Less is better
            """Rank and Find the Current Best"""
            if de_list1[0].get_fitness() < BestFitness:
                BestPosition = de_list1[0].get_position()
                BestFitness = fn.calculation(BestPosition,iteration)
            
            """Write Moved Position"""
            for i in range (len(de_list1)):
                pos_writer.writerow(de_list1[i].get_position())
            for i in range (len(de_list2)):
                pos_writer.writerow(de_list2[i].get_position())

            # # File Close
            pos.close()
            # tmp.close()

            sys.stdout.write("\r Trial:%3d , Iteration:%7d, BestFitness:%.4f" % (trial , iteration, BestFitness))
            results_list.append(str(BestFitness))
            offline = offline + BestFitness
        results_list.append("")
        results_list.append(str(offline/cf.get_iteration()))
        results_writer.writerow(results_list)

if __name__ == '__main__':
    main()
    results.close()