import numpy as np
import math
from config import Config as cf
import function as fn

class Individual:
    def __init__(self):
        self.init(0)

    def init(self, iteration):
        self.__position = np.random.rand(cf.get_dimension()) * (cf.get_max_domain() - cf.get_min_domain())  + cf.get_min_domain()
        self.__fitness = fn.calculation(self.__position,0) # iteration = 0
        self.__intensity = 1 / (1 + self.__fitness) # for minimize problem
        self.__strategy = "null"

    def get_fitness(self):
        return self.__fitness

    def set_fitness(self,fitness):
        self.__fitness = fitness

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    # def get_strategy(self):
    #     return self.__strategy
    
    # def set_strategy(self, strategy):
    #     self.__strategy = strategy

    def rand_1(self,selfIndex,de_list):
        """select three points (a, b, c)"""
        a = np.random.randint(0, len(de_list))
        while (a == selfIndex):
            a = np.random.randint(0, len(de_list))
        b = np.random.randint(0, len(de_list))
        while (b == selfIndex or a == b):
            b = np.random.randint(0, len(de_list))
        c = np.random.randint(0, len(de_list))
        while (c == selfIndex or c == a or c == b):
            c = np.random.randint(0, len(de_list)) 

        """Select Random Index (R)"""
        R = np.random.randint(0,cf.get_dimension())

        # 次元数毎に更新を行う
        for i in range(len(self.__position)):
            rnd = np.random.rand()
            if (rnd < cf.get_CR() or i == R):
                """update equation"""
                self.__position[i] = de_list[a].get_position()[i] + cf.get_F() * (de_list[b].get_position()[i] - de_list[c].get_position()[i])
                if (self.__position[i] > cf.get_max_domain()):
                    self.__position[i] = cf.get_max_domain()
                if (self.__position[i] < cf.get_min_domain()):
                    self.__position[i] = cf.get_min_domain()
    
    def global_1(self,selfIndex,de_list):
        """select three points (a, b, c)"""
        a = 0
        while (a == selfIndex):
            a = np.random.randint(0, len(de_list))
        b = np.random.randint(0, len(de_list))
        while (b == selfIndex or a == b):
            b = np.random.randint(0, len(de_list))
        c = np.random.randint(0, len(de_list))
        while (c == selfIndex or c == a or c == b):
            c = np.random.randint(0, len(de_list)) 

        """Select Random Index (R)"""
        R = np.random.randint(0,cf.get_dimension())

        # 次元数毎に更新を行う
        for i in range(len(self.__position)):
            rnd = np.random.rand()
            if (rnd < cf.get_CR() or i == R):
                """update equation"""
                self.__position[i] = de_list[a].get_position()[i] + cf.get_F() * (de_list[b].get_position()[i] - de_list[c].get_position()[i])
                if (self.__position[i] > cf.get_max_domain()):
                    self.__position[i] = cf.get_max_domain()
                if (self.__position[i] < cf.get_min_domain()):
                    self.__position[i] = cf.get_min_domain()
    
    def local_neighborhood(self, selfIndex, de_list):
        # m 近傍個体分のリストを作る
        distance_dic = {} 
        self_position = self.get_position()
        for i in range(len(de_list)):
            if selfIndex == i:
                continue
            current_distance = 0
            current_position = de_list[i].get_position()
            for dim in range(cf.get_dimension()):
                current_distance = current_distance + np.sqrt((self_position[dim] - current_position[dim])**2)
            # 辞書登録
            distance_dic[de_list[i]] = current_distance
        # sort distance_list
        distance_dic = sorted(distance_dic, key=lambda ID:distance_dic.values())
        
        # apply to close_list
        close_list = []
        for close_ind in distance_dic.keys():
            close_list.append(close_ind)

        self.rand_1(selfIndex,close_list)

    def print_info(self,i):
        print("id:","{0:3d}".format(i),
              "|| fitness:",str(self.__fitness).rjust(14," "),
              "|| position:",np.round(self.__position,decimals=4))


if __name__ == '__main__':
    pass