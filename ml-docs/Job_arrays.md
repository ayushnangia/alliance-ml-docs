# Job arrays

Other languages:

- English
- [français](Job_arrays_fr.md)

*Parent page: [Running jobs](Scheduler.md)*

If your work consists of a large number of tasks which differ only in some parameter, you can conveniently submit many tasks at once using a *job array,* also known as a *task array* or an *array job*. The individual tasks in the array are distinguished by an environment variable, `$SLURM_ARRAY_TASK_ID`, which Slurm sets to a different value for each task. You set the range of values with the `--array` parameter.

See [Job Array Support](https://slurm.schedmd.com/job_array.html) for more details.

## Examples of the --array parameter

```
sbatch --array=0-7       # $SLURM_ARRAY_TASK_ID takes values from 0 to 7 inclusive
sbatch --array=1,3,5,7   # $SLURM_ARRAY_TASK_ID takes the listed values
sbatch --array=1-7:2     # Step size of 2, same as the previous example
sbatch --array=1-100%10  # Allows no more than 10 of the jobs to run simultaneously

```

## A simple example

**File :** simple\_array.sh

```
#!/bin/bash
#SBATCH --array=1-10
#SBATCH --time=3:00:00
program_x <input.$SLURM_ARRAY_TASK_ID
program_y $SLURM_ARRAY_TASK_ID some_arg another_arg

```

This job will be scheduled as ten independent tasks. Each task has a separate time limit of 3 hours, and each may start at a different time on a different host.

The script references `$SLURM_ARRAY_TASK_ID` to select an input file (named *program\_x* in our example), or to set a command-line argument for the application (as in *program\_y*).

Using a job array instead of a large number of separate serial jobs has advantages for you and other users. A waiting job array only produces one line of output in squeue, making it easier for you to read its output. The scheduler does not have to analyze job requirements for each task in the array separately, so it can run more efficiently too.

Note that, other than the initial job-submission step with `sbatch`, the load on the scheduler is the same for an array job as for the equivalent number of non-array jobs. The cost of dispatching each array task is the same as dispatching a non-array job. You should not use a job array to submit tasks with very short run times, e.g. much less than an hour. Tasks with run times of only a few minutes should be grouped into longer jobs using [META](META-Farm.md), [GLOST](GLOST.md), [GNU Parallel](GNU_Parallel.md), or a shell loop inside a job.

## Example: Multiple directories

Suppose you have multiple directories, each with the same structure, and you want to run the same script in each directory. If the directories can be named with sequential numbers then the example above can be easily adapted. If the names are not so systematic, then create a file with the names of the directories, like so:

```
$ cat case_list
pacific2016
pacific2017
atlantic2016
atlantic2017

```

There are several ways to select a given line from a file; this example uses `sed` to do so:

**File :** directories\_array.sh

```
#!/bin/bash
#SBATCH --time=3:00:00
#SBATCH --array=1-4

echo "Starting task $SLURM_ARRAY_TASK_ID"
DIR=$(sed -n "${SLURM_ARRAY_TASK_ID}p" case_list)
cd $DIR

# Place the code to execute here
pwd
ls

```

Cautions:

- Take care that the number of tasks you request matches the number of entries in the file.
- The file `case_list` should not be changed until all the tasks in the array have run, since it will be read each time a new task starts.

## Example: Multiple parameters

Suppose you have a Python script doing certain calculations with some parameters defined in a Python list or a NumPy array such as

**File :** my\_script.py

```
import time
import numpy as np

def calculation(x, beta):
    time.sleep(2) #simulate a long run
    return beta * np.linalg.norm(x**2)

if __name__ == "__main__":
    x = np.random.rand(100)
    betas = np.linspace(10,36.5,100) #subdivise the interval [10,36.5] with 100 values
    for i in range(len(betas)): #iterate through the beta parameter
        res = calculation(x,betas[i])
        print(res) #show the results on screen

# Run with: python my_script.py

```

The above task can be processed in a job array so that each value of the beta parameter can be treated in parallel.
The idea is to pass the `$SLURM_ARRAY_TASK_ID` to the Python script and get the beta parameter based on its value.
The Python script becomes

**File :** my\_script\_parallel.py

```
import time
import numpy as np
import sys

def calculation(x, beta):
    time.sleep(2) #simulate a long run
    return beta * np.linalg.norm(x**2)

if __name__ == "__main__":
    x = np.random.rand(100)
    betas = np.linspace(10,36.5,100) #subdivise the interval [10,36.5] with 100 values
    
    i = int(sys.argv[1]) #get the value of the $SLURM_ARRAY_TASK_ID
    res = calculation(x,betas[i])
    print(res) #show the results on screen

# Run with: python my_script_parallel.py $SLURM_ARRAY_TASK_ID

```

The job submission script is (note the array parameters goes from 0 to 99 like the indexes of the NumPy array)

**File :** data\_parallel\_python.sh

```
#!/bin/bash
#SBATCH --array=0-99
#SBATCH --time=1:00:00
module load scipy-stack
python my_script_parallel.py $SLURM_ARRAY_TASK_ID

```