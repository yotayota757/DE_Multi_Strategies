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
        """Generate Initial Population"""
        for p in range(cf.get_population_size()):
            de_list1.append(id.Individual())

        for p in range(cf.get_population_size()):
            de_list2.append(id.Individual())

        """Sort Array"""
        de_list =  sorted(de_list, key=lambda ID : ID.get_fitness())

        """Find Initial Best"""
        BestPosition = de_list[0].get_position() # Best Solution
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
            tmp_list = copy.deepcopy(de_list)

            """Generate New Solutions"""
            for i in range(len(tmp_list)):

                candidate = copy.deepcopy(tmp_list[i])

                """select three points (a, b, c)"""
                if(de_list[i].get):
                    a = np.random.randint(0, cf.get_population_size())
                    while (a == i):
                        a = np.random.randint(0, cf.get_population_size())
                else:
                    a = 0
                b = np.random.randint(0, cf.get_population_size())
                while (b == i or a == b):
                    b = np.random.randint(0, cf.get_population_size())
                c = np.random.randint(0, cf.get_population_size())
                while (c == i or c == a or c == b):
                    c = np.random.randint(0, cf.get_population_size())

                """Select Random Index (R)"""
                R = np.random.randint(0,cf.get_dimension())

                candidate.generate(a=de_list[a], b=de_list[b], c=de_list[c], R=R)
                candidate.set_fitness(fn.calculation(candidate.get_position(),iteration))
                tmp_list[i].set_fitness(fn.calculation(tmp_list[i].get_position(),iteration))

                if candidate.get_fitness() < tmp_list[i].get_fitness():
                    tmp_list[i] = copy.deepcopy(candidate)

            """Write Moved Position"""
            for i in range (len(de_list)):
                pos_writer.writerow(de_list[i].get_position())

            """Sort Array"""
            de_list = sorted(tmp_list, key=lambda ID: ID.get_fitness())


            BestFitness = fn.calculation(BestPosition,iteration)

            #Less is better
            """Rank and Find the Current Best"""
            if de_list[0].get_fitness() < BestFitness:
                BestPosition = de_list[0].get_position()
                BestFitness = fn.calculation(BestPosition,iteration)

            # # File Close
            pos.close()
            # tmp.close()

            sys.stdout.write("\r Trial:%3d , Iteration:%7d, BestFitness:%.4f" % (trial , iteration, BestFitness))
            results_list.append(str(BestFitness))

        results_writer.writerow(results_list)

if __name__ == '__main__':
    main()
    results.close()