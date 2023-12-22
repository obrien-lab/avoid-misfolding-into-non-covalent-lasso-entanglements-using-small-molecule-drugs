import os, sys
import numpy as np
import mdtraj as mdt
import parmed as pmd

def analysis(pmd_struct):
    struct = pmd_struct['!@H=']
    lig = struct[':LIG']
    prot = struct['!:LIG']
    interaction_res_list = []
    for prot_res in prot.residues:
        tag = False
        for prot_atm in prot_res.atoms:
            prot_coor = np.array([prot_atm.xx, prot_atm.xy, prot_atm.xz])
            for lig_res in lig.residues:
                for lig_atm in lig_res.atoms:
                    lig_coor = np.array([lig_atm.xx, lig_atm.xy, lig_atm.xz])
                    dist = np.sum((prot_coor - lig_coor)**2)**0.5
                    if dist < dist_cutoff:
                        tag = True
                        break
                if tag:
                    break
            if tag:
                break
        if tag:
            interaction_res_list.append(prot_res.number)
    counts = [0 for section in N_ter_sections]
    for idx in interaction_res_list:
        for i, section in enumerate(N_ter_sections):
            if idx in section:
                counts[i] += 1
                break
    on_target = 0
    frac = np.sum(counts)/len(interaction_res_list)
    if (0 not in counts[0:3:2]) and frac >= frac_cutoff:
        on_target = 1
    return (np.sum(counts), frac, on_target)

dist_cutoff = 4 # Angstrom
frac_cutoff = 0.8
N_ter_sections = [np.arange(1,13), np.arange(13,25), np.arange(25,36)]
dt = 0.1 # ns

pmd_struct = pmd.load_file('complex.psf')
# Load inital structure
traj_0 = mdt.load('phase_1/complex.pdb')
pmd_struct.coordinates = traj_0.xyz[0]*10
[num_counts, frac, on_target] = analysis(pmd_struct)
with open('LIG_contacts.dat', 'w') as f:
    f.write('%10s %6s %6s %6s\n'%('Time (ns)', 'nCnts', 'fb', 'onTar'))
    f.write('%10.1f %6d %6.4f %6d\n'%(0, num_counts, frac, on_target))
# Analyze trajectory
traj = mdt.load('prod_image.dcd',top='complex.psf')
for i in range(traj.n_frames):
    pmd_struct.coordinates = traj[i].xyz*10
    [num_counts, frac, on_target] = analysis(pmd_struct)
    with open('LIG_contacts.dat', 'a') as f:
        f.write('%10.1f %6d %6.4f %6d\n'%((i+1)*dt, num_counts, frac, on_target))






