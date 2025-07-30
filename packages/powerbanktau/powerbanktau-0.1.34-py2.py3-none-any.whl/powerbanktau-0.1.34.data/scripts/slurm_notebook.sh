#!/bin/bash

# Check if a directory is passed as an argument
if [ -z "$1" ]; then
  echo "Error: No directory provided."
  echo "Usage: ./script.sh /path/to/directory [partition] [memory] [gpus] [env] [jobname] [base_port]"
  exit 1
fi

directory=$1            # First argument: directory to work in
partition=${2:-engineering}  # Second argument: Slurm partition (default: 'engineering')
mem=${3:-3G}            # Third argument: memory (default: 3G)
gpus=${4:-0}            # Fourth argument: number of GPUs (default: 0)
env=${5:-base}          # Fifth argument: conda environment (default: 'base')
jobname=${6:-workspace} # Sixth argument: job name (default: 'workspace')
base_port=${7:-8888}    # Seventh argument: base port (default: 8888)
account=""

# If GPUs are requested, configure Slurm GRES and account
if [ "$gpus" -gt 0 ]; then
  account="--gres=gpu:$gpus -A gpu-general-users"
fi

# Submit the job to Slurm
sbatch <<EOT
#!/bin/bash
#SBATCH --partition=$partition
#SBATCH --mem=$mem
#SBATCH --job-name=$jobname
#SBATCH --ntasks=1
#SBATCH --time=120:00:00
#SBATCH --output=/tamir2/nicolaslynn/logging/output/slurm-%j.out
#SBATCH --error=/tamir2/nicolaslynn/logging/error/slurm-%j.err
#SBATCH $account

# Load user environment
source ~/.bashrc
source /tamir2/nicolaslynn/home/miniconda3/etc/profile.d/conda.sh

# If GPUs are requested, load the Miniconda module
if [ "$gpus" -gt 0 ]; then
    module load miniconda/miniconda3-2023-environmentally || { echo "Failed to load miniconda module"; exit 1; }
fi

# Print the Job ID
echo "Job ID: \$SLURM_JOB_ID"

# Print node information
echo "Node List for Job ID: \$SLURM_JOB_ID"
echo \$SLURM_NODELIST

# Function to find an available port

# Change to the specified directory
cd $directory || { echo "Error: Directory not found: $directory"; exit 1; }

# Activate the Conda environment
conda activate $env || { echo "Error: Conda environment '$env' not found"; exit 1; }

# Start Jupyter Lab
jupyter lab --ip=* --port=$base_port --no-browser
EOT