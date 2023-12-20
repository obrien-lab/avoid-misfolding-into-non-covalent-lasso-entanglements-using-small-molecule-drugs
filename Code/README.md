### These are the codes used in performing the coarse-grained level and all-atom level simulations for protein co-translational and post-translational folding with the presence of small molecule ligands.

### 1. continuous_synthesis_v7.py
This is an updated version of the previous code [`continuous_synthesis_v6.py`](https://github.com/obrien-lab/cg_simtk_protein_folding/blob/master/Continuous_synthesis_protocol/continuous_synthesis_v6.py) for the co-translational protein folding simulation. 
In this version (v7), we incorporated the LJ 12-6 interactions between ligands and nascent chain. Details of the methodology can be found in the paper.

#### Parameters in Control file
The following parameters are new in this version. The description of other parameters can be found [here](https://github.com/obrien-lab/cg_simtk_protein_folding/wiki/continuous_synthesis_v6.py#3-parameters-in-control-file).
| Keywords | Type | Intepretation |
| ------ | ------ | ------ |
| start_traj_id | int | The trajectory index to start. This effects the output file names. |
| spherical_restraint_mask | string | Molecules to be restained within a shpere. For example, selection block "L24 : 42 - 59" will select all atoms in resid 42 to 59 of segid L24. Use ":" to select residue number and "@" to select atom name. Use " - " to select a range of residues (space required) and "," to select multiple individual residue. Use "\|" to separate multiple selection blocks. |
| spherical_restraint_center | float * 3 | x y z coordinate of the spherical center in angstrom for the restraint. |
| spherical_restraint_radius | float | Spherical radius in angstrom for the restraint. |

#### Example of the control file for a simulation with ligand (LIG) present
```
use_gpu = 1
tpn = 1
ppn = 1
num_traj = 3
prot_psf = setup/4c5c_model_clean_ca.psf
prot_top = setup/4c5c_model_clean_ca.top
prot_param = setup/4c5c_model_clean_nscal1_fnn1_go_bt.prm
ribo_psf = setup/50S_tRNA_cg_truncated_9VD.psf
ribo_top = setup/50S_tRNA_cg_9VD.top
ribo_param = setup/combine_ribo_L24_9VD_ep_1.0.prm
starting_strucs = setup/50S_tRNA_cg_truncated.cor
start_nascent_chain_length = 1
total_nascent_chain_length = 9999
temp_prod = 310
mrna_seq = setup/4c5c_mrna_sequence_slow.txt
trans_times = setup/Fluitt_ecoli_trans_time_310K_avg_16.5.txt
uniform_ta = 0
uniform_mfpt = 0.05
ribo_free_mask = L24 : 42 - 59 | LIG
time_stage_1 = 0.000340
time_stage_2 = 0.004201
ribosome_traffic = 1
initiation_rate = 0.083333
scale_factor = 4375901
x_eject = 60
spherical_restraint_mask = LIG
spherical_restraint_center = 160 0 0
spherical_restraint_radius = 100
log_file = info_1-3.log
restart = 1
start_traj_id = 1
```

Please refer to the [wiki page of previous version](https://github.com/obrien-lab/cg_simtk_protein_folding/wiki/continuous_synthesis_v6.py) for more information.


### 2. post_trans_single_run_v2.py

### 3. run_NVT_MD.py
