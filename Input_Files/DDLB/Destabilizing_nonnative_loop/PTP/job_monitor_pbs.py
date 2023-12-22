import numpy as np
import os, sys, time

start_id = 0
total_extend = 1000
njob_mgc_max = 30
job_prefix = 'P1_'

####################################

def get_njob(allocation_key, job_prefix):
    word = os.popen('qstat -u yuj179 | grep %s | grep %s | wc -l'%(allocation_key, job_prefix)).readline().strip()
    njob = int(word)
    word = os.popen('qstat -u yuj179 | grep %s | grep " C " | grep %s | wc -l'%(allocation_key, job_prefix)).readline().strip()
    njob -= int(word)
    word = os.popen('qstat -u yuj179 | grep batch | grep " Q " | grep %s | wc -l'%job_prefix).readline().strip()
    njob += int(word)
    return njob

####################################
localtime = '_'.join(time.asctime(time.localtime(time.time())).split())
f = open('Monitor_%s.log'%localtime, 'w')
f.write('Monitor starts at %s\n'%(time.asctime(time.localtime(time.time()))))
f.write('Start id: %d\n'%start_id)
f.close()
while start_id < total_extend:
    njob_mgc = get_njob('mgc', job_prefix)
    print(njob_mgc)
    n_submit = np.min([njob_mgc_max - njob_mgc, total_extend - start_id])
    if n_submit > 0:
        f = open('Monitor_%s.log'%localtime, 'a')
        f.write('Submit %d jobs to mgc at %s\n'%(n_submit, time.asctime(time.localtime(time.time()))))
        lines = os.popen('python extend_sim_pbs.py %d %d'%(start_id, n_submit)).readlines()
        for line in lines:
            f.write(line)
        start_id += n_submit
        f.write('Start id: %d\n'%start_id)
        f.close()
    
    time.sleep(2)
    

