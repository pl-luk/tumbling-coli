import matplotlib.pyplot as plt
import os
import shutil
from main import *

'''
Calculate (mean) square displacement with simulation output positions.npy
'''

def delta_r2(positions):
    return np.sum(np.power(positions,2), axis=2)

'''
Calculate slope with (mean) square displacement and the timepoints of these datapoints, which can be calculated with:
timeline = np.append([0]*len(times[0,:]), np.cumsum(times[:-1,:], axis=0).flatten())
from simulation output times.npy
'''

def LeastSquares(mean_delta_r, timeline):
    n = len(mean_delta_r)
    x = timeline
    y = mean_delta_r
    x_bar = np.sum(x)/n
    y_bar = np.sum(y)/n
    
    a = (np.sum(x*y) - n * x_bar * y_bar)/(np.sum(x*x) - n * x_bar * x_bar)
    b = (y_bar * np.sum(x*x) - x_bar * np.sum(x*y))/(np.sum(x*x) - n * x_bar * x_bar)
    
    return a, b

'''
Calculate standatd deviation for different bacteria numbers form the diffusion 
coefficient form N simulations:
'''

def std(N):
    D_std = np.zeros([3,7])
    N_bac = [10, 50, 100, 250, 500, 1000, 2000]
    D_std[0,:] = N_bac
    
    for i in range(7):
        D = np.zeros([N])
        for j in range(N):
            print(N_bac[i], j+1)
            sim(N_bac[i], 60*60, 10)
            pos=np.load('./data/positions.npy')
            times=np.load('./data/times.npy')
            dt=np.append([0]*len(times[0,:]), np.cumsum(times[:-1,:], axis=0).flatten())
            dr2=delta_r2(pos).flatten()
            D[j] = LeastSquares(dr2[600:], dt[600:])[0]/4
            shutil.rmtree('./data')
        D_std[1,i] = np.mean(D)
        D_std[2,i] = np.std(D)
        
    return D_std

'''
Calculate the diffusion coefficient depending on the mean angle for N bacteria, 
with N_angle points between 0 and 360 degrees and the angle_variance
'''

def Var_mean_angle(N, N_angle, angle_variance = 1):
    
    D = np.zeros([2,N_angle])
    D[0,:] = np.linspace(0, 360, N_angle)
    
    for i in range(N_angle):
        print(i+1)
        sim(N, 60*60, 10, alpha = D[0,i] / 180 * np.pi, angle_variance = 1)
        pos=np.load('./data/positions.npy')
        times=np.load('./data/times.npy')
        dt=np.append([0]*len(times[0,:]), np.cumsum(times[:-1,:], axis=0).flatten())
        dr2=delta_r2(pos).flatten()
        D[1,i] = LeastSquares(dr2[600:], dt[600:])[0]/4
        shutil.rmtree('./data')
    
    return D

'''
Calculate the diffusion coefficient depending on the mean runtime for N bacteria, 
with N_r points between rt_min and rt_max in seconds
'''

def Var_mean_rt(N, rt_min, rt_max, N_rt):
    
    D = np.zeros([2,N_rt])
    D[0,:] = np.linspace(rt_min, rt_max, N_rt)
    
    for i in range(N_rt):
        print(i+1)
        sim(N, 60*60, 10, tau = D[0,i])
        pos=np.load('./data/positions.npy')
        times=np.load('./data/times.npy')
        dt=np.append([0]*len(times[0,:]), np.cumsum(times[:-1,:], axis=0).flatten())
        dr2=delta_r2(pos).flatten()
        D[1,i] = LeastSquares(dr2[600:], dt[600:])[0]/4
        shutil.rmtree('./data')
    
    return D

'''
Calculate the position for a single bacteria at time t by linear interpolation
with pos as the positions of one bacteria at the timeline dt
'''

def pos_fixed_t_single(pos, dt, t):
    for j in range(1, len(dt)):
        if ( t >= dt[j-1]) and (t <= dt[j]):
            pos_f = pos[j-1,:] + (pos[j,:]-pos[j-1,:]) * (t-dt[j-1])/(dt[j]-dt[j-1]) 
    return pos_f

'''
Calculate the position at N_t timepoints between 0s and 1h for multiple bacteria
with pos as positions.npy and dt as the timeline (see LeastSquares function)
'''


def pos_fixed_t(pos, dt, N_t):
    N=len(pos[0,:,0])
    t = np.linspace(0,60*60-1, N_t)
    dt_rs=np.reshape(dt, [-1,N])
    pos_fixed = np.zeros([N_t, N, 2])
    for i in range(N_t):
        for j in range(N):
            pos_fixed[i,j,:] = pos_fixed_t_single(pos[:,j,:], dt_rs[:,j], t[i])
    return t, pos_fixed
    


