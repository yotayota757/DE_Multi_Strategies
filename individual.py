import numpy as np
import math
from config import Config as cf
import function as fn

class Individual:
    def __init__(self):
        self.__position = np.random.rand(cf.get_dimension()) * (cf.get_max_domain() - cf.get_min_domain())  + cf.get_min_domain()
        self.__fitness = fn.calculation(self.__position,0) # iteration = 0
        self.__intensity = 1 / (1 + self.__fitness) # for minimize problem

    def get_fitness(self):
        return self.__fitness

    def set_fitness(self,fitness):
        self.__fitness = fitness

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def generate(self, a, b, c, R):
        for i in range(len(self.__position)):
            rnd = np.random.rand()
            if (rnd < cf.get_CR() or i == R):
                """update equation"""
                self.__position[i] = a.get_position()[i] + cf.get_F() * (b.get_position()[i] - c.get_position()[i])
                if (self.__position[i] > cf.get_max_domain()):
                    self.__position[i] = cf.get_max_domain()
                if (self.__position[i] < cf.get_min_domain()):
                    self.__position[i] = cf.get_min_domain()


    def print_info(self,i):
        print("id:","{0:3d}".format(i),
              "|| fitness:",str(self.__fitness).rjust(14," "),
              "|| position:",np.round(self.__position,decimals=4))


if __name__ == '__main__':
    pass