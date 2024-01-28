import matplotlib.pyplot as plt
from bacteria import *

"""
Simulation of N bacteria until maximum time Tmax, with datapoints in time-interval dt
Output: array of N bacteria-classes, time-datapoints in self.data_time and position-datapoints in self.data_pos
"""

def sim(dt, Tmax, N, mean_angle = 70, mean_runtime = 1):
    
    bac_array = []

    for i in range(N):
        
        bac_array.append(bacteria(mean_angle, mean_runtime))
        
        while bac_array[i].data_time[-1] <= Tmax:
            bac_array[i].step(dt, Tmax)
            
    return bac_array

"""
Calculation of the mean squared displacement of an array with bacteria-classes
"""

def mean_delta_r(bac_array):
    
    N=len(bac_array)
    l=len(bac_array[0].data_time)
    
    dr = np.zeros([N,l])
    for i in range(N):
        dr[i,:] = np.sum(np.power(bac_array[i].data_pos, 2), axis = 0)
        
    return np.mean(dr, axis = 0)


"""
linear fit to calculate a and b
"""

def LeastSquares(mean_delta_r, timeline):
    n = len(mean_delta_r)
    x = timeline
    y = mean_delta_r
    x_bar = np.sum(x)/n
    y_bar = np.sum(y)/n
    
    a = (np.sum(x*y) - n * x_bar * y_bar)/(np.sum(x*x) - n * x_bar * x_bar)
    b = (y_bar * np.sum(x*x) - x_bar * np.sum(x*y))/(np.sum(x*x) - n * x_bar * x_bar)
    
    return a, b

"""
Calculation of the diffusion-coefficient depending on the mean angle with N_angle points between 0 and 360 degrees
"""

def Var_mean_angle(dt, Tmax, N, N_angle):
    
    D = np.zeros([2,N_angle])
    D[0,:] = np.linspace(0, 360, N_angle)
    
    for i in range(N_angle):
        
        bac = sim(dt, Tmax, N, mean_angle = D[0,i])
        D[1,i] = LeastSquares(mean_delta_r(bac), bac[0].data_time)[0]/4
        print(i+1)
    
    return D

"""
Calculation of the diffusion-coefficient depending on the mean runtime (rt) with N_rt points between rt_min and rt_max
"""

def Var_mean_runtime(dt, Tmax, N, rt_min, rt_max, N_rt):
    
    D = np.zeros([2,N_rt])
    D[0,:] = np.linspace(rt_min, rt_max, N_rt)
    
    for i in range(N_rt):
        
        bac = sim(dt, Tmax, N, mean_runtime = D[0,i])
        D[1,i] = LeastSquares(mean_delta_r(bac), bac[0].data_time)[0]/4
        print(i+1)
    
    return D

