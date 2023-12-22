#!/usr/bin/env python3
import sys, getopt, math, os, multiprocessing, time
import numpy as np
import mdtraj as mdt
import parmed as pmd

usage='Usage: python calc_cont_synth_N_vs_T.py <num_proc> <work_folder_list>'

eject_offset = 0
nproc = 20
if len(sys.argv) == 3:
    nproc = int(sys.argv[1])
    work_folder_list = sys.argv[2].strip().split()
elif len(sys.argv) == 2:
    nproc = int(sys.argv[1])
    work_folder_list = ['./']
else:
    print("Wrong number of argv")
    print(usage)
    sys.exit()

###### parse info.log ######
def parse_info():
    num_traj = None
    prot_prefix = None
    total_chain_length = None
    fo = open('info_1-1.log')
    for line in fo:
        line = line.strip()
        if line.startswith('Number of trajectories: '):
            words = line.split()
            num_traj = int(words[-1])
        elif line.startswith('Protein psf file: '):
            words = line.split()
            prot_prefix = words[-1].split('.psf')[0]
        elif line.startswith('Total nascent chain length: '):
            words = line.split()
            total_chain_length = int(words[-1])
        elif line.startswith('File save steps: '):
            words = line.split()
            nsave = int(words[-1])
        elif line.startswith('Time step: '):
            words = line.split()
            dt = float(words[-2])
        elif line.startswith('Scaling factor: '):
            words = line.split()
            alpha = float(words[-1])
    return (num_traj, prot_prefix, total_chain_length, nsave, dt, alpha)
###### END parse info.log ######

###### parse *.out ######
def parse_out(traj_dir, nsave, dt, alpha):
    TS = {}
    data_file = './output/'+traj_dir+'.out'
    traj_prefix = './traj/'+traj_dir+'/'
    init_t = 0
    tag_ter = 0
    fo = open(data_file, 'r')
    for line in fo:
        line = line.strip()
        if line.startswith('--> Elongation at length'):
            idx = int(line.split()[4]) - 1
            TS[idx] = [[],[],[]]
        elif line.startswith('Simulation steps for in silico dwell time before peptidyl transfer: '):
            step = int(line.split(': ')[1])
            if step < 0:
                step = 1
            if step < nsave:
                traj_name = [traj_prefix+'rnc_l'+str(idx+1)+'_stage_1_final.cor']
                ts = [step*dt/1000*alpha/1e9+init_t] # in s
            elif step%nsave == 0:
                traj_name = [traj_prefix+'rnc_l'+str(idx+1)+'_stage_1.dcd']
                ts = [5000*i*dt/1000*alpha/1e9+init_t for i in range(1, int(step/nsave)+1)]
            else:
                traj_name = [traj_prefix+'rnc_l'+str(idx+1)+'_stage_1.dcd', traj_prefix+'rnc_l'+str(idx+1)+'_stage_1_final.cor']
                ts = [5000*i*dt/1000*alpha/1e9+init_t for i in range(1, int(step/nsave)+1)]
                ts.append(step*dt/1000*alpha/1e9+init_t)
            if idx > 0:
                init_t += step * dt / 1000 * alpha / 1e9
                if idx-1 not in list(TS.keys()):
                    for i in range(idx):
                        TS[i] = [['',[],[]],['',[],[]],['',[],[]]]
                TS[idx-1][2] = [traj_name, ts, [0 for i in range(len(ts))]]
        elif line.startswith('Simulation steps for in silico dwell time before translocation: '):
            step = int(line.split(': ')[1])
            if step < 0:
                step = 1
            if step < nsave:
                traj_name = [traj_prefix+'rnc_l'+str(idx+1)+'_stage_2_final.cor']
                ts = [step*dt/1000*alpha/1e9+init_t] # in s
            elif step%nsave == 0:
                traj_name = [traj_prefix+'rnc_l'+str(idx+1)+'_stage_2.dcd']
                ts = [5000*i*dt/1000*alpha/1e9+init_t for i in range(1, int(step/nsave)+1)]
            else:
                traj_name = [traj_prefix+'rnc_l'+str(idx+1)+'_stage_2.dcd', traj_prefix+'rnc_l'+str(idx+1)+'_stage_2_final.cor']
                ts = [5000*i*dt/1000*alpha/1e9+init_t for i in range(1, int(step/nsave)+1)]
                ts.append(step*dt/1000*alpha/1e9+init_t)
            init_t += step * dt / 1000 * alpha / 1e9
            TS[idx][0] = [traj_name, ts, [0 for i in range(len(ts))]]
        elif line.startswith('Simulation steps for in silico dwell time before next tRNA binding: '):
            step = int(line.split(': ')[1])
            if step < 0:
                step = 1
            if step < nsave:
                traj_name = [traj_prefix+'rnc_l'+str(idx+1)+'_stage_3_final.cor']
                ts = [step*dt/1000*alpha/1e9+init_t] # in s
            elif step%nsave == 0:
                traj_name = [traj_prefix+'rnc_l'+str(idx+1)+'_stage_3.dcd']
                ts = [5000*i*dt/1000*alpha/1e9+init_t for i in range(1, int(step/nsave)+1)]
            else:
                traj_name = [traj_prefix+'rnc_l'+str(idx+1)+'_stage_3.dcd', traj_prefix+'rnc_l'+str(idx+1)+'_stage_3_final.cor']
                ts = [5000*i*dt/1000*alpha/1e9+init_t for i in range(1, int(step/nsave)+1)]
                ts.append(step*dt/1000*alpha/1e9+init_t)
            init_t += step * dt / 1000 * alpha / 1e9
            TS[idx][1] = [traj_name, ts, [0 for i in range(len(ts))]]
        elif line.startswith('--> Elongation termination'):
            idx += 1
            TS[idx] = [[],[]]
            tag_ter = 1
        elif line.startswith('Done at step ') and tag_ter == 1:
            step = int(line.split()[-1])
            if step < nsave:
                traj_name = traj_prefix+'rnc_l'+str(idx)+'_ejection_final.cor'
                ts = [step*dt/1000*alpha/1e9+init_t] # in s
            else:
                traj_name = traj_prefix+'rnc_l'+str(idx)+'_ejection.dcd'
                ts = [5000*i*dt/1000*alpha/1e9+init_t for i in range(1, int(step/nsave)+1)]
            init_t += step * dt / 1000 * alpha / 1e9
            tag_ter = 2
            TS[idx][0] = [traj_name, ts, [0 for i in range(len(ts))]]
        elif line.startswith('Done at step ') and tag_ter == 2:
            step = int(line.split()[-1])
            if step < nsave:
                traj_name = traj_prefix+'rnc_l'+str(idx)+'_dissociation_final.cor'
                ts = [step*dt/1000*alpha/1e9+init_t] # in s
            else:
                traj_name = traj_prefix+'rnc_l'+str(idx)+'_dissociation.dcd'
                ts = [5000*i*dt/1000*alpha/1e9+init_t for i in range(1, int(step/nsave)+1)]
            init_t += step * dt / 1000 * alpha / 1e9
            TS[idx][1] = [traj_name, ts, [0 for i in range(len(ts))]]
    return TS
