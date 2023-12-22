import sys, os, random
import numpy as np

num_traj = 10
start_traj_id = 1
num_job = 10
tmp_cntrl_file = '../setup/CSP_tmp.cntrl'

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
        elif line.startswith('restart = '):
            f.write('restart = 0\n')
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
        f.write('restart = 0\n')
    f.close()
    
    f = open('job_%d.pbs'%(i+1), 'w')
    f.write('''#PBS -N d1_0.5_'''+str(i+1)+'''
#PBS -r n
#PBS -o $PBS_JOBID.out
#PBS -e $PBS_JOBID.err
#PBS -l nodes=1:ppn=2:gpus=1:shared:gc_t4
#PBS -l qos=mgc_nih
#PBS -l walltime=2:00:00:00
#PBS -A mgc_nih

cd $PBS_O_WORKDIR

continuous_synthesis_v7.py -f CSP_'''+str(start_id)+'''-'''+str(end_id)+'''.cntrl
''')
    f.close()
    
    os.system('qsub job_%d.pbs'%(i+1))
