#!/bin/bash

############################################################
# This script will sbatch the slurm files in each subfolder.
############################################################

current_dir=$(pwd)

for dir in "$current_dir"/*; do
    if [ -d "$dir" ]; then
        # Find the .sh file in the directory
        slurm_path=$(find "$dir" -name '*.sh' -print -quit)

        # If no .sh file is found, skip this directory
        if [ -z "$slurm_path" ]; then
            continue
        fi

        slurm_file=$(basename "$slurm_path")
        
        folder_name=$(basename "$dir")

        cd "${dir}"
        echo "Sbatching ${slurm_file} from ${folder_name}..."
        sbatch $slurm_file
        cd ..

    fi
done
echo "Done."