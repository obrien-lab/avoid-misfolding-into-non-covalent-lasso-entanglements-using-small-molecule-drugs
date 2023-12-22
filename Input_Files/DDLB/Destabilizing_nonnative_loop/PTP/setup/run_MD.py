#!/usr/bin/env python3
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout, exit, stderr
import os, time, traceback
import parmed as pmd
import numpy as np

############################################
# energy decomposition 
def forcegroupify(system):
    forcegroups = {}
    for i in range(system.getNumForces()):
        force = system.getForce(i)
        force.setForceGroup(i)
        f = str(type(force))
        s = f.split('\'')
        f = s[1]
        s = f.split('.')
        f = s[-1]
        forcegroups[i] = f
    return forcegroups

def getEnergyDecomposition(handle, context, forcegroups):
    energies = {}
    for i, f in forcegroups.items():
        try:
            states = context.getState(getEnergy=True, groups={i})
        except ValueError as e:
            print(str(e))
            energies[i] = Quantity(np.nan, kilocalories/mole)
        else:
            energies[i] = states.getPotentialEnergy()
    results = energies
    handle.write('    Potential Energy:\n')
    for idd in energies.keys():
        handle.write('      %s: %.4f kcal/mol\n'%(forcegroups[idd], energies[idd].value_in_unit(kilocalories/mole))) 
    return results

# remove bond constraints of LIG atoms
def rm_cons_LIG(system, psf_pmd, forcefield, templete_map):
    system_new = forcefield.createSystem(top, nonbondedMethod=CutoffNonPeriodic,
                 nonbondedCutoff=2.0*nanometer, 
                 constraints=None, removeCMMotion=False, ignoreExternalBonds=True, 
                 residueTemplates=templete_map)
    bond_force = system_new.getForce(0)
    bond_parameter_list = [bond_force.getBondParameters(i) for i in range(bond_force.getNumBonds())]
    tag = 0
    while tag == 0 and system.getNumConstraints() != 0:
        for i in range(system.getNumConstraints()):
            con_i = system.getConstraintParameters(i)[0]
            con_j = system.getConstraintParameters(i)[1]
            segid_i = psf_pmd.atoms[con_i].residue.segid
            segid_j = psf_pmd.atoms[con_j].residue.segid
            if segid_i == 'LIG' and segid_j == 'LIG':
                system.removeConstraint(i)
                # print('Constraint %d is removed, range is %d'%(i, system.getNumConstraints()))
                for bp in bond_parameter_list:
                    if (con_i == bp[0] and con_j == bp[1]) or (con_i == bp[1] and con_j == bp[0]):
                        system.getForce(0).addBond(*bp)
                        break
                tag = 0
                break
            else:
                tag = 1
# END remove bond constraints of LIG atoms

############################################

psffile = sys.argv[1]
ncrstfile = sys.argv[2]
prmfile = sys.argv[3]
temp = float(sys.argv[4])
nproc = '2'
outname = sys.argv[5]
rand = int(sys.argv[6])
sim_time = float(sys.argv[7])

alpha = 4331293
timestep = 0.015*picoseconds
sim_steps = int(np.ceil(sim_time*1e9/alpha*nanoseconds / timestep / 5000) * 5000)
fbsolu = 0.05/picosecond
temp = temp*kelvin

psf_pmd = pmd.load_file(psffile)
psf = CharmmPsfFile(psffile)
rst = pmd.load_file(ncrstfile)
forcefield = ForceField(prmfile)
top = psf.topology
# re-name residues that are changed by openmm
for resid, res in enumerate(top.residues()):
    if res.name != psf_pmd.residues[resid].name:
        res.name = psf_pmd.residues[resid].name
templete_map = {}
for chain in top.chains():
    for res in chain.residues():
        templete_map[res] = res.name
system = forcefield.createSystem(top, nonbondedMethod=CutoffNonPeriodic,
        nonbondedCutoff=2.0*nanometer, 
        constraints=AllBonds, removeCMMotion=False, ignoreExternalBonds=True, 
        residueTemplates=templete_map)
