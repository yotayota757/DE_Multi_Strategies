import numpy as np
import individual as id
import function as fn
import sys
import copy
import os
import csv
from config import Config as cf
from movingpeaks import MovingPeaks
from matplotlib import cm
from matplotlib import pyplot as plt

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

        print_image = False
        mpb = MovingPeaks(dim=cf.get_dimension(), npeaks = 10, number_severity=1)
        offline = 0

        results_list = [] # fitness list
        de_all_list = []

        """Generate Initial Population"""
        for _ in range(cf.get_population_size()):
            de = id.Individual()
            de.set_fitness(fn.calc_mpb(de.get_position(),0,mpb,True))
            de_all_list.append(de)
        
        """Sort Array"""
        de_all_list =  sorted(de_all_list, key=lambda ID : ID.get_fitness(),reverse=True)

        """"split list into two list"""
        split_index = (int)(cf.get_population_ratio()*cf.get_population_size())
        de_list1 = de_all_list[:split_index]
        de_list2 = de_all_list[split_index:]

        """Find Initial Best"""
        BestPosition = de_list1[0].get_position() # Best Solution
        BestFitness = fn.calc_mpb(BestPosition,0,mpb,False)

        """↓↓↓Main Loop↓↓↓"""
        for iteration in range(cf.get_iteration()):
            # 環境変化知覚 for printing image
            if mpb.env_changed and print_image:
                # 背景関数
                Z = []
                Y = np.arange(100,0,-0.1)
                X = np.arange(0,100,0.1)
                for y in Y:
                    z = []
                    for x in X:
                        pos = [x,y]
                        z.append(mpb.__call__(pos, count=False)[0])
                    Z.append(z)
                mpb.got_env_info()

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
                candidate.set_fitness(fn.calc_mpb(candidate.get_position(),iteration,mpb,True))
                tmp_list1[i].set_fitness(fn.calc_mpb(tmp_list1[i].get_position(),iteration,mpb,False))

                if candidate.get_fitness() > tmp_list1[i].get_fitness():
                    tmp_list1[i] = copy.deepcopy(candidate)

            for i in range(len(tmp_list2)):
                candidate = copy.deepcopy(tmp_list2[i])

                # DE動作
                candidate.local_neighborhood(i,de_list2)
                # 評価値の確認
                candidate.set_fitness(fn.calc_mpb(candidate.get_position(),iteration,mpb,True))
                tmp_list2[i].set_fitness(fn.calc_mpb(tmp_list2[i].get_position(),iteration,mpb,False))

                if candidate.get_fitness() > tmp_list2[i].get_fitness():
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
                        if tmp_list2[i].get_fitness() < tmp_list2[j].get_fitness():
                            tmp_list2[i].init()
                            tmp_list2[i].set_fitness(fn.calc_mpb(tmp_list2[i].get_position(),iteration,mpb,True))
                        else:
                            tmp_list2[j].init()
                            tmp_list2[j].set_fitness(fn.calc_mpb(tmp_list2[j].get_position(),iteration,mpb,True))
            
            """Sort Array"""
            de_all_list = tmp_list1 + tmp_list2
            # de_all_list.append(tmp_list2) # 型がリストになってしまう
            # 上位A%で切り分け
            de_all_list = sorted(de_all_list, key=lambda ID: ID.get_fitness(),reverse=True)
            split_index = (int)(cf.get_population_ratio()*cf.get_population_size())
            de_list1 = de_all_list[:split_index]
            de_list2 = de_all_list[split_index:]

            # 前iteration の position
            BestFitness = fn.calc_mpb(BestPosition,iteration,mpb,False)

            #Less is better
            """Rank and Find the Current Best"""
            if de_list1[0].get_fitness() > BestFitness:
                BestPosition = de_list1[0].get_position()
                BestFitness = fn.calc_mpb(BestPosition,iteration,mpb,False)
            
            """Write Moved Position"""
            for i in range (len(de_list1)):
                pos_writer.writerow(de_list1[i].get_position())
            for i in range (len(de_list2)):
                pos_writer.writerow(de_list2[i].get_position())

            # # File Close
            pos.close()
            # tmp.close()

            if print_image:
                name = str(iteration)
                fig_name = name.zfill(6)
                fig = plt.figure() 
                ax = fig.add_subplot(1,1,1)
                # ヒートマップの生成
                ax.imshow(Z, cmap=cm.jet, extent =[0, 100, 0, 100])
                # 解集団のプロット
                for de in de_list1:
                    ax.scatter(de.get_position()[0], de.get_position()[1], c = 'm', alpha = 0.5) # １列目のデータをx軸の値、2列目のデータをy軸の値として与える。   
                for de in de_list2:
                    # exclusion範囲の表示
                    ax.scatter(de.get_position()[0], de.get_position()[1], s = cf.get_exclusion_dist(), c = 'k', alpha = 0.5)
                    ax.scatter(de.get_position()[0], de.get_position()[1], c = 'w', alpha = 0.5) # 50行目以降
                ax.axis([0, 100, 0, 100])

                fig.savefig("./results/figure/" + fig_name + ".png")
                # plt.show() # グラフの描画
                plt.close()

            sys.stdout.write("\r Trial:%3d , Iteration:%7d, BestFitness:%.4f" % (trial , iteration, BestFitness))
            results_list.append(str(BestFitness))
            offline = offline + BestFitness
        results_list.append("")
        results_list.append(str(mpb.offlineError()))
        results_writer.writerow(results_list)

if __name__ == '__main__':
    main()
    results.close()