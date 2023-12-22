import os, sys
import numpy as np

file_path = '/storage/home/yuj179/mygroup/drug_design/virtual_drug/9VD/DDLB/CSP/'
num_trajs = 100
start_ncl = 190

# copy output
os.system('mkdir output')
for i in range(num_trajs):
    f = open(file_path+'/output/%d.out'%(i+1))
    lines = f.readlines()
    f.close()
    
    f = open('./output/%d.out'%(i+1), 'w')
    for line in lines:
        if line.startswith('--> Elongation at length %d with random seed'%start_ncl):
            break
        else:
            f.write(line)
    f.close()
    
# copy trajectory
os.system('mkdir traj')
for i in range(num_trajs):
    os.system('mkdir traj/%d/'%(i+1))
    os.system('cp %s/traj/%d/rnc_l%d_stage_3_final.cor ./traj/%d/'%(file_path, i+1, start_ncl-1, i+1))

#os.system('cp %s/traj/1/rnc_l%d.psf ./'%(file_path, start_ncl-1))

# copy setup
#os.system('cp -r %s/setup/ ./'%file_path)