custom_nb_force = system.getForce(4)
custom_nb_force.setUseSwitchingFunction(True)
custom_nb_force.setSwitchingDistance(1.8*nanometer)

# Turn off LJ 12-10-6 interactions between protein and ligands
custom_nb_force_copy = custom_nb_force.__copy__()
protein_atom_list = []
ligand_atom_list = []
for residue in psf_pmd.residues:
    if residue.segid == 'A':
        for atom in residue.atoms:
            protein_atom_list.append(atom.idx)
    elif residue.segid == 'LIG':
        ligand_atom_list.append([atom.idx for atom in residue.atoms])
for i in range(len(protein_atom_list)-1):
    custom_nb_force.addInteractionGroup([protein_atom_list[i]], protein_atom_list[i+1:])
ligand_combined_list = []
for lig in ligand_atom_list:
    ligand_combined_list += lig
for i in range(len(ligand_combined_list)-1):
    custom_nb_force.addInteractionGroup([ligand_combined_list[i]], ligand_combined_list[i+1:])
    
# Add LJ 12-6 interactions between protein and ligands
custom_nb_force_copy.setEnergyFunction('ke*charge1*charge2/ep/r*exp(-r/ld)+kv*(a/13/r^12 - c/2/r^6); '+
                                       'ke=ke1*ke2; ep=ep1*ep2; ld=ld1*ld2; kv=kv1*kv2; '+
                                       'a=acoef(index1, index2); c=ccoef(index1, index2)')
custom_nb_force_copy.setNonbondedMethod(0) # No cutoff
custom_nb_force_copy.setUseSwitchingFunction(False) # No switch
custom_nb_force_copy.addInteractionGroup(protein_atom_list, ligand_combined_list)
system.addForce(custom_nb_force_copy)

# Remove ligands bond constraints
rm_cons_LIG(system, psf_pmd, forcefield, templete_map)

# COM distance restraint
k = 0.1*kilocalories/mole/angstroms**2
R0 = 200 * angstrom
force = CustomCentroidBondForce(2, "k*(max(d-R0, 0))^2; d=distance(g1,g2)")
force.addGlobalParameter('k', k)
force.addGlobalParameter('R0', R0)
force.addGroup(protein_atom_list)
for g in ligand_atom_list:
    force.addGroup(g)
for g2_idx in range(len(ligand_atom_list)):
    force.addBond([0,g2_idx+1])
system.addForce(force)

forcegroups = forcegroupify(system)

integrator = LangevinIntegrator(temp, fbsolu, timestep)
integrator.setConstraintTolerance(0.00001)
integrator.setRandomNumberSeed(rand)

# prepare simulation
#platform = Platform.getPlatformByName('CPU')
#properties = {'Threads': nproc}

platform = Platform.getPlatformByName('CUDA')
properties = {'CudaPrecision': 'mixed'}
properties["DeviceIndex"] = "0"

forcegroups = forcegroupify(system)

# Attempt of creating the simulation object (sometimes fail due to CUDA environment)
i_attempt = 0
while True:
    try:
        simulation = Simulation(top, system, integrator, platform, properties)
    except Exception as e:
        print('Error occurred at attempt %d...'%(i_attempt+1))
        traceback.print_exc()
        i_attempt += 1
        continue
    else:
        break

simulation.context.setPositions(rst.coordinates[0]*angstrom)
simulation.context.setVelocities(rst.velocities[0]*angstrom/picosecond)

# append reporters
simulation.reporters = []
simulation.reporters.append(DCDReporter(outname+'.dcd', 5000, append=False))
simulation.reporters.append(pmd.openmm.reporters.RestartReporter(outname+'.ncrst', 5000, netcdf=True))
simulation.reporters.append(StateDataReporter(outname+'.out', 5000, step=True,
    potentialEnergy=True, temperature=True, progress=False, remainingTime=False,
    speed=True, separator='	'))

getEnergyDecomposition(stdout, simulation.context, forcegroups)
#simulation.minimizeEnergy(tolerance=1*kilojoule/mole)
#getEnergyDecomposition(stdout, simulation.context, forcegroups)

# run production simulation
simulation.step(sim_steps)
print('Done!')
