#!/bin/bash
#SBATCH -J C_1_51_51
#SBATCH -p gpuA40x4
#SBATCH --mail-type=NONE
#SBATCH -o %j.o # Name of stdout output file
#SBATCH -e %j.e # Name of stderr error file
#SBATCH -N 1
#SBATCH -n 2
#SBATCH --gpus=1
#SBATCH --mem=64GB
#SBATCH -t 48:00:00
#SBATCH -A bbjq-delta-gpu

cd $SLURM_SUBMIT_DIR

continuous_synthesis_v7.py -f CSP_51-51.cntrl
