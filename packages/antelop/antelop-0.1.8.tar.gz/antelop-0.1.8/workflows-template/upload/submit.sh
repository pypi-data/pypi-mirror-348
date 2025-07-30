#!/bin/bash

logdir=<data_dir>/logs
mkdir -p $logdir/$1
cd $logdir/$1

sbatch --export=$2 -t 1:00:00 -c 1 --parsable <install_dir>/workflows/upload/upload.slurm "$3" "$4" "$5"
