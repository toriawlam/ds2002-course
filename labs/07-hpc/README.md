
## Lab 07: HPC

This lab gets you hands-on with **high performance computing (HPC)** workflows using the **Slurm** scheduler. You will run a *single batch job* and then scale it up to a **job array** that processes multiple input files in parallel as resources become available.

You’ll use a lightweight text-analysis task (word counting with **lemmatization**) as the motivating example. The ratio of unique word count to total word count serves as an indicator of the author's vocabulary complexity. This is an advancement compared to the processing of the *Moby Dick* text in an earlier lab.

---

## Learning goals

By completing this lab, you will be able to:

- Write and submit Slurm batch scripts (`sbatch`).
- Understand and use common `#SBATCH` directives (job name, partition, memory, time, CPUs).
- Monitor jobs using `squeue` and `sacct`.
- Use **job arrays** (`#SBATCH --array`) and the environment variable `SLURM_ARRAY_TASK_ID` to parallelize “one file per task” workloads.
- Follow HPC best practices: run work in `/scratch/$USER/...` rather than cluttering your home directory.

---

## Setup (HPC environment)

1. Log in to the UVA HPC system in a terminal.

2. Load and activate the course Python environment:

```bash
module load miniforge
source activate ds2002
```

3. Install NLTK (needed by the provided text-processing script):

```bash
pip install --user nltk
```

> If you already have NLTK installed in your environment, you can skip this step.

4. Input data and processing script

In `labs/07-hpc/`, the course repo includes:

- `create-book-files.sh` – downloads **five Project Gutenberg novels** into:
  - `book-1.txt` (Pride and Prejudice, Jane Austen)
  - `book-2.txt` (The Count of Monte Cristo, Alexandre Dumas)
  - `book-3.txt` (Dracula, Bram Stoker)
  - `book-4.txt` (Metamorphosis, Franz Kafka)
  - `book-5.txt` (The Kingdom of God Is Within You, Leo Tolstoy)
- `process-book.py` – reads an input `.txt` file, tokenizes text into words, **lemmatizes** tokens, counts word frequencies, and writes a CSV `word,count` file.

---


## Task 1: Create the input files in scratch

Create a scratch working directory for this lab and generate the input text files there:

```bash
WORKDIR=/scratch/$USER/ds2002-jobruns/text-analysis
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# Run the provided helper script from the course repo
bash ~/ds2002-course/labs/07-hpc/create-book-files.sh
```

Confirm that you now have `book-1.txt` … `book-5.txt` in your scratch directory:

```bash
ls -lh book-*.txt
```

These files refer to the following books:

- `book-1.txt` – Pride and Prejudice by Jane Austen
- `book-2.txt` – The Count of Monte Cristo by Alexandre Dumas
- `book-3.txt` – White Fang by Jack London
- `book-4.txt` – Dracula by Bram Stoker
- `book-5.txt` – Metamorphosis by Franz Kafka

---

## Task 2: Write and run a serial Slurm job (one file)

1. In your fork of the course repo, create a folder:

- `~/ds2002-course/mywork/lab7`

2. In that folder, create a Slurm job script named `serial-book.sh` that:

- Has a shebang: `#!/bin/bash`
- Includes these Slurm directives (you may adjust time/memory if needed):
  - `--account=ds2002`
  - `--job-name` (choose your own)
  - `--output=serial-book-%j.out`
  - `--error=serial-book-%j.err`
  - `--time=00:10:00`
  - `--partition=standard`
  - `--mem=8G`
  - `--nodes=1`
  - `--ntasks-per-node=1`
  - `--cpus-per-task=1`
- Runs the provided Python script `process-book.py` on **one file**:
  - Input: `book-1.txt`
  - Output: `results-1.csv`

Your Python invocation should look like this:

```bash
python ~/ds2002-course/labs/07-hpc/process-book.py book-1.txt results-1.csv
```

3. Submit the job:

```bash
sbatch ~/ds2002-course/mywork/lab7/serial-book.sh
```

4. Monitor the job status:

```bash
squeue --me
# or:
sacct -S today
```

5. When the job completes, verify the output file exists in scratch and inspect the first few lines:

```bash
ls -lh results-1.csv
head results-1.csv
```

Your output should look like this:

```text
word,count
a,3049
abatement,1
abbey,1
abhorrence,6
...
```

### Task 3: Convert the serial job to a job array

Now you will scale the workflow to process **five files** using a **job array**.

1. Copy your serial script to a new file, `jobarray-book.sh`.

2. Edit `jobarray-book.sh`:

- Revise the log and error file specification. The %A and %a will expand to the parent job ID and specific task ID, respectively.
  - `#SBATCH --output=jobarray-book-%A-%a.out`
  - `#SBATCH --error=jobarray-book-%A-%a.err`
- It includes the directive: `#SBATCH --array=1-5`
- It uses the array index to select the input and output:
  - Input: `book-${SLURM_ARRAY_TASK_ID}.txt`
  - Output: `results-${SLURM_ARRAY_TASK_ID}.csv`
- It runs `process-book.py` using those variables.

Take a look at the job array example in [practice/08-hpc](../../practice/08-hpc/) for inspiration if needed.

3. Submit the job array:

```bash
sbatch ~/ds2002-course/mywork/lab7/jobarray-book.sh
```

4. Monitor the job array. Note how logs contain both the array job ID and task index:

```bash
squeue --me
sacct -S today
```

5. When the array completes, confirm you have all five output files:

```bash
ls -lh results-*.csv
```

6. **Optional:** Expand the job array

Feel free to add additional books or other text sources as `book-*.txt` files, resize the job array, and submit again to fully explore the gains in analysis throughput. You can either edit the `create-book-files.sh` script or manually create new `book-*.txt` files.

The results of this optional activity are not required for lab submission.

---

## Deliverables (what to submit)

Commit these files to your forked course repo under `mywork/lab7/`:

- `serial-book.sh` – your single-job script
- `jobarray-book.sh` – your job-array script

You do **not** need to commit the `/scratch/...` output files; those are generated on the cluster and may be large.

---

## Submit your work

1. Copy the `results-*.csv` files to `~/ds2002-course/mywork/lab7/`. 
2. Run `sacct -S 2026-03-09 > ~/ds2002-course/mywork/lab7/jobhistory.txt`. Don't worry if your job history shows TIMEOUT, FAILED, or CANCELLED jobs. That will not affect your lab score. **The intention for this lab is for you to try and explore; it is not about perfect results.** Most of my initial job submissions fail at first because I have overlooked some detail. Making adjustments is an iterative process that supports your learning!
3. The `~/ds2002-course/mywork/lab7/` folder should contain:
   - serial-book.sh
   - jobarray-book.sh
   - results-1.csv
   - results-2.csv
   - results-3.csv
   - results-4.csv
   - results-5.csv
   - jobhistory.txt
  
4. Add and commit your files:

```bash
cd ~/ds2002-course
git add mywork/lab7/*
git commit -m "Complete Lab 07: HPC job arrays"
git push
```

5. Submit the URL of your `mywork/lab7` folder in Canvas, e.g.:

`https://github.com/YOUR_USERNAME/ds2002-course/tree/main/mywork/lab7`