#!/usr/bin/env bash

#SBATCH -J grid_lr
#SBATCH --qos main
#SBATCH --output=/home/users/aslee/WASA_faciesXRF/job_logs/slurm-%j.txt
#SBATCH -c 10
#SBATCH --mem=10GB
#SBATCH -t 01:00:00


/home/users/aslee/miniconda3/bin/python /home/users/aslee/WASA_faciesXRF/grid_raw_lr.py
#/home/users/aslee/miniconda3/bin/python /home/users/aslee/WASA_faciesXRF/grid_raw_svc.py
#/home/users/aslee/miniconda3/bin/python /home/users/aslee/WASA_faciesXRF/grid_raw_rf.py