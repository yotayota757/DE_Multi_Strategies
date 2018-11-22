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

continuePlotting = False
 
def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True

def data_points():
    f = open("data.txt", "w")
    for i in range(10):
        f.write(str(randint(0, 10))+'\n')
    f.close()
 
    f = open("data.txt", "r")
    data = f.readlines()
    f.close()
 
    l = []
    for i in range(len(data)):
        l.append(int(data[i].rstrip("\n")))
    return l

def app():
    # initialise a window.
    root = Tk()
    root.config(background='white')
    
    WIDTH = 800
    HEIGHT = 800

    #メインウィンドウのタイトルを変更
    root.title("Operating Demo")
    #ウインドウサイズ（「幅x高さ」で指定）
    root.geometry(str(WIDTH)+"x"+str(HEIGHT))
    
    lab = Label(root, text="Live Plotting", bg = 'white').pack()
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top",fill='both',expand=True)
 
    def plotter():
        while continuePlotting:
            ax.cla()
            ax.axis([-5.12, 5.12, -5.12, 5.12])
            # ヒートマップ用の値（配列）
            X = np.arange(-5.12, 5.12, 0.01)
            Y = np.arange(-5.12, 5.12, 0.01)
            X,Y = np.meshgrid(X, Y)
            # 背景関数
            Z = rastrigin(X, Y, A=10)
            # ax.grid()
            # dpts = data_points()
            # ax.plot(range(10), dpts, marker='o', color='orange')
            ax.imshow(Z, cmap=cm.jet, extent =[-5.12, 5.12, -5.12, 5.12])
            graph.draw()
            time.sleep(0.2)
 
    def gui_handler():
        change_state()
        threading.Thread(target=plotter).start()
 
    b = Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white")
    b.pack()
    
    root.mainloop()
 
if __name__ == '__main__':
    app()