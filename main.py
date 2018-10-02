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

        results_list = [] # fitness list
        de_list1 = [] # population list
        de_list2 = [] 
        # de_list = []
        """Generate Initial Population"""
        for p in range(cf.get_population_size_1()):
            de_list1.append(id.Individual())

        for p in range(cf.get_population_size_2()):
            de_list2.append(id.Individual())
        
        # for p in range(cf.get_population_size()):
        #     de_list.append(id.Individual())

        """Sort Array"""
        de_list1 =  sorted(de_list1, key=lambda ID : ID.get_fitness())
        de_list2 =  sorted(de_list2, key=lambda ID : ID.get_fitness())
        # de_list =  sorted(de_list, key=lambda ID : ID.get_fitness())

        """Find Initial Best"""
        BestPosition1 = de_list1[0].get_position() # Best Solution1
        BestFitness1 = fn.calculation(BestPosition1,0)
        BestPosition2 = de_list2[0].get_position() # Best Solution2
        BestFitness2 = fn.calculation(BestPosition2,0)
        # BestPosition = de_list[0].get_position() # Best Solution
        # BestFitness = fn.calculation(BestPosition,0)

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

                # candidate.generate(a=de_list[a], b=de_list[b], c=de_list[c], R=R)
                # DE動作
                candidate.rand_1(i,de_list1)
                # 評価値の確認
                candidate.set_fitness(fn.calculation(candidate.get_position(),iteration))
                tmp_list1[i].set_fitness(fn.calculation(tmp_list1[i].get_position(),iteration))

                if candidate.get_fitness() < tmp_list1[i].get_fitness():
                    tmp_list1[i] = copy.deepcopy(candidate)

            for i in range(len(tmp_list2)):
                candidate = copy.deepcopy(tmp_list2[i])

                # candidate.generate(a=de_list[a], b=de_list[b], c=de_list[c], R=R)
                # DE動作
                candidate.global_1(i,de_list2)
                # 評価値の確認
                candidate.set_fitness(fn.calculation(candidate.get_position(),iteration))
                tmp_list2[i].set_fitness(fn.calculation(tmp_list2[i].get_position(),iteration))

                if candidate.get_fitness() < tmp_list2[i].get_fitness():
                    tmp_list2[i] = copy.deepcopy(candidate)

            """Write Moved Position"""
            for i in range (len(tmp_list1)):
                pos_writer.writerow(tmp_list1[i].get_position())
            for i in range (len(tmp_list2)):
                pos_writer.writerow(tmp_list2[i].get_position())

            """Sort Array"""
            de_list1 = sorted(tmp_list1, key=lambda ID: ID.get_fitness())
            de_list2 = sorted(tmp_list2, key=lambda ID: ID.get_fitness())

            BestFitness1 = fn.calculation(BestPosition1,iteration)
            BestFitness2 = fn.calculation(BestPosition2,iteration)

            #Less is better
            """Rank and Find the Current Best"""
            if de_list1[0].get_fitness() < BestFitness1:
                BestPosition1 = de_list1[0].get_position()
                BestFitness1 = fn.calculation(BestPosition1,iteration)
            
            if de_list2[0].get_fitness() < BestFitness2:
                BestPosition2 = de_list2[0].get_position()
                BestFitness2 = fn.calculation(BestPosition2,iteration)

            # # File Close
            pos.close()
            # tmp.close()

            sys.stdout.write("\r Trial:%3d , Iteration:%7d, BestFitness1:%.4f, BestFitnesss2:%.4f" % (trial , iteration, BestFitness1, BestFitness2))
            # results_list.append(str(BestFitness))

        # results_writer.writerow(results_list)

if __name__ == '__main__':
    main()
    results.close()