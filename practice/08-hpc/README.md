# High Performance Computing

The goal of this activity is to familiarize you with high performance computing (HPC) systems and concepts. HPC is essential for running computationally intensive workloads, parallel processing, and leveraging specialized hardware for data science tasks that require significant computational resources.

If the initial examples and lab feel like a breeze, challenge yourself with activities in the *Advanced Concepts* section and explore the resource links at the end of this post.

* Confirm you completed the **Setup** steps.
* Go through the **In-class Exercises** to familiarize yourself with serial jobs, job arrays, and the process of job submission, and job status checks.
* Continue with the **Lab 07 - HPC** section. 
* Optional: Explore the **Advanced Concepts** if you wish to try multi-core processing and GPU jobs for deep learning.

## Setup

To follow along, complete the [HPC Setup instructions](../../setup/hpc.md) if you haven’t already. Then log into the UVA HPC cluster and create a dedicated directory for job input and output so batch jobs run from scratch instead of your home directory:

```bash
mkdir -p /scratch/$USER/ds2002-jobruns
```

## Working directory best practices

On Afton/Rivanna, each account has two main directories: **`/home/$USER/`** and **`/scratch/$USER/`**. Use each for the right purpose so your jobs run efficiently and your data stays manageable.

**Home directory (`/home/$USER/` or `~`)**

- Store personal configuration (e.g. `~/.bashrc`)
- Store code and scripts.
- Store conda/venv environments (e.g. `~/.conda/envs/ds2002`).
- On Afton/Rivanna, home is backed up: daily snapshots are kept for a week in `/home/.snapshots`, so you can recover accidentally deleted files. Home is not intended for large or temporary job I/O.

**Scratch directory (`/scratch/$USER/`)**

- **Temporary** storage for job input and output. Use it to stage data and write results for compute jobs.
- Scratch is usually on a high-performance filesystem with fast parallel read/write, so jobs I/O runs faster than from home.
- Scratch is much larger than home but has strict policies: on Afton/Rivanna, files unused for 90 days are automatically deleted. There are no backups—do not keep the only copy of important data only on scratch.
- ***Do not store your code and scripts here!***

**Recommendation:** Run batch jobs from scratch. For this course, set a working directory and `cd` into it before submitting or running job scripts:

```bash
WORKDIR=/scratch/$USER/ds2002-jobruns
mkdir -p $WORKDIR
cd $WORKDIR
```

Here, `$USER` is your computing ID (e.g. `khs3z`), so the path becomes something like `/scratch/khs3z/ds2002-jobruns`.

## In-class exercises

Let's get started and submit some jobs. All examples are in `practice/08-hpc`.

### Serial Job

Serial jobs use only a single CPU core. This is in contrast to parallel jobs which use multiple CPU cores simultaneously. 

#### Step 1: The job script

