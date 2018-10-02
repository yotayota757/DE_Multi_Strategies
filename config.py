import numpy as np
class Config:
    __PopulationSize1 = 50 # Population Size (default = 100)
    __PopulationSize2 = 50
    # __PopulationSize = 100
    __MaxDomain = 500 # variable upper limit
    __MinDomain = -500 # variable lower limit
    __Dimension = 2 # The number of dimension
    __F = 0.8 # differential weight
    __CR = 0.5 # crossover probability
    __Trial = 31
    __Iteration = 6000

    @classmethod
    def get_population_size_1(cls):
        return cls.__PopulationSize1

    @classmethod
    def get_population_size_2(cls):
        return cls.__PopulationSize2
    
    # @classmethod
    # def get_population_size(cls):
    #     return cls.__PopulationSize

    @classmethod
    def get_F(cls):
        return cls.__F

    @classmethod
    def get_CR(cls):
        return cls.__CR

    @classmethod
    def get_iteration(cls):
        return cls.__Iteration

    @classmethod
    def get_trial(cls):
        return cls.__Trial

    @classmethod
    def get_dimension(cls):
        return cls.__Dimension

    @classmethod
    def get_max_domain(cls):
        return cls.__MaxDomain

    @classmethod
    def set_max_domain(cls, _max_domain):
        cls.__MaxDomain = _max_domain

    @classmethod
    def get_min_domain(cls):
        return cls.__MinDomain

    @classmethod
    def set_min_domain(cls, _min_domain):
        cls.__MinDomain = _min_domain







