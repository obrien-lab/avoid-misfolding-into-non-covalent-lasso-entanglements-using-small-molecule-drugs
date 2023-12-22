#!/usr/bin/env python3
import os, sys, time, traceback, multiprocessing
import parmed as pmd
import mdtraj as mdt
import numpy as np

############################################
def analysis(i):
    global sel_ligand_res, traj_dir, psffile, native_cor_file, dom_def_file, sec_struct_file
    print('Analyzing traj #%d'%(i+1))
    traj = mdt.load(traj_dir+'/%d.dcd'%(i+1), top=psffile)
    traj.atom_slice(sel_protein_atm).save('tmp_%d.dcd'%(i+1), force_overwrite=True)
    # Calculate Q
    os.system('calc_native_contact_fraction_v2.pl -i '+native_cor_file+' -d '+dom_def_file+' -s '+sec_struct_file+' -t tmp_%d.dcd -o ./Q/'%(i+1))
    os.system('mv ./Q/qbb_tmp_%d.dat ./Q/qbb_%d.dat'%(i+1, i+1))
    
    # Calculate G
    os.system('calc_entanglement_number.pl -i '+native_cor_file+' -t tmp_%d.dcd -o ./G/'%(i+1))
    os.system('mv ./G/G_tmp_%d.dat ./G/G_%d.dat'%(i+1, i+1))
    
    os.system('rm -f tmp_%d.dcd'%(i+1))
    
    # Calculate Num of binding
    f = open('./N_bind/Nb_%d.dat'%(i+1), 'w')
    f.close()
    for fi in range(traj.n_frames):
        nc = 0
        for s1 in sel_ligand_res:
            tag = False
            for a1 in struct.residues[s1].atoms:
                for s2 in sel_protein_atm:
                    d = np.sum((traj.xyz[fi,a1.idx,:]-traj.xyz[fi,s2,:])**2)**0.5
                    if d <= dist_cutoff:
                        print(a1, s2, d)
                        nc += 1
                        tag = True
                        break
                if tag:
                    break
        f = open('./N_bind/Nb_%d.dat'%(i+1), 'a')
        f.write('%10d\n'%nc)
        f.close()

############################################

dist_cutoff = 0.8 # nm
psffile = sys.argv[1]
traj_dir = sys.argv[2]
sec_struct_file = sys.argv[3]
dom_def_file = sys.argv[4]
native_cor_file = sys.argv[5]
num_traj = int(sys.argv[6])
start_id = int(sys.argv[7])
nproc = int(sys.argv[8])

os.system('mkdir Q')
os.system('mkdir G')
os.system('mkdir N_bind')

struct = pmd.load_file(psffile)
sel_protein_atm = []
sel_ligand_res = []
for atm in struct.atoms:
    if atm.residue.segid == 'A':
        sel_protein_atm.append(atm.idx)
for res in struct.residues:
    if res.segid == 'LIG':
        sel_ligand_res.append(res.idx)

pool = multiprocessing.Pool(nproc)
for i in range(start_id-1, num_traj):
    pool.apply_async(analysis, (i,))

while True:
    time.sleep(10)
    if len(pool._cache) == 0:
        print('All Done.')
        break

pool.close()
pool.join()