###### END parse *.out ######

def Cal_N_ligand_bound(psf_file, traj_file):
    dist_cutoff = 0.8 # nm
    struct = pmd.load_file(psf_file)
    sel_protein_atm = []
    sel_ligand_res = []
    for atm in struct.atoms:
        if atm.residue.segid == 'A':
            sel_protein_atm.append(atm.idx)
    for res in struct.residues:
        if res.segid == 'LIG':
            sel_ligand_res.append(res.idx)
    if traj_file.endswith('.dcd'):
        traj = mdt.load(traj_file, top=psf_file)
    elif traj_file.endswith('.cor'):
        top = mdt.load_topology(psf_file)
        xyz = pmd.load_file(traj_file).positions.value_in_unit(pmd.unit.nanometers)
        xyz = [[list(c) for c in xyz]]
        traj = mdt.Trajectory(xyz, top)
    N_list = []
    for fi in range(traj.n_frames):
        nc = 0
        for s1 in sel_ligand_res:
            tag = False
            for a1 in struct.residues[s1].atoms:
                for s2 in sel_protein_atm:
                    d = np.sum((traj.xyz[fi,a1.idx,:]-traj.xyz[fi,s2,:])**2)**0.5
                    if d <= dist_cutoff:
                        #print(a1, s2, d)
                        nc += 1
                        tag = True
                        break
                if tag:
                    break
        N_list.append(nc)
    return N_list

