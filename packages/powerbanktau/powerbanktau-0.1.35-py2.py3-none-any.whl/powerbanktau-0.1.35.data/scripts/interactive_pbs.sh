#!/bin/sh

# Default values
queue="tamirQ"
memory=5
cpus=1
gpus=0

# Parse arguments
while [ "$#" -gt 0 ]; do
    case "$1" in
        -q|--queue) queue="$2"; shift 2;;
        -m|--memory) memory="$2"; shift 2;;
        -c|--cpus) cpus="$2"; shift 2;;
        -g|--gpus) gpus="$2"; shift 2;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
done

## Conditional logic similar to Python script
#if [ "$gpus" -eq 0 ]; then
#    gpus=1
#fi

# Construct and execute the command
qsub -q $queue -I -l nodes=1:ppn=1,ngpus=$gpus,ncpus=$cpus,cput=24:00:00,mem="${memory}gb",pmem="${memory}gb",pvmem="$(($memory * 2))gb",vmem="$(($memory * 2))gb"
#qsub -q tamirQ -I -l nodes=1:ppn=1,ngpus=0,ncpus=1,cput=24:00:00,mem=5gb,pmem=5gb,vmem=10gb,pvmem=10gb
#qsub -q hugemem -I -l nodes=1:ppn=1,ngpus=0,ncpus=1,cput=1:00:00,mem=5gb,pmem=5gb,pvmem=10gb,vmem=10gb