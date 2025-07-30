#!/bin/bash

# Check if a directory is passed as an argument
if [ -z "$1" ]; then
  echo "Error: No directory provided."
  echo "Usage: ./script.sh /path/to/directory [partition] [memory]"
  exit 1
fi

directory=$1
partition=${2:-tamirQ}
mem=${3:-5gb}
jobname=${4:-workspace}
base_port=${5:-8888}

# Submit the job to PBS
qsub -q $partition -l mem=$mem,walltime=120:00:00,nodes=1:ncpus=1 -N $jobname -o /tamir2/nicolaslynn/logging/output/pbs-$PBS_JOBID.out -e /tamir2/nicolaslynn/logging/error/pbs-$PBS_JOBID.err <<EOT
source /tamir2/nicolaslynn/home/miniconda3/etc/profile.d/conda.sh


# Change to the specified directory
cd $directory || { echo "Directory not found"; exit 1; }

# Print the Job ID
echo "Job ID: \$PBS_JOBID"

# Print node information
echo "Node List for Job ID: \$PBS_JOBID"
cat \$PBS_NODEFILE

# Activate base environment explicitly
conda activate base
echo "conda env list"

# Start Jupyter Lab
jupyter lab --ip=* --port=$base_port --no-browser
EOT