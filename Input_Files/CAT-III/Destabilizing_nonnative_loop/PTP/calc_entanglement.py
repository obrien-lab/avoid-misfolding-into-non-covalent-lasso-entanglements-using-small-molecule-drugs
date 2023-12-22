#!/usr/bin/env python3

import getopt, os, time, multiprocessing, random, math, traceback, io, sys
import numpy

def analysis(traj, cor_file, out_dir):
	os.system('calc_entanglement_number.pl -i %s -t %s -o %s -r 1'%(cor_file, traj, out_dir))

np = int(sys.argv[1])
start_traj_idx = int(sys.argv[2])
end_traj_idx = int(sys.argv[3])
start_rep_idx = int(sys.argv[4])
end_rep_idx = int(sys.argv[5])

psf_file = os.popen('ls setup/*.psf').readlines()[0].strip()
cor_file = os.popen('ls setup/*.cor').readlines()[0].strip()

#traj_list = os.popen('ls | grep "^[0-9]\\+$"').readlines()
#traj_list = [t.strip() for t in traj_list]
traj_list = numpy.arange(start_traj_idx, end_traj_idx+1)

os.system("mkdir -p analysis/entanglement")

pool = multiprocessing.Pool(np)
for traj_dir in traj_list:
    traj_dir = str(traj_dir)
    for idx in range(start_rep_idx-1, end_rep_idx):
        pool.apply_async(analysis, (traj_dir+'/traj_'+traj_dir+'_'+str(idx+1)+'.dcd', cor_file, 'analysis/entanglement/'))

while True:
    time.sleep(10)
    if len(pool._cache) == 0:
        print('All Done.')
        break

pool.close()
pool.join()
