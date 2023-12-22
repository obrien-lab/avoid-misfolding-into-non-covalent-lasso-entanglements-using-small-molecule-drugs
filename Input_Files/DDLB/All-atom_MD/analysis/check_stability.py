import os, sys
import numpy as np

traj_id_list = [1,2,3,4,5,6,7,8,9,10]
cutoff = 0.5

total_ratio = 0
for traj_id in traj_id_list:
    with open('../%d/LIG_contacts.dat'%traj_id) as f:
        lines = f.readlines()
    data = np.array([[float(w) for w in line.strip().split()] for line in lines[1:]])
    
    num_unbound = 0
    for i in range(0,len(data)):
        ratio = data[i,2]
        if np.isnan(ratio):
            num_unbound += 1
        elif ratio < cutoff:
            num_unbound += 1
    unbound_ratio = num_unbound / len(data)
    total_ratio += unbound_ratio
    print('Traj %d off-target ratio = %.4f'%(traj_id, unbound_ratio))
    
    fc = 0
    #for i in range(9900,len(data)):
    for i in range(5000,len(data)):
        ratio = data[i,2]
        if np.isnan(ratio):
            fc += 0
        else:
            fc += ratio
    #fc = fc / (len(data)-9900)
    fc = fc / (len(data)-5000)
    #print('Traj %d average fc in last 10 ns = %.4f'%(traj_id, fc))
    print('Traj %d average fc in last 500 ns = %.4f'%(traj_id, fc))
total_ratio /= len(traj_id_list)
print('Total off-target ratio = %.4f'%(total_ratio))


