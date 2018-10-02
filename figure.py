from matplotlib import cm
from matplotlib import pyplot as plt
import math
import numpy as np
import os
import sys
import glob

def rastrigin(*X, **kwargs):
  A = kwargs.get('A', 10)
  return A*len(X) + sum([(x**2 - A * np.cos(2 * math.pi * x)) for x in X])

def schwefel(*X, **kwargs):
  A = kwargs.get('A', 418.9829)
  return A*len(X) - sum([(x * np.sin(np.sqrt(np.abs(x)))) for x in X])
    
    
def main(file_name):
  population = 50
  data1 = np.genfromtxt(file_name,delimiter=",",max_rows=population)
  data2 = np.genfromtxt(file_name,delimiter=",",skip_header=population)
  name = file_name.replace(".csv","")
  fig_name = name.zfill(6)
  fig = plt.figure() 
  ax = fig.add_subplot(1,1,1)

  # if (int(name) < 30):
  #   # ヒートマップ用の値（配列）
  #   X = np.arange(-512, 512, 1)
  #   Y = np.arange(512, -512, -1)
  #   X,Y = np.meshgrid(X, Y)
  #   # 背景関数
  #   Z = schwefel(X, Y, A=418.9829)
  #   # ヒートマップの生成
  #   ax.imshow(Z, cmap=cm.jet, extent =[-512, 512, -512, 512])
  #   # 解集団のプロット
  #   ax.scatter(data[:,0], data[:,1], c = 'm', alpha = 0.5) # １列目のデータをx軸の値、2列目のデータをy軸の値として与える。
  #   ax.axis([-512, 512, -512, 512])
  # else:
  #   # ヒートマップ用の値（配列）
  #   X = np.arange(-5.12, 5.12, 0.01)
  #   Y = np.arange(-5.12, 5.12, 0.01)
  #   X,Y = np.meshgrid(X, Y)
  #   # 背景関数
  #   Z = rastrigin(X, Y, A=10)
  #   # ヒートマップの生成
  #   ax.imshow(Z, cmap=cm.jet, extent =[-5.12, 5.12, -5.12, 5.12])
  #   # 解集団のプロット
  #   ax.scatter(data[:,0]/100, data[:,1]/100, c = 'm', alpha = 0.5) # １列目のデータをx軸の値、2列目のデータをy軸の値として与える。  
  #   ax.axis([-5.12, 5.12, -5.12, 5.12])
    

  # ヒートマップ用の値（配列）rastrigin
  # X = np.arange(-5.12, 5.12, 0.01)
  # Y = np.arange(-5.12, 5.12, 0.01)
  # X,Y = np.meshgrid(X, Y)
  # # 背景関数
  # Z = rastrigin(X, Y, A=10)
  # # ヒートマップの生成
  # ax.imshow(Z, cmap=cm.jet, extent =[-5.12, 5.12, -5.12, 5.12])
  # # 解集団のプロット
  # ax.scatter(data[:,0]/100, data[:,1]/100, c = 'm', alpha = 0.5) # １列目のデータをx軸の値、2列目のデータをy軸の値として与える。  
  # ax.axis([-5.12, 5.12, -5.12, 5.12])

  # ヒートマップ用の値（配列）schwefel
  X = np.arange(-512, 512, 1)
  Y = np.arange(512, -512, -1)
  X,Y = np.meshgrid(X, Y)
  # 背景関数
  Z = schwefel(X, Y, A=418.9829)
  # ヒートマップの生成
  ax.imshow(Z, cmap=cm.jet, extent =[-512, 512, -512, 512])
  # 解集団のプロット
  ax.scatter(data1[:,0], data1[:,1], c = 'm', alpha = 0.5) # 0~50列目のデータをx軸の値、2列目のデータをy軸の値として与える。
  ax.scatter(data2[:,0], data2[:,1], c = 'w', alpha = 0.5) # 50行目以降
  ax.axis([-512, 512, -512, 512])
  

  fig.savefig("../../figure/" + fig_name + ".png")
  # plt.show() # グラフの描画
  plt.close()
  sys.stdout.write("\r" + fig_name + ".png : 出力完了!")
  


if __name__ == '__main__':
    os.chdir("./results/position/0/")
    files = glob.glob("*.csv")
    for file in files: 
        # print (file)
    	main(file)