Afton/Rivanna uses [Slurm (Simple Linux Utility for Resource Management)](https://slurm.schedmd.com/overview.html) to manage job submissions and scheduling. Jobs are scheduled by submitting a job script to the scheduler.

A job script is a specialized Bash script: 

- Starts with #SBATCH directives that define hardware resources for job execution;
- Loads the software tools needed;
- Followed by commands to execute.

The first example is `01-hello.sh`. It looks like this:
 
```bash
#!/bin/bash
#SBATCH --account=ds2002
#SBATCH --job-name=hello
#SBATCH --output=hello-%j.out
#SBATCH --error=hello-%j.err
#SBATCH --time=00:01:00
#SBATCH --partition=standard
#SBATCH --mem=8G
#SBATCH --nodes=1                   # that's the default for standard partition
#SBATCH --ntasks-per-node=1         # that's the default for standard partition
#SBATCH --cpus-per-task=1           # that's the default for standard partition

# Execute some simple commands to print information about the job
# The output will be saved to the files specified in the #SBATCH --output and #SBATCH --error directives.
echo "Hello, ds2002!"
echo "The job is running on the $(hostname) node."
echo "The job id is $SLURM_JOB_ID"
echo "The job name is $SLURM_JOB_NAME."
echo "Available resources for this job:"
echo "  - CPU Cores (per task): $SLURM_CPUS_PER_TASK"
echo "  - Memory: $SLURM_MEM_PER_NODE"

# Redirect some output to a file
echo "Redirection of echo/print output to specific file" > hello.txt
# uncomment next line to print all environment variables related to SLURM
# printenv | grep SLURM >> hello.txt
```

The first part defines the allocation to use, a jobname, output and error filenames, time limit, hardware partition, needed memory, nodes, and cpu cores. For complete reference, review [References > Batch directives](#batch-directives).

#### Step 2: Submit the job

We assume you have the fork of the course repository in `~/ds2002-course`. Run the following two commands, update the paths if needed.

```bash
cd /scratch/$USER/ds2002-jobruns
sbatch ~/ds2002-course/practice/08-hpc/01-hello.sh
```

Following best practice, we change into a work directory in the /scratch folder first, then we submit the job with the `sbatch` command. `sbatch` is a command provided by Slurm resource manager. It will take your job script, inspect the #SBATCH directives and add it to the job queue.

You should see a message:
```
Submitted batch job 10058413
```

**Common errors:**

- `sbatch: error: Batch job submission failed: Invalid partition name specified` - Check `#SBATCH --partition` in your job script and make sure it matches one of the [available partitions](#available-partitions-and-limits). The partition names may vary from system to system.
- `sbatch: error: Batch job submission failed: Requested time limit is invalid (missing or exceeds some limit)` - Check the `qlist` command and ensure that your job script sets a time limit within the bounds of the selected partition.
- `sbatch: error: Batch job submission failed: Job violates accounting/QOS policy or AssocGrpBillingMinutes` - Indicates that the allocated account, project, or user has exhausted their service units (system credits) which provide CPU/GPU time. Run the `allocations` command to check your allocation balance, see [References > Allocation account](#allocation-account).

#### Step 3: Check job status

**Active jobs**

Now that the job is in the queue, we can check its status with the `squeue` command. You can add a job's ID to get information about a particular job (update the job number with your specific job ID).

```bash
squeue --job 10058413
```

At first you may see something like this:
```
JOBID      PARTITION   NAME   USER    ST    TIME  NODES   NODELIST(REASON) 
10058413   standard-+  hello  khs3z   PD    3:05    1     (none)
```

The `ST` column indicates the job status; `PD` stands for `PENDING`, meaning the job is in the queue waiting to be allocated to hardware but not running yet.

You can run `squeue 10058413 --start` to get an estimate when the job may run. Note that this is a best guess estimate and not 100% accurate.

Depending on how busy the cluster is, the job may quickly be placed on a node and run. The `squeue` `ST` field would change to `R` (`RUNNING`).

Output:
```
JOBID      PARTITION   NAME   USER    ST    TIME  NODES   NODELIST(REASON) 
10058413   standard-+  hello  khs3z    R    3:05    1     udc-an38-5
```

If you want to see all your active jobs run:
```bash
squeue --me
```

**Job history**

The sacct command shows your active jobs (in the queue) as well as past jobs. Run this command and compare its output to the `squeue` command.

```bash
sacct -S 2026-03-01 
```

Output:
```
JobID           JobName  Partition    Account  AllocCPUS      State ExitCode 
------------ ---------- ---------- ---------- ---------- ---------- --------
10057749          hello standard-+     ds2002          1  COMPLETED      0:0 
10057749.ba+      batch                ds2002          1  COMPLETED      0:0 
```

See [References > Checking job status](#checking-job-status) for a complete list of job states and their meaning.

It is important to review how long your completed jobs actually took to execute. We refer to this as the elapsed time, as opposed to the time limit specified in the job script. 

```bash
sacct -S 2026-03-01 --format=jobid,jobname%25,partition,account,start,elapsed,end,state,exit
```

#### Step 4: Review output

When the job has successfully completed the `01-hello.sh` script, you should have three files:
- hello-10057749.err
- hello-10057749.out
- hello.txt

The first two are generated by Slurm and have collected all standard output or error messages produced during execution of the job script. Note that the filenames contain the job IDs, as we had specified with `#SBATCH --output=hello-%j.out` and `#SBATCH --error=hello-%j.err`. **If you are using a logger in Python, instead of print statements, they likely all end up in the `.err` files even for outputs from `logger.info`. That's just a default, so don't be concerned about that.

In addition, we created `hello.txt` to capture specific output by redirecting output of the `echo` command. This is simply to illustrate the flexibility you have to capture a subset of "terminal" message in specific files if needed. 

### Job Arrays

Job arrays run the same script many times with a different **array index** per run. Slurm sets `SLURM_ARRAY_TASK_ID` (e.g. 1, 2, 3, …) so each task can handle a different input. This is ideal for “one file per task” workflows.

**Simple example: text processing with 5 files**

Suppose you have five input files `data-1.txt` … `data-5.txt` and a script `process-text.py` that takes input and output paths.

#### Step 1: Create the input files

In your working directory (e.g. `/scratch/$USER/ds2002-jobruns`) run the provided script:

```bash
bash ~/ds2002-course/practice/08-hpc/create-text-files.sh
```

This creates `data-1.txt` … `data-5.txt` with different content so each file has a different word count. The job array script `02-jobarray-text.sh` runs one task per file.

#### Step 2: Setup the job script
- Request a job array with `#SBATCH --array=1-5` (tasks 1 through 5). Each task gets its own `SLURM_ARRAY_TASK_ID` (1, 2, 3, 4, 5).

- In the job script, set INPUT and OUTPUT filenames based on the job array task index `${SLURM_ARRAY_TASK_ID}` and call the Python script. The example in `02-jobarray-text.sh` looks like this:

```bash
#!/bin/bash
#SBATCH --account=ds2002
#SBATCH --job-name=text-array
#SBATCH --output=text-array-%A_%a.out
#SBATCH --error=text-array-%A_%a.err
#SBATCH --partition=standard
#SBATCH --time=00:05:00
#SBATCH --mem=8G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --array=1-5

INPUT="data-${SLURM_ARRAY_TASK_ID}.txt"
OUTPUT="results-${SLURM_ARRAY_TASK_ID}.txt"

module load miniforge
source activate ds2002
python ~/ds2002-course/practice/08-hpc/process-text.py "$INPUT" "$OUTPUT"
```

- `%A` = job array job ID; `%a` = array task index. So each task gets its own log (e.g. `text-array-123_1.out`, `text-array-123_2.out`).
- Task 1 runs `process-text.py data-1.txt results-1.txt`, task 2 runs `process-text.py data-2.txt results-2.txt`, and so on.
- Run `sbatch` from a directory that contains (or can see) `data-1.txt` … `data-5.txt`, or set `WORKDIR` and `cd` there before the `python` line.

### Step 3: Submit the job script

In your WORKDIR, run:

```bash
sbatch ~/ds2002-course/practice/08-hpc/02-jobarray-text.sh
```

#### Step 4: Check job status

Use `squeue` and `sacct` to check on your jobs.

```
10112610_1   text-array          1 2026-03-09T15:25:44   00:00:01  COMPLETED      0:0 
10112610_1.+      batch          1 2026-03-09T15:25:44   00:00:01  COMPLETED      0:0 
10112610_2   text-array          1 2026-03-09T15:25:44   00:00:01  COMPLETED      0:0 
10112610_2.+      batch          1 2026-03-09T15:25:44   00:00:01  COMPLETED      0:0 
10112610_3   text-array          1 2026-03-09T15:25:44   00:00:01  COMPLETED      0:0 
10112610_3.+      batch          1 2026-03-09T15:25:44   00:00:01  COMPLETED      0:0 
10112610_4   text-array          1 2026-03-09T15:25:44   00:00:01  COMPLETED      0:0 
10112610_4.+      batch          1 2026-03-09T15:25:44   00:00:01  COMPLETED      0:0 
10112610_5   text-array          1 2026-03-09T15:25:44   00:00:01  COMPLETED      0:0 
10112610_5.+      batch          1 2026-03-09T15:25:44   00:00:01  COMPLETED      0:0
```

Note the job ID format. The `10112610` designates the job array; the suffix (after the `_`) indicates the task ID.

#### Step 5: Review output

Slurm will schedule 5 tasks; each reads one `data-<id>.txt` and writes one `results-<id>.txt`.

Check with:
```bash
ls -ltr
```

```
-rw------- 1 khs3z users    0 Mar  9 18:52 text-array-10112610_2.err
-rw------- 1 khs3z users    0 Mar  9 18:52 text-array-10112610_3.err
-rw------- 1 khs3z users    0 Mar  9 18:52 text-array-10112610_1.err
-rw------- 1 khs3z users    0 Mar  9 18:52 text-array-10112610_5.err
-rw------- 1 khs3z users    0 Mar  9 18:52 text-array-10112610_4.err
-rw------- 1 khs3z users   52 Mar  9 18:52 text-array-10112610_1.out
-rw------- 1 khs3z users   42 Mar  9 18:52 results-1.txt
-rw------- 1 khs3z users   52 Mar  9 18:52 text-array-10112610_5.out
-rw------- 1 khs3z users   43 Mar  9 18:52 results-5.txt
-rw------- 1 khs3z users   52 Mar  9 18:52 text-array-10112610_2.out
-rw------- 1 khs3z users   43 Mar  9 18:52 results-2.txt
-rw------- 1 khs3z users   52 Mar  9 18:52 text-array-10112610_4.out
-rw------- 1 khs3z users   43 Mar  9 18:52 results-4.txt
-rw------- 1 khs3z users   52 Mar  9 18:52 text-array-10112610_3.out
-rw------- 1 khs3z users   43 Mar  9 18:52 results-3.txt
```

## Advanced Concepts (Optional)

### Single Node Multiprocessing Jobs

This section shows how to move from a **purely serial** Python job to a **multi-process** job on a *single node* using Python's `multiprocessing` package and small tweaks to the Slurm directives in the job script.

The Python code is in `serial-pi.py` (single core processing) and `mp-pi.py` for multi-core processing. In these examples, π is estimated using the Monte Carlo method.

**single core processing (serial)**

The key function in `serial-pi.py`:

```python
def calculate_pi(num_points):
    """
    Calculate pi using the Monte Carlo method. We use an inefficent for loop on purpose to demonstrate the serial nature of the computation.
    """
    master = random.Random()
    seed = master.randint(0, 2**32 - 1)
    random.seed(seed)
    logging.info(f"Calculating pi using {num_points} points")
    num_inside = 0
    for _ in range(num_points):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            num_inside += 1
    return 4 * num_inside / num_points
```

This is a **brute-force Monte Carlo** approach to estimating the value of π:

- We imagine a unit square \([0,1] \times [0,1]\) with a quarter of a unit circle of radius 1 inside it.
- The loop throws `num_points` random “darts” uniformly into the square (`x`, `y` in \([0,1]\)).
- It counts how many land **inside the quarter circle** (`x**2 + y**2 <= 1`) in `num_inside`.
- The fraction `num_inside / num_points` approximates the area ratio (area of quarter circle)/(area of square) = (π/4).
- Multiplying by 4 gives an estimate of π: `4 * num_inside / num_points`.

Review the entire scripts, and submit a serial job like so (run from a directory on the cluster where the repo is available):

```bash
sbatch ~/ds2002-course/practice/08-hpc/03-serial-pi.sh
```

The script `03-serial-pi.sh` sets `NUM_POINTS=100000000` and `OUTPUT_FILE=pi.csv` internally.

As we increase the number of points (random dart throws), the estimate reflects the actual value of π more precisely. But, the calculation also takes much longer.

**multi-core processing**

If we have multiple CPU cores available, we can use the same Monte Carlo idea but split the work across processes where the number of processes matches the number of CPU cores.

Let's take a look at an example, the Python script `mp-pi.py` which is invoked by the `04-mp-pi.sh` job script.

The job script `04-mp-pi.sh` is very similar to the serial version. 

```bash
#!/bin/bash
#SBATCH --account=ds2002
#SBATCH --job-name=pi
#SBATCH --output=pi-%a.out
#SBATCH --error=pi-%a.err
#SBATCH --time=00:01:00
#SBATCH --partition=standard
#SBATCH --mem-per-cpu=8G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8

NUM_POINTS=100000000
OUTPUT_FILE=pi.csv

# use $SLURM_CPUS_PER_TASK to get the number of CPU cores assigned to the job
# use $SLURM_MEM_PER_CPU to get the amount of memory assigned to each CPU core
echo "Number of CPU cores assigned to the job: $SLURM_CPUS_PER_TASK"
echo "Amount of memory assigned to each CPU core: $SLURM_MEM_PER_CPU"

# we pass the number of CPU cores assigned to the job to set up the ideal number of processes inside the python script
python ~/ds2002-course/practice/08-hpc/mp-pi.py $NUM_POINTS $OUTPUT_FILE $SLURM_CPUS_PER_TASK
```

Note the following #SBATCH directives:
- `#SBATCH --mem-per-cpu=8G` – this replaces `--mem=8G` in the serial version.
- `#SBATCH --cpus-per-task=8` – note the increase from 1 to 8 compared to the serial version.
- Passing `SLURM_CPUS_PER_TASK` as the third argument lets `mp-pi.py` create exactly that many worker processes, so the Python code automatically matches the number of processes to the cores Slurm assigned.

The key adjustments in the `mp-pi.py` script are in the `calculate_pi` function and addition of a new function `count_inside` that is called from within `calculate_pi`. 
- `mp-pi.py` takes three arguments: `<num_points> <output_file> <num_processes>`.
  - `calculate_pi(num_points, num_processes)` divides the total number of random points into `num_processes` chunks.
  - A `multiprocessing.Pool` runs `count_inside` in parallel on each chunk, then sums the partial counts to estimate π in the same way as the serial version (just faster when more cores are available).

```python
def calculate_pi(num_points, num_processes):
    """
    Distribute num_points across num_processes workers; sum inside counts and compute pi.
    """
    logging.info(f"Calculating pi using {num_points} points and {num_processes} processes")
    master = random.Random()
    base_seed = master.randint(0, 2**32 - 1)
    # distribute the numpoints across the workers
    chunk_size = num_points // num_processes
    remainder = num_points % num_processes
    chunks = []
    for i in range(num_processes):
        n = chunk_size + (1 if i < remainder else 0)
        if n > 0:
            chunks.append((n, base_seed, i))
    logging.info(f"Chunks: {chunks}")

    # create a pool of workers and map the count_inside function to the chunks
    # counts is a list of results returned by each worker
    with Pool(processes=num_processes) as pool:
        counts = pool.map(count_inside, chunks)
    
    # aggregate the results
    total_inside = sum(counts)
    return 4.0 * total_inside / num_points
```

```python
def count_inside(args):
    """
    Worker: generate n_points random (x,y) and return how many fall inside unit circle.
    args = (n_points, base_seed, worker_id) so each worker has distinct random number generator state.
    """
    n_points, base_seed, worker_id = args
    random.seed(base_seed + worker_id)
    num_inside = 0
    for _ in range(n_points):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            num_inside += 1
    logging.info(f"Worker {worker_id}: {num_inside} points of {n_points} points inside are within the unit circle")
    return num_inside
```

In the Python script, we need to define a function that is called by each process, we call it `count_inside`. At its core it retains the same approach of randomly hitting the dart board. As arguments it needs the number of points to "test" (i.e. number of darts to throw at the dart board), a unique seed to initialize the random number generator, and the id of the worker process.  

To submit the multiprocessing job (run from a directory on the cluster where the repo is available):

```bash
sbatch ~/ds2002-course/practice/08-hpc/04-mp-pi.sh
```

When the serial and multiprocessing jobs have completed, compare their runtimes:
```bash
sacct --format=jobid,jobname,alloccpus,start,elapsed,state,exit
```

### GPU Jobs

**PyTorch and the deep learning example**

[PyTorch](https://pytorch.org/) is a widely used framework for deep learning. Training neural networks on large datasets is much faster on a **GPU** than on CPU, so HPC clusters provide GPU nodes and a way to request them in your job. This example runs the official PyTorch **MNIST** demo: it trains a small convolutional network on the MNIST handwritten-digit dataset and reports training progress and final test accuracy.

**Job script (`05-pytorch.sh`)**

The script requests a single GPU device on a single node and runs the example inside an Apptainer container with GPU support (more on containers in a few weeks):

- `#SBATCH --partition=gpu` and `#SBATCH --gres=gpu:1` – request one GPU (required for GPU jobs).
- `#SBATCH --mem=32G`, `#SBATCH --time=00:10:00`, `#SBATCH --cpus-per-task=4` – resources for data loading and training.
- The script downloads the PyTorch MNIST example from GitHub (`curl -o pytorch-example.py ...`) so no local copy is required.
- `module load apptainer` and `module load pytorch` – load the environment that provides the PyTorch container and `CONTAINERDIR`.
- `apptainer run --nv $CONTAINERDIR/pytorch-2.9.0.sif pytorch-example.py` – run the Python script inside the container; `--nv` enables NVIDIA GPU access.

**Python script (`pytorch-example.py`)**

The example (same as [PyTorch examples – MNIST](https://github.com/pytorch/examples/tree/main/mnist)) trains a small CNN on MNIST for 14 epochs by default. It prints training loss per batch and, at the end of each epoch, test-set average loss and accuracy. All output goes to the job’s stdout (and thus to the `.out` file).

**How to submit**

From a directory on the cluster (e.g. `/scratch/$USER/ds2002-jobruns`):

```bash
sbatch ~/ds2002-course/practice/08-hpc/05-pytorch.sh
```

**Expected results**

When the job completes, check the output file (e.g. `pytorch-<jobid>.out`). The tail of the file will show the final test result for the last epoch, for example:

```
Test set: Average loss: 0.0283, Accuracy: 9912/10000 (99%)
```

Exact numbers may vary slightly. Training progress (epoch, batch, loss) appears above this final line.

## References

### Batch directives

Batch directives define hardware resources for job execution (e.g. number of CPU cores, memory, specialty hardware like GPUs, and time limit). For the Slurm scheduler, these directives start with the `#SBATCH` keyword.

Below are the most common directives used in the course examples. For the full list, see the [Slurm sbatch documentation](https://slurm.schedmd.com/sbatch.html). 

#### Allocation Account

```
#SBATCH --account=ds2002
```

Billing account or project to charge for the job. On Rivanna/Afton, use the allocation assigned to the course (e.g. `ds2002`).

To check allocations you have access to, run this command:
```bash
allocations
```

Output:
```
Account                      Balance        Reserved       Available                
-----------------          ---------       ---------       ---------                
ds2002                       1000000               0          999559 
```

The available column indicates how many service units are available. Service units reflect credits and are related to how much compute time you have access to. When the available balance is zero, you will not be able to submit any new jobs. In such case, reach out to your course instructor or research advisor who can request additional credits.

#### Job name

```
#SBATCH --job-name=hello
```

Human-readable name for the job. Shown in queue listings (`squeue`) and in job history.

#### Output and error files

```
#SBATCH --output=hello-%j.out
#SBATCH --error=hello-%j.err
```

File where standard output (stdout) and standard error (stderr) are written. `%j` is replaced by the job ID so each run gets unique files.

#### Partition

Queue (partition) to submit to. A partition defines a set of compute nodes; they are often grouped based on particular hardware specifications or job use cases.

```
#SBATCH --partition=standard
```

For this course, we'll use:
- `standard` for all non-GPU jobs;
- `gpu` for any examples that involve GPU devices; 
- `interactive` for Open OnDemand apps like VSCode, JupyterLab, etc.
 
If you use `#SBATCH --partition=gpu` on Afton/Rivanna, you have to combine this with a `#SBATCH --gres` directive to specify how many GPUs you need (and optionally which type), see [GPU Jobs](#gpu-jobs). 

#### GPU resource (gres)

```
#SBATCH --gres=gpu:1
```

Requests one GPU for the job. Use `gpu:2` (or more) for multi-GPU jobs. Only meaningful when using the `gpu` partition.


#### Nodes

```
#SBATCH --nodes=1
```

Number of compute nodes to allocate for the job. For most course jobs you use a single node (`1`). Multi-node jobs (e.g. `--nodes=2`) are for distributed runs across several machines and are rarely needed for the examples here. On many partitions, `1` is the default.

#### Tasks per node

```
#SBATCH --ntasks-per-node=1
```

Number of tasks (processes) to run per node. For a single serial or multithreaded program, use `1` task per node. Use more than one when you launch multiple separate processes (e.g. with MPI). On many partitions, `1` is the default.

#### CPUs per task

```
#SBATCH --cpus-per-task=4
```

Number of CPU cores per task. Useful for multi-threaded or data-loading workloads.

#### Memory

```
#SBATCH --mem=32G
```

Total memory (RAM) for the job on each node. Here, 32 GB. Adjust based on your script’s needs.

Alternatively, you can use `#SBATCH --mem-per-cpu=9GB` to specify how much memory should be allocated for each cpu core. This is the preferred way for code that involves multi-threading or multi-processing to prevent "starving" cpu cores of memory as the number of threads/processes is increased, see [Single Node Multiprocessing Jobs](#single-node-multiprocessing-jobs).

The `--mem` and `--mem-per-cpu` directives are mutually exclusive; you have to choose one or the other.

#### Time limit

```
#SBATCH --time=00-00:10:00
```

Maximum wall-clock time (dd-HH:MM:SS). The job is terminated when the time limit is reached; 10 minutes in this example. Request only what you need so the job can start sooner.

#### Available partitions and limits

The `qlist` command shows all available partitions and how busy they are. You may not have access to all of them. The ones relevant for this course are `interactive`, `standard`, and `gpu`.

```bash
qlist
```

```
PARTITION                     TOTAL_CORES FREE_CORES  RUNNING_JOBS   PENDING_JOBS   TIMELIMIT    
----------------------------------------------------------------------------------------------------
interactive                   2208        710         28             1              12:00:00    
standard                      18032       10602       688            216            7-00:00:00  
dedicated                     368         96          1              3              infinite    
parallel                      17184       504         115            9              3-00:00:00  
gpu                           4104        2628        259            343            3-00:00:00  
bii                           4360        439         2              25             7-00:00:00  
bii-gpu                       608         0           1              7              3-00:00:00  
bii-largemem                  3744        336         1              1              7-00:00:00  
gpu-mig                       128         70          29             12             3-00:00:00 
```


The `qlimits` command shows the max number of cpu cores, memory, and nodes you can request in each partition.

```bash
qlimits
```

```
Queue          Maximum      Maximum          Minimum      Maximum       Maximum       Default       Maximum      Minimum     
(partition)    Submit       Cores(GPU)/User  Cores/Job    Mem/Node(MB)  Mem/Core(MB)  Mem/Core(MB)  Nodes/Job    Nodes/Job   
========================================================================================================================
standard       5000         cpu=1500                      384000+                     4000          1                        
dedicated      10000                                      768000+                     4000          UNLIMITED                
interactive    5000         cpu=24                        128000+                     4000          2                        
parallel       2000         cpu=6000                      768000                      4000          64           2           
gpu            10000        gres/gpu=32                   257000+                     4000          16                       
bii            10000        cpu=400                       384000                      4000          112                      
bii-gpu        10000                                      384000+                     4000          12                       
bii-largemem   10000                                      768000+                     4000          10                       
gpu-mig        2000         gres/gpu=28                   2000000       15000         4000          1   
```

### Submit a Job

The `sbatch` command submits the job script to the scheduler. As best practice, change into a dedicated work directory before running `sbatch`. E.g.,

```bash
cd /scratch/$USER/ds2002-jobruns
sbatch ~/ds2002-course/practice/08-hpc/01-hello.sh
```

Output:
```
Submitted batch job 10058413
```

### Checking Job Status

The `squeue` command shows you all the jobs currently in the job queue. You can add a job's ID to get information about a particular job.

```bash
squeue --job 10058413
```

Output:
```
JOBID      PARTITION  NAME      USER    ST    TIME  NODES   NODELIST(REASON) 
10058413   gpu-a6000  pytorch-  khs3z    R    3:05    1     udc-an38-5
```
The `ST` field indicates the job's status. 

- PD: Pending; in the queue waiting for available hardware
- R: Running
- CG: Completing; commands in the job script have completed and the resource manager is cleaning up

To only see all your active jobs, run:
```bash
squeue --me
```

>**Note:** the `squeue` command only lists active jobs, either pending, running, or cancelling. 

The sacct command shows your active jobs (in the queue) as well as past jobs. 

```bash
sacct -S 2026-03-01 
```

Output:
```
JobID           JobName  Partition    Account  AllocCPUS      State ExitCode 
------------ ---------- ---------- ---------- ---------- ---------- --------
10057749          hello standard-+     ds2002          4  COMPLETED      0:0 
10057749.ba+      batch                ds2002          4  COMPLETED      0:0 
10058297     pytorch-e+  gpu-a6000     ds2002          4     FAILED    127:0 
10058297.ba+      batch                ds2002          4     FAILED    127:0 
10058317     pytorch-e+  gpu-a6000     ds2002          4    TIMEOUT      0:0 
10058317.ba+      batch                ds2002          4  CANCELLED     0:15 
10058413     pytorch-e+  gpu-a6000     ds2002          4  COMPLETED      0:0 
10058413.ba+      batch                ds2002          4  COMPLETED      0:0 
10079753     pytorch-e+  gpu-a6000     ds2002          4    RUNNING      0:0 
10079753.ba+      batch                ds2002          4    RUNNING      0:0
```

- PD (PENDING): The job is waiting for resource allocation. The squeue output will often provide a reason in the NODELIST(REASON) column (e.g., "Priority", "Resources", "Dependency").
- R (RUNNING): The job has an allocated node(s) and is currently executing its tasks or batch script.
- CG (COMPLETING): The job has finished execution but is performing cleanup tasks, such as running the epilog script or staging out data.
- CD (COMPLETED): The job completed successfully, exiting with a zero exit code.
- F (FAILED): The job terminated with a non-zero exit code or some other failure condition.
- CA (CANCELLED): The job was explicitly canceled by a user or system administrator.
- TO (TIMEOUT): The job was terminated because it exceeded its allocated time limit (wall time).
- OOM (OUT_OF_MEMORY): The job terminated because it exceeded its requested memory limit.
- NF (NODE_FAIL): The job terminated due to the failure of one or more of its allocated nodes.
- S (SUSPENDED): The job's execution has been suspended, and its allocated CPUs have been released for other jobs.
- ST (STOPPED): The job's execution has been stopped (using SIGSTOP), but its resources have been retained.

## Resources

- [UVA Research Computing](https://www.rc.virginia.edu/)
- [Intro to UVA's HPC System](https://learning.rc.virginia.edu/tutorials/hpc-intro/)
- [HPC Wiki](https://hpc-wiki.info/hpc/HPC_Wiki)
- [Slurm](https://slurm.schedmd.com/overview.html)
