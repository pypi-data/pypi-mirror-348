#!/bin/bash
#SBATCH --job-name=antelop_analysis
#SBATCH --partition=cpu
#SBATCH --ntasks=1

container=<install_dir>/containers/antelop-python.sif
envstr="DB_USER=$DB_USER,DB_PASS=$DB_PASS,DB_HOST=$DB_HOST,S3_USER=$S3_USER,S3_PASS=$S3_PASS,S3_HOST=$S3_HOST"

echo $3

echo "Upload in progress..."
apptainer exec -B <data_dir> -B $3 -B <install_dir> --env $envstr $container python <install_dir>/workflows/upload/upload.py --tablename "$1" --insert_dict "$2"
echo "Upload completed."
