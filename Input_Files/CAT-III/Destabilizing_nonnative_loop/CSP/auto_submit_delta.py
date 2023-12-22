import os, sys, time
import numpy as np

num_traj = 100
start_traj_id = 1
num_job = 100
total_nascent_chain_length = 9999
tmp_cntrl_file = 'setup/cont_synth_tmp.cntrl'

num_traj_per_job = int((num_traj-start_traj_id+1)/num_job)
num_traj_last_job = (num_traj-start_traj_id+1) - num_traj_per_job * (num_job-1)

for i in range(num_job):
    f = open(tmp_cntrl_file)
    lines = f.readlines()
    f.close()
    
    start_id = start_traj_id + i * num_traj_per_job
    if i != num_job - 1:
        end_id = start_id + num_traj_per_job -1
        num_traj_this_job = num_traj_per_job
    else:
        end_id = start_id + num_traj_last_job - 1
        num_traj_this_job = num_traj_last_job
    f = open('CSP_%d-%d.cntrl'%(start_id, end_id), 'w')
    find_gpu_tag = False
    find_start_id_tag = False
    find_restart_tag = False
    for line in lines:
        if line.startswith('use_gpu = '):
            f.write('use_gpu = 1\n')
            find_gpu_tag = True
        elif line.startswith('tpn = '):
            f.write('tpn = 1\n')
        elif line.startswith('ppn = '):
            f.write('ppn = 1\n')
        elif line.startswith('num_traj = '):
            f.write('num_traj = %d\n'%num_traj_this_job)
        elif line.startswith('start_traj_id = '):
            f.write('start_traj_id = %d\n'%start_id)
            find_start_id_tag = True
        elif line.startswith('total_nascent_chain_length = '):
            f.write('total_nascent_chain_length = %d\n'%total_nascent_chain_length)
        elif line.startswith('restart = '):
            f.write('restart = 1\n')
            find_restart_tag = True
        elif line.startswith('log_file = '):
            f.write('log_file = info_%d-%d.log\n'%(start_id, end_id))
        else:
            f.write(line)
    if not find_gpu_tag:
        f.write('use_gpu = 1\n')
    if not find_start_id_tag:
        f.write('start_traj_id = %d\n'%start_id)
    if not find_restart_tag:
        f.write('restart = 1\n')
    f.close()
    
    f = open('job_%d.slurm'%(i+1), 'w')
    f.write('''#!/bin/bash
#SBATCH -J C_1_'''+str(start_id)+'''_'''+str(end_id)+'''
#SBATCH -p gpuA40x4
#SBATCH --mail-type=NONE
#SBATCH -o %j.o # Name of stdout output file
#SBATCH -e %j.e # Name of stderr error file
#SBATCH -N 1
#SBATCH -n 2
#SBATCH --gpus=1
#SBATCH --mem=64GB
#SBATCH -t 48:00:00
#SBATCH -A bbjq-delta-gpu

cd $SLURM_SUBMIT_DIR

continuous_synthesis_v7.py -f CSP_'''+str(start_id)+'''-'''+str(end_id)+'''.cntrl
''')
    f.close()
    
    os.system('sbatch job_%d.slurm'%(i+1))
    time.sleep(1)
