#!/usr/bin/env python3
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout, exit, stderr
import os, time, traceback
import parmed as pmd
import numpy as np
import mdtraj as mdt

###### convert time seconds to hours ######
def convert_time(seconds):
    return seconds/3600
###### END convert time seconds to hours ######

############## MAIN #################
prmtop_file = sys.argv[1]
ncrst_file = sys.argv[2]
temp = float(sys.argv[3])
ppn = sys.argv[4]
outname = sys.argv[5]
rand = int(sys.argv[6])
sim_step = int(float(sys.argv[7]))
if len(sys.argv) == 9:
    use_gpu = int(sys.argv[8])
else:
    use_gpu = -1
cpfile = outname+'.ncrst'

timestep = 2.0*femtoseconds
fbsolu = 2/picosecond
nsteps_save = 50000
temp = temp*kelvin

current_step = 0
if_restart = 0
if os.path.exists(outname+'.out'):
    ff = open(outname+'.out')
    lines = ff.readlines()
    last_line = lines[-1].strip()
    ff.close()
    if not last_line.startswith('Time') and os.path.getsize(outname+'.out') != 0:
        if_restart = 1
        current_step = int(last_line.split()[1])
else:
    f = open(outname+'.out', 'w')
    f.write('%10s %20s %13s %13s %10s %12s\n'%('Time(ns)', 'Steps', 'Ep (kcal/mol)', 'Ek (kcal/mol)', 'T (K)',  'Speed (ns/d)'))
    f.close()
    
if current_step >= sim_step:
    print('Simulation has been run for %d steps >= the total step %d. No more simulation need to run.'%(current_step, sim_step))
    sys.exit()

structure = pmd.load_file(prmtop_file)
system = structure.createSystem(nonbondedMethod=PME,
                                nonbondedCutoff=10.0*angstroms,
                                constraints=HBonds)
# Restrain the last C-alpha atom
force = CustomExternalForce("k*((x-x0)^2+(y-y0)^2+(z-z0)^2)")
force.addPerParticleParameter("k")
force.addPerParticleParameter("x0")
force.addPerParticleParameter("y0")
force.addPerParticleParameter("z0")
coor_list = pmd.load_file(ncrst_file).coordinates[0]
rest_idx = 0
for atom in structure.atoms:
    if atom.name == 'CA':
        rest_idx = atom.idx
force.addParticle(rest_idx, (1*kilocalories_per_mole/angstroms**2,
                  coor_list[rest_idx][0]*angstroms, coor_list[rest_idx][1]*angstroms, coor_list[rest_idx][2]*angstroms))
system.addForce(force)

integrator = LangevinIntegrator(temp, fbsolu, timestep)
integrator.setConstraintTolerance(0.00001)
integrator.setRandomNumberSeed(rand)

# prepare simulation
if use_gpu == -1:
    properties = {'Threads': ppn}
    platform = Platform.getPlatformByName('CPU')
else:
    dev_index = use_gpu
    properties = {'CudaPrecision': 'mixed'}
    properties["DeviceIndex"] = "%d"%(dev_index);
    platform = Platform.getPlatformByName('CUDA')

# Attempt of creating the simulation object (sometimes fail due to CUDA environment)
i_attempt = 0
while True:
    try:
        simulation = Simulation(structure.topology, system, integrator, platform, properties)
    except Exception as e:
        print('Error occurred at attempt %d...'%(i_attempt+1))
        traceback.print_exc()
        i_attempt += 1
        continue
    else:
        break

if if_restart != 0:
    try:
        rst = pmd.load_file(cpfile)
        simulation.context.setPositions(rst.coordinates[0]*angstrom)
        simulation.context.setVelocities(rst.velocities[0]*angstrom/picosecond)
        simulation.context.setPeriodicBoxVectors(np.array([rst.cell_lengths[0], 0, 0])*angstrom, 
                                                 np.array([0, rst.cell_lengths[1], 0])*angstrom, 
                                                 np.array([0, 0, rst.cell_lengths[2]])*angstrom)
    except Exception as e:
        print(e)
        print('Warning: Fail to load checkpoint, use the last frame and random velocity instead.')
        dcd_traj = mdt.load(outname+'.dcd', top=prmtop_file)
        dcd_traj[-1].save(outname+'.pdb')
        current_cor = PDBFile(outname+'.pdb')
        os.system('rm -f '+outname+'.pdb')
        simulation.context.setPositions(current_cor.getPositions())
        simulation.context.setVelocitiesToTemperature(temp)
        rst = pmd.load_file(ncrst_file)
        simulation.context.setPeriodicBoxVectors(np.array([rst.cell_lengths[0], 0, 0])*angstrom, 
                                                 np.array([0, rst.cell_lengths[1], 0])*angstrom, 
                                                 np.array([0, 0, rst.cell_lengths[2]])*angstrom)
else:
    rst = pmd.load_file(ncrst_file)
    simulation.context.setPositions(rst.coordinates[0]*angstrom)
    simulation.context.setVelocitiesToTemperature(temp)
    simulation.context.setPeriodicBoxVectors(np.array([rst.cell_lengths[0], 0, 0])*angstrom, 
                                             np.array([0, rst.cell_lengths[1], 0])*angstrom, 
                                             np.array([0, 0, rst.cell_lengths[2]])*angstrom)

# append reporters
simulation.reporters = []
simulation.reporters.append(pmd.openmm.reporters.RestartReporter(cpfile, nsteps_save, netcdf=True))
if if_restart != 0:
    simulation.reporters.append(DCDReporter(outname+'.dcd', nsteps_save, append=True))
else:
    simulation.reporters.append(DCDReporter(outname+'.dcd', nsteps_save, append=False))

# Compute the number of degrees of freedom.
dof = 0
for i in range(system.getNumParticles()):
    if system.getParticleMass(i) > 0*dalton:
        dof += 3
dof -= system.getNumConstraints()
if any(type(system.getForce(i)) == CMMotionRemover for i in range(system.getNumForces())):
    dof -= 3

# run production simulation
start_time = time.time()
nframe = 0
while True:
    simulation.step(nsteps_save)
    nframe += 1
    if if_restart == 0:
        time_id = nsteps_save * nframe * timestep.value_in_unit(nanosecond)
        step_id = nsteps_save * nframe
    else:
        time_id = (current_step + nsteps_save * nframe) * timestep.value_in_unit(nanosecond)
        step_id = current_step + nsteps_save * nframe
        
    end_time = time.time()
    time_cost = convert_time(end_time - start_time)
    speed = nsteps_save * nframe * timestep.value_in_unit(nanosecond) / time_cost * 24
    Ep = simulation.context.getState(getEnergy=True).getPotentialEnergy().value_in_unit(kilocalorie/mole)
    Ek = simulation.context.getState(getEnergy=True).getKineticEnergy().value_in_unit(kilocalorie/mole)
    Temp = (2*simulation.context.getState(getEnergy=True).getKineticEnergy()/
                    (dof*MOLAR_GAS_CONSTANT_R)).value_in_unit(kelvin)
    
    f = open(outname+'.out', 'a')
    f.write('%10.3f %20d %13.6g %13.6g %10.4f %12.2f\n'%(time_id, step_id, Ep, Ek, Temp, speed))
    f.close()
    if step_id >= sim_step:
        break
