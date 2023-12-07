#!/bin/bash

############################################################
# This script will sbatch the slurm files in each subfolder.
# The slurm file must be named as follows:
# (HINT: same as 'slurm_new_name' in 'slurmgod-create.sh')
############################################################
slurm_file="cp2k-slurm.sh"
############################################################

current_dir=$(pwd)

for dir in "$current_dir"/*; do
    if [ -d "$dir" ]; then
        # If no input file is found, skip this directory
        if [ ! -f "$dir"/$slurm_file ]; then
            continue
        fi
        
        job_name=$(basename "$dir")
        echo "Launching from  $job_name"

        cd "${dir}"
        sbatch $slurm_file
        cd ..

    fi
done
echo "Done."

