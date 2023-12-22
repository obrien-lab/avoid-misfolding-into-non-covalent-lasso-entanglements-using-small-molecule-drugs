import numpy as np
import os, sys, random

walltime = '2:00:00:00'
n_rep = 10
n_traj = 100
sim_time = 10 # s
submit_start_id = int(sys.argv[1])
submit_num = int(sys.argv[2])

psffile = 'prot_l306.psf'
ncrstfile = 'prot_l306_dissociation_final.ncrst'
alpha = 4331293
timestep = 0.015
sim_steps = int(np.ceil(sim_time*1e9/alpha*1e3 / timestep / 5000) * 5000)

for ei in range(submit_start_id, submit_start_id+submit_num):
    idx_traj = int(ei/n_rep)+1
    idx_rep = int(ei-(idx_traj-1)*n_rep)+1
    outfile = '%d/traj_%d_%d.out'%(idx_traj, idx_traj, idx_rep)
    tag_finish = False
    if os.path.exists(outfile):
        f = open(outfile)
        lines = f.readlines()
        f.close()
        last_line = lines[-1].strip()
        if last_line.startswith('Done'):
            tag_finish = True
        elif not last_line.startswith('Time') and os.path.getsize(outfile) != 0:
            end_step = int(last_line.split()[0])
            if end_step >= sim_steps:
                tag_finish = True
        
    if not tag_finish:
        os.chdir('%d/'%(idx_traj))
        
        rand = int(random.random()*1e7)
        
        f = open('job_%d.pbs'%(idx_rep), 'w')
        f.write('''#!/bin/bash
#PBS -N P1_'''+str(idx_traj)+'''_'''+str(idx_rep)+'''
#PBS -r n
#PBS -o $PBS_JOBID.out
#PBS -e $PBS_JOBID.err
#PBS -l nodes=1:ppn=2:gpus=1:shared:gc_t4
#PBS -l qos=mgc_nih
#PBS -l walltime=5:00:00:00
#PBS -A mgc_nih

cd $PBS_O_WORKDIR

python ../setup/run_MD.py '''+psffile+''' '''+ncrstfile+''' ../setup/4c5c_9VD.xml 310 traj_'''+str(idx_traj)+'''_'''+str(idx_rep)+''' '''+str(rand)+''' '''+str(sim_time)+'''
''')
        f.close()
        
        os.system('qsub job_%d.pbs'%(idx_rep))
        print('Submit %d %d'%(idx_traj, idx_rep))
        
        os.chdir('../')
    else:
        print('Skip %d %d finished job'%(idx_traj, idx_rep))
