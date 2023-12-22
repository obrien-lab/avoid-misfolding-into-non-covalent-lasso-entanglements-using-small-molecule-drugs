import os 
import numpy as np

num_traj = 100
co_dir = '/storage/home/yuj179/mygroup/drug_design/virtual_drug/9VD/DDLB/CSP'
prefix = 'prot_l306'

for i in range(num_traj):
    os.system('mkdir %d'%(i+1))
    os.system('cp '+co_dir+'/traj/'+str(i+1)+'/'+prefix+'.psf ./'+str(i+1))
    os.system('cp '+co_dir+'/traj/'+str(i+1)+'/'+prefix+'_dissociation_final.ncrst ./'+str(i+1))
