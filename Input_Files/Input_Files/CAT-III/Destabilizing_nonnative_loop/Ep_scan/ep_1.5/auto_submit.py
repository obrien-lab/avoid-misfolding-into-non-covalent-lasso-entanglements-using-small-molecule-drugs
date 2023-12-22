import sys, os, random
import numpy as np

num_rep = 10
start_id = 1
psffile = '../setup/protein_9VD_1.psf'
corfile = '../setup/protein_9VD_1.cor'
prmfile = './3cla_9VD.xml'
vecfile = '../setup/prot_l213_dissociation_final.vel'
temp = 310

for i in range(start_id-1, num_rep):
    rand = int(random.random()*1e7)
    f = open('job_%d.pbs'%(i+1), 'w')
    f.write('''#PBS -N d1_1.5_'''+str(i+1)+'''
#PBS -r n
#PBS -o $PBS_JOBID.out
#PBS -e $PBS_JOBID.err
#PBS -l nodes=1:ppn=2:gpus=1:shared:gc_t4
#PBS -l qos=mgc_nih
#PBS -l walltime=2:00:00:00
#PBS -A mgc_nih

cd $PBS_O_WORKDIR

python ../setup/run_MD.py '''+psffile+''' '''+corfile+''' '''+prmfile+''' '''+vecfile+''' '''+str(temp)+''' '''+str(i+1)+''' '''+str(rand)+''' > '''+str(i+1)+'''.out
''')
    f.close()
    
    os.system('qsub job_%d.pbs'%(i+1))
