#!/bin/bash

# Default values
queue="engineering"
memory=5
gpus=0  # Default number of GPUs is 0
account=''

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -q|--queue) queue="${2:-$queue}"; shift 2;;
        -m|--memory) memory="${2:-$memory}"; shift 2;;
        -g|--gpus) gpus="${2:-$gpus}"; shift 2;;
        *) echo "Unknown parameter passed: $1"; exit 1;;
    esac
done

if [[ "$gpus" -gt 0 ]]; then
    echo "here"
    account="--gres=gpu:$gpus -A gpu-general-users"
fi

# Construct and execute the srun command
srun --partition="$queue" --nodes=1 --ntasks=1 --cpus-per-task=1 --time=2700 --mem="${memory}G" $account --pty bash

# If the number of GPUs is greater than 1, load the Miniconda module
if [[ "$gpus" -gt 0 ]]; then
    echo "here"
    module load miniconda/miniconda3-2023-environmentally || { echo "Failed to load miniconda module"; exit 1; }
fi