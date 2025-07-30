import os
import gc
from tqdm import tqdm
from pathlib import Path
import pandas as pd
from dask_jobqueue import PBSCluster, SLURMCluster
from dask.distributed import Client, wait, LocalCluster


# def launch_slurm_dask_cluster(memory_size="3GB", num_workers=25, queue="engineering",
#                               walltime="7200", dashboard_address=":23154", cores=1, processes=1,
#                           log_directory="~/../logging/dask-logs", working_directory=None,
#                           gpus=0, gpu_module="miniconda/miniconda3-2023-environmentally"):

# """
# :param memory_size: The amount of memory allocated for each Dask worker (default is '3GB').
# :param num_workers: The number of workers to be created in the Dask cluster (default is 25).
# :param queue: The SLURM queue/partition to use for job scheduling (default is 'engineering').
# :param walltime: The maximum wall clock time for the job in seconds (default is '7200').
# :param dashboard_address: The address for the Dask dashboard (default is ':23154').
# :param cores: The number of CPU cores to allocate for each worker (default is 1).
# :param processes: The number of processes per worker (default is 1).
# :param log_directory: The directory to store Dask worker logs (default is '~/../logging/dask-logs').
# :param working_directory: The working directory where the SLURM job will execute (default is None).
# :param gpus: The number of GPUs to allocate for each worker (default is 0).
# :param gpu_module: The module to load before execution (default is 'miniconda/miniconda3-2023-environmentally').
# :return: A tuple consisting of the Dask client and the SLURMCluster instance.
# """
# Commands to execute before worker starts
# pre_executors = []
# if working_directory is not None:
#     pre_executors.append(f"cd {working_directory}")

# # Load GPU module if GPUs are requested
# if gpus > 0:
#     pre_executors.append(f"module load {gpu_module}")
#     job_extra = {
#         "--gres": f"gpu:{gpus}",  # Request the number of GPUs
#         "-A": "gpu-general-users"  # Add account info for GPU partition
#     }
# else:
#     job_extra = {}

# # Create SLURMCluster depending on whether GPUs are requested or not
# cluster = SLURMCluster(
#     cores=cores,
#     memory=memory_size,
#     processes=processes,
#     queue=queue,
#     walltime=walltime,
#     scheduler_options={"dashboard_address": dashboard_address},
#     log_directory=log_directory,
#     job_script_prologue=pre_executors,
#     job_extra_directives=job_extra if gpus > 0 else None  # Pass `job_extra` only if GPUs are used
# )

# # Scale the cluster to the specified number of workers
# cluster.scale(num_workers)

# # Connect the Dask client to the cluster
# client = Client(cluster)

# return client, cluster

def launch_slurm_dask_cluster(memory_size="3GB", num_workers=25, queue="engineering",
                        walltime="7200", dashboard_address=":23154", cores=1, processes=1,
                        log_directory="~/../logging/dask-logs", working_directory=None,
                        gpus=0, gpu_module="miniconda/miniconda3-2023-environmentally"):
    """
    :param memory_size: The amount of memory allocated for each Dask worker (default is '3GB').
    :param num_workers: The number of workers to be created in the Dask cluster (default is 25).
    :param queue: The SLURM queue/partition to use for job scheduling (default is 'tamirQ').
    :param walltime: The maximum wall clock time for the job in seconds (default is '7200').
    :param dashboard_address: The address for the Dask dashboard (default is ':23154').
    :param cores: The number of CPU cores to allocate for each worker (default is 1).
    :param processes: The number of processes per worker (default is 1).
    :param log_directory: The directory to store Dask worker logs (default is '~/.dask-logs').
    :param working_directory: The working directory where the SLURM job will execute (default is None).
    :return: A tuple consisting of the Dask client and the SLURMCluster instance.
    """
    pre_executors = []
    if working_directory is not None:
        pre_executors.append(f"cd {working_directory}")

    if gpus > 0:
        # Load the specified GPU module before execution
        pre_executors.append(f"module load {gpu_module}")

    if gpus == 0:
        cluster = SLURMCluster(
            cores=cores,
            memory=memory_size,
            processes=processes,
            queue=queue,
            walltime=walltime,
            scheduler_options={"dashboard_address": dashboard_address},
            log_directory=log_directory,
            job_script_prologue=pre_executors
        )
    else:
        cluster = SLURMCluster(
            cores=cores,
            memory=memory_size,
            processes=processes,
            queue=queue,
            walltime=walltime,
            scheduler_options={"dashboard_address": dashboard_address},
            log_directory=log_directory,
            job_script_prologue=pre_executors,
            extra=[f"--gres=gpu:{gpus}"]
        )


    cluster.scale(num_workers)
    client = Client(cluster)
    return client, cluster


