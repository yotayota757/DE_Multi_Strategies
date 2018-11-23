from tkinter import *
from random import randint

# core imports for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
import time
import threading

from matplotlib import cm
from matplotlib import pyplot as plt
from figure import *
import individual as id

class Demo:
    def __init__(self):
        self.init()
 
    def init(self):
        """ initialize a window """
        root = Tk()
        root.config(background='white')
    
        WIDTH = 800
        HEIGHT = 800
        self.__continuePlotting = False
        self.__func = "rastrigin"
        self.__individuals = []
        for p in range(cf.get_population_size()):
            self.__individuals.append(id.Individual().get_position())

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
    
        Button(root, text="Start/Stop", command=self.gui_handler, bg="red", fg="white").pack()
        Button(root, text="Change function", command=self.change_func, bg="red", fg="white").pack()

        root.mainloop()
 
    def plotter(self):
        while self.__continuePlotting:
            self.__ax.cla()
            split_index = (int)(cf.get_population_ratio()*cf.get_population_size())
            list1 = self.__individuals[:split_index]
            list2 = self.__individuals[split_index:]
            # 毎回Zの計算をしているから遅いかも
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
 
if __name__ == '__main__':
    test = Demo()