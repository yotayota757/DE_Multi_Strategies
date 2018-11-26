from tkinter import *
# core imports for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading

from matplotlib import cm
from matplotlib import pyplot as plt
from figure import *

import individual as id
import function as fn
import copy

class Demo:
    def __init__(self):
        self.init()
 
    def init(self):
        """ initialize a window """
        root = Tk()
        root.config(background='white')
    
        WIDTH = 800
        HEIGHT = 800
        self.__continuePlotting = True
        self.__func = "rastrigin"
        self.__individuals = []

        #メインウィンドウのタイトルを変更
        root.title("Operating Demo")
        #ウインドウサイズ（「幅x高さ」で指定）
        root.geometry(str(WIDTH)+"x"+str(HEIGHT))
    
        Label(root, text="Live Plotting", bg = 'white').pack()
    
        fig = plt.figure()
        self.__ax = fig.add_subplot(1,1,1)
        
        # tkinter設定
        self.__graph = FigureCanvasTkAgg(fig, master=root)
        self.__graph.get_tk_widget().pack(side="top",fill='both',expand=True)

        # for creating heatmap
        # rastrigin
        # ヒートマップ用の値（配列）
        X = np.arange(-5.12, 5.12, 0.01)
        Y = np.arange(-5.12, 5.12, 0.01)
        X,Y = np.meshgrid(X, Y)
        # 背景関数
        self.__rast_heat = rastrigin(X, Y, A=10)

        # schwefel
        # ヒートマップ用の値（配列）
        X = np.arange(-512, 512, 1)
        Y = np.arange(512, -512, -1)
        X,Y = np.meshgrid(X, Y)
        # 背景関数
        self.__sch_heat = schwefel(X, Y, A=418.9829)
    
        Button(root, text="Start/Stop", command=self.gui_handler, bg="green", fg="black").pack()
        Button(root, text="Change function", command=self.change_func, bg="green", fg="black").pack()
        Button(root, text="quit", command=self.quit,bg="red",fg="white").pack()
        self.root = root
        self.root.mainloop()
        
        # self.thread_plot = threading.Thread(target=self.plotter)
        # self.thread_plot.daemon = True
        # self.thread_plot.start()
        # self.thread_main = threading.Thread(target=self.main)
        # self.thread_main.daemon = True
        # self.thread_main.start()
        # threading.Thread(target=self.main).start()


    # DEの動作
    def main(self):
        while True:
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
            BestFitness = self.calculation(BestPosition)

            """↓↓↓Main Loop↓↓↓"""
            for iteration in range(cf.get_iteration()):
                while not self.__continuePlotting:
                    time.sleep(0.3)
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
                    candidate.set_fitness(self.calculation(candidate.get_position()))
                    tmp_list1[i].set_fitness(self.calculation(tmp_list1[i].get_position()))

                    if candidate.get_fitness() < tmp_list1[i].get_fitness():
                        tmp_list1[i] = copy.deepcopy(candidate)

                for i in range(len(tmp_list2)):
                    candidate = copy.deepcopy(tmp_list2[i])

                    # DE動作
                    candidate.local_neighborhood(i,de_list2)
                    # 評価値の確認
                    candidate.set_fitness(self.calculation(candidate.get_position()))
                    tmp_list2[i].set_fitness(self.calculation(tmp_list2[i].get_position()))

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
                BestFitness = self.calculation(BestPosition)

                #Less is better
                """Rank and Find the Current Best"""
                if de_list1[0].get_fitness() < BestFitness:
                    BestPosition = de_list1[0].get_position()
                    BestFitness = self.calculation(BestPosition) 
                
                self.update_position(de_all_list)
                time.sleep(0.5)
 
    def plotter(self):
        while self.__continuePlotting:
            position_list = []
            for ind in self.__individuals:
                position_list.append(ind.get_position())
            split_index = (int)(cf.get_population_ratio()*len(position_list))
            list1 = position_list[:split_index]
            list2 = position_list[split_index:]
            self.__ax.cla()
            if self.__func == "rastrigin":
                # ヒートマップ生成
                self.__ax.imshow(self.__rast_heat, cmap=cm.jet, extent =[-5.12, 5.12, -5.12, 5.12])
                # 解集団のプロット
                for ind in list1:
                    self.__ax.scatter(ind[0]/100,ind[1]/100, c = 'm', alpha = 0.8) # １列目のデータをx軸の値、2列目のデータをy軸の値として与える。   
                # exclusion範囲の表示
                for ind in list2:
                    self.__ax.scatter(ind[0]/100, ind[1]/100, s = cf.get_exclusion_dist(), c = 'k')
                    self.__ax.scatter(ind[0]/100, ind[1]/100, c = 'w') # 50行目以降
            elif self.__func == "schwefel":
                # ヒートマップの生成
                self.__ax.imshow(self.__sch_heat, cmap=cm.jet, extent =[-512, 512, -512, 512])
                # 解集団のプロット
                for ind in list1:
                    self.__ax.scatter(ind[0],ind[1], c = 'm', alpha = 0.8) # １列目のデータをx軸の値、2列目のデータをy軸の値として与える。   
                # exclusion範囲の表示
                for ind in list2:
                    self.__ax.scatter(ind[0], ind[1], s = cf.get_exclusion_dist(), c = 'k')
                    self.__ax.scatter(ind[0], ind[1], c = 'w') # 50行目以降
            else:
                print("error no function is defined for demo")

            # 描画
            self.__graph.draw()

    def calculation(self,position):
        if self.__func == "rastrigin":
            return fn.rastrigin(position)
        else:
            return fn.schwefel(position)

    def update_position(self,de_list):
        self.__individuals = de_list

    def change_func(self):
        if self.__func == "rastrigin":
            self.__func = "schwefel"
        else:
            self.__func = "rastrigin"

    def change_state(self):
        if self.__continuePlotting == True:
            self.__continuePlotting = False
        else:
            self.__continuePlotting = True

    def gui_handler(self):
        self.change_state()
        threading.Thread(target=self.plotter).start()
        threading.Thread(target=self.main).start()

    def quit(self):
        self.root.destroy()
 
if __name__ == '__main__':
    test = Demo()