#!/bin/bash
#SBATCH -J job_moni
#SBATCH -p gpuA40x4
#SBATCH --mail-type=END
#SBATCH -o %j.o # Name of stdout output file
#SBATCH -e %j.e # Name of stderr error file
#SBATCH -N 1
#SBATCH -n 2
#SBATCH --gpus=0
#SBATCH -t 48:00:00
#SBATCH -A bbjq-delta-gpu

cd $SLURM_SUBMIT_DIR

python job_monitor_delta.py
