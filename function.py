import numpy as np

"""
[Reference]
https://www.sfu.ca/~ssurjano/index.html
"""

"""Parameters"""
# for ackley
a = 20
b = 0.2
c = np.pi


# def calculation(array, t):#as you want
#     fitness = singlemoving(array,t)
#     return fitness

def calculation(array, t):#as you want
    fitness = 0
    if(t < 3000):
        fitness = rastrigin(array)
    if(t >= 3000):
        fitness = schwefel(array)
    # fitness = schwefel(array)
    return fitness


def singlemoving(array,t): #単峰性の動的環境
    # (0, 0)中心で半径125の半径の円
    a = ((array[0] - 125 * np.sin(0.01*t))**2 / (2 * 40**2))
    b = ((array[1] + 125 * np.cos(0.01*t))**2 / (2 * 40**2))
    fitness = 1 - np.exp(-a - b)
    return fitness

"""Benchmark Functions"""
def ackley(array):
    sum1 = 0
    sum2 = 0

    for i in range (len(array)):
        sum1 = sum1 + array[i]**2

    for i in range (len(array)):
        sum2 = sum2 + np.cos(c*array[i])

    fitness = - a * np.exp(-b * np.sqrt((1/d) * sum1)) - np.exp((1/d) * sum2) + a + np.exp(1)

    return fitness

def rosenbrock(array):
    sum1 = 0

    for i in range(len(array) - 1):
        sum1 = sum1 + (100 * (array[i+1] - array[i])**2 + (array[i] - 1)**2)

    fitness = sum1
    return fitness

def sphere(array):
    fitness = 0
    for i in range(len(array)):
        fitness = fitness + array[i]**2
    return fitness

def rastrigin(array):
    sum = 0
    fitness = 0
    for x in array:
        sum = sum + x**2 - 10 * np.cos(2 * np.pi * x)
    fitness = 10.0 * len(array) + sum
    return fitness

def rastrigin_stded(array):
    sum = 0
    fitness = 0
    for x in array:
        X = (x / 500.0) * 5.12
        sum = sum + X**2 - 10 * np.cos(2 * np.pi * X)
    fitness = 10.0 * len(array) + sum
    return fitness

def schwefel(array):
    sum = 0
    fitness = 0
    for x in array:
        sum = sum + x * np.sin(np.sqrt(np.abs(x)))
    fitness = 418.9829 * len(array) - sum
    return fitness

def michalewicz(array):#for the number of Dimension is 2
    sum = 0
    fitness = 0
    m = 10
    for (i,x) in enumerate(array, start=1):
        sum = sum + np.sin(x) * np.sin((i * (x**2) )/np.pi)**(2*m)
    fitness = -sum
    return fitness

if __name__ == '__main__':
    a = np.array([2.20,1.0])
    print (michalewicz(a))
