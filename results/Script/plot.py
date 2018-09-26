# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import numpy as np
import os
import glob

# def find_all_files(directory):
#     for root, dirs, files in os.walk(directory):
#         yield root
#         for file in files:
#         	if file == (*.csv):
# 	            yield os.path.join(root, file)

def main(file_name):
  data = np.genfromtxt(file_name,delimiter=",")
  name = file_name.replace(".csv","")
  fig_name = name.zfill(14)
  fig = plt.figure()
  ax = fig.add_subplot(1,1,1)
  ax.scatter(data[0:15,0], data[0:15,0], color="blue", label="PSO") # １列目のデータをx軸の値、3列目のデータをy軸の値として与える。
  ax.scatter(data[16:30,0], data[16:30,1], color="orange", label="CS") # １列目のデータをx軸の値、3列目のデータをy軸の値として与える。
  ax.scatter(data[31:45,0], data[31:45,1], color="green", label="DE") # １列目のデータをx軸の値、3列目のデータをy軸の値として与える。
  ax.set_xlabel('x_1') # x軸
  ax.set_ylabel('x_2') # y軸
  # 動的用
  # ax.scatter(125 * np.sin(0.01*int(name)), - 125 * np.sin(0.01*int(name)), color="red", label="optimum")
  # plt.show() # グラフの描画
  plt.ylim(-500,500)
  plt.xlim(-500,500)
  plt.grid(color='gray',linestyle="dashed")
  plt.title(fig_name)
  plt.legend()
  fig.savefig("fig" + os.sep + fig_name + ".png")
  plt.close()
  print (fig_name + ".png : 出力完了!")

if __name__ == '__main__':
    # main()
    files = glob.glob("*.csv")
    for file in files: 
        # print (file)
    	main(file)