def launch_local_dask_cluster(memory_size="3GB", num_workers=25, dashboard_address=":23154", cores=1):
    cluster = LocalCluster(
        n_workers=num_workers,
        threads_per_worker=cores,
        memory_limit=memory_size,
        dashboard_address=dashboard_address,
    )
    client = Client(cluster)
    return client, cluster


def launch_pbs_dask_cluster(memory_size="3GB", num_workers=25, queue="tamirQ",
                        walltime="24:00:00", dashboard_address=":23154", cores=1, processes=1,
                        log_directory="~/.dask-logs", working_directory=None):
    """
    :param memory_size: The amount of memory to allocate for each worker node, specified as a string (e.g., "3GB").
    :param num_workers: The number of worker nodes to start in the PBS cluster.
    :param queue: The job queue to submit the PBS jobs to.
    :param walltime: The maximum walltime for each worker node, specified as a string in the format "HH:MM:SS".
    :param dashboard_address: The address where the Dask dashboard will be hosted.
    :param cores: The number of CPU cores to allocate for each worker node.
    :param processes: The number of processes to allocate for each worker node.
    :param log_directory: The directory where Dask will store log files.
    :param working_directory: The directory to change to before executing the job script on each worker node.
    :return: A tuple consisting of the Dask client and the PBS cluster objects.
    """
    pre_executors = []
    if working_directory is not None:
        pre_executors.append(f"cd {working_directory}")

    cluster = PBSCluster(
        cores=cores,
        memory=memory_size,
        processes=processes,
        queue=queue,
        walltime=walltime,
        scheduler_options={"dashboard_address": dashboard_address},
        log_directory=log_directory,
        job_script_prologue=pre_executors
    )

    cluster.scale(num_workers)
    client = Client(cluster)
    return client, cluster


def process_and_save_tasks(tasks, funct, dask_client, save_loc, file_index=0, capacity=1000, save_multiplier=10):
    def save_results(results, index):
        if results:
            df = pd.concat(results)
            df.to_csv(os.path.join(save_loc, f'results_{index}.csv'))
            return []

        return results

    futures, all_results = [], []
    for i, task in tqdm(enumerate(tasks), total=len(tasks)):
        futures.append(dask_client.submit(funct, task))
        if (i + 1) % capacity == 0:
            wait(futures)
            all_results.extend([f.result() for f in futures if f.status == 'finished' and f.result() is not None])
            futures = []

        if (i + 1) % (capacity * save_multiplier) == 0:
            all_results = save_results(all_results, file_index)
            file_index += 1
            gc.collect()

    wait(futures)
    all_results.extend([f.result() for f in futures if f.status == 'finished' and f.result() is not None])
    save_results(all_results, file_index)
    return all_results


def collect_results(result_dir):
    """
    :param result_dir: Directory containing result CSV files to be collected
    :return: A concatenated pandas DataFrame containing data from all CSV files in the result directory
    """
    result_path = Path(result_dir)
    data = [pd.read_csv(file) for file in result_path.iterdir()]
    return pd.concat(data)


def restart_checkpoint(result_dir, patern='*'):
    """
    :param patern:
    :param result_dir: Directory path where checkpoint result files are stored.
    :return: A tuple containing a list of unique mutation IDs processed from the checkpoint files and the highest checkpoint index found.
    """
    result_path = Path(result_dir)
    files = sorted(result_path.glob(patern), key=lambda x: int(x.stem.split('_')[-1]), reverse=True)

    if not files:
        return [], 0

    try:
        data = []
        latest_file = files[0]
        for file in files:
            data.append(pd.read_csv(file))
        processed_muts = pd.concat(data).mut_id.unique().tolist()
        highest_checkpoint = int(latest_file.stem.split('_')[-1])
        return processed_muts, highest_checkpoint

    except Exception as e:
        print(f"Error processing file {files}: {e}")
        return [], 0

