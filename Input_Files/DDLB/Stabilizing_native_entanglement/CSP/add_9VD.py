import os
import parmed as pmd
import numpy as np

num_traj = 100
num_9VD = 1
start_ncl = 190

a=pmd.load_file('setup/50S_tRNA_cg_truncated.psf')
    
b = pmd.load_file('setup/9VD.psf')

c=a
for i in range(num_9VD):
    c=c+b
c.save('setup/50S_tRNA_cg_truncated_9VD.psf', overwrite=True)

f = open('packmol.in', 'w')
f.write('''#
# 9VD in a sphere with radius 100 A
#

tolerance 2.0
seed -1
add_amber_ter

structure tmp.pdb
  number 1
  fixed 0. 0. 0. 0. 0. 0.
  radius 4.0
end structure

structure setup/9VD.pdb
  number '''+str(num_9VD)+''' 
  inside sphere 160. 0. 0. 100.
  radius 4.0
end structure

output tmp_9VD.pdb
''')
f.close()

for i in range(0, num_traj):
#for i in [11,30,42,79,87,91]:
    path = './traj/%d/'%(i+1)
    d = pmd.load_file('./rnc_l%d.psf'%(start_ncl-1))
    e = pmd.load_file(path+'rnc_l%d_stage_3_final.cor'%(start_ncl-1))
    
    non_lig_idx = []
    for idx, se in enumerate(e.segid):
        if se != 'LIG':
            non_lig_idx.append(idx)
            
    d.coordinates = e.coordinates[0][non_lig_idx]
    d.save('tmp.pdb', overwrite=True)
    
    os.system('packmol < packmol.in')
    
    for j in range(num_9VD):
        d=d+b
    d.coordinates = pmd.load_file('tmp_9VD.pdb').coordinates
    d.save(path+'rnc_l%d_stage_3_final.cor'%(start_ncl-1), format='charmmcrd', overwrite=True)
    
    os.system('rm -f tmp.pdb')
    os.system('rm -f tmp_9VD.pdb')