def analysis(root_dir, ana_dir, traj_dir, init_idx, prefix, max_chain_length, eject_offset, termination_list, prot_prefix):
    global nsave, dt, alpha
    N_file_name = root_dir+'/'+ana_dir+'/Nb_'+str(int(traj_dir)+init_idx-1)+'_t.dat'
    f_N = open(N_file_name, 'w')
    f_N.close()
    
    TS = parse_out(traj_dir, nsave, dt, alpha)
    
    tag_header = False
    for chain_length in range(eject_offset+4, max_chain_length+1):
        for stage in range(3):
            if stage == 2:
                psf_name = './traj/'+traj_dir+'/'+prefix+str(chain_length+1)+'.psf'
            else:
                psf_name = './traj/'+traj_dir+'/'+prefix+str(chain_length)+'.psf'
            if chain_length == max_chain_length and stage == 2:
                break
            max_eject_idx = max([chain_length - eject_offset, 1]) - 1
            
            N_list = []
            if not os.path.exists(psf_name):
                N_list.append('NAN')
            else:
                for traj_name in TS[chain_length-1][stage][0]:
                    if traj_name.endswith('.cor'):
                        if os.path.exists(traj_name):
                            if not os.path.getsize(traj_name):
                                N_list.append('NAN')
                                continue
                        else:
                            N_list.append('NAN')
                            continue
                        N_list += Cal_N_ligand_bound(psf_name, traj_name)
                    else:
                        if os.path.exists(traj_name):
                            if not os.path.getsize(traj_name):
                                for ind in range(len(TS[chain_length-1][stage][1])-1):
                                    N_list.append('NAN')
                                continue
                        else:
                            for ind in range(len(TS[chain_length-1][stage][1])-1):
                                N_list.append('NAN')
                            continue
                        N_list += Cal_N_ligand_bound(psf_name, traj_name)
                    
            TS[chain_length-1][stage][2] = N_list
            if chain_length >= eject_offset+4 and not tag_header and N_list[-1] != 'NAN':
                tag_header = True
                f_N = open(N_file_name, 'a')
                f_N.write('%12s %5s %5s %6s\n'%('Time (s)', 'Len', 'Stage', 'Nb'))

                if chain_length == eject_offset+4 and stage == 0:
                    for i in range(eject_offset+3):
                        for j in range(len(TS[i])):
                            for k in range(len(TS[i][j][1])):
                                f_N.write('%12.6f %5d %5d %6d\n'%(TS[i][j][1][k], i+1, j+1, 0))
                f_N.close()
            
            f_N = open(N_file_name, 'a')
            for k in range(len(N_list)):
                if N_list[k] == 'NAN':
                    continue
                f_N.write('%12.6f %5d %5d %6d\n'%(TS[chain_length-1][stage][1][k], chain_length, stage+1, N_list[k]))
            f_N.close()

    if len(TS) <= max_chain_length:
        return

    for stage in range(2):
        psf_name = './traj/'+traj_dir+'/'+prefix+str(max_chain_length)+'.psf'
        traj_name = TS[max_chain_length][stage][0]
        N_list = Cal_N_ligand_bound(psf_name, traj_name)
        TS[max_chain_length][stage][2] = N_list
        f_N = open(N_file_name, 'a')
        for k in range(len(N_list)):
            f_N.write('%12.6f %5d %5d %6d\n'%(TS[max_chain_length][stage][1][k], max_chain_length, stage+4, N_list[k]))
        f_N.close()   
    

###################### MAIN ################################
if len(work_folder_list) == 0:
    work_folder_list = ['./']
root_dir = os.getcwd()
ana_dir = 'N_bind_vs_T'
if not os.path.exists(ana_dir):
    os.mkdir(ana_dir)

max_length = 0
max_num_traj = 0
for work_folder in work_folder_list:
    os.chdir(work_folder)
    if work_folder == './':
        init_idx = 1
    else:
        words = work_folder.split('-')
        init_idx = int(words[0])
    (num_traj, prot_prefix, total_chain_length, nsave, dt, alpha) = parse_info()

    prefix = 'rnc_l'

    traj_dir_list = []
    for file in os.listdir('./traj/'):
        if os.path.isdir('./traj/'+file):
            traj_dir_list.append(file)    
    
    pool = multiprocessing.Pool(nproc)
    for traj_dir in traj_dir_list:
        chain_length_list = []
        termination_list = []
        for file in os.listdir('./traj/'+traj_dir):
            if file.startswith(prefix) and file.endswith('_stage_3_final.cor'):
                name = os.path.splitext(file)[0]
                words = name.split('l')
                words = words[-2].split('_')
                chain_length_list.append(int(words[0]))
            elif file.startswith(prefix) and (file.endswith('_ejection.dcd') or file.endswith('_dissociation.dcd')):
                termination_list.append(file)
        max_chain_length = max(chain_length_list)
        if max_chain_length > max_length:
            max_length = max_chain_length
        max_num_traj += 1
        pool.apply_async(analysis, (root_dir, ana_dir, traj_dir, init_idx, prefix, max_chain_length, eject_offset, termination_list, prot_prefix))

    while True:
        time.sleep(10)
        if len(pool._cache) == 0:
            print('All Done.')
            break

    pool.close()
    pool.join()

    os.chdir(root_dir)
