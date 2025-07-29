"""Contains function to create a chain of jobs in SLURM."""

import shutil
import subprocess
from pathlib import Path

from churn.task import Task


def create_batch_chain(*tasks: Task, run_all: bool = False) -> bool:
    """
    Create a chain of jobs in SLURM.

    Each job is created with a dependency on the previous job. Tasks are run
    in the task folder.

    Parameters
    ----------
    tasks : Task
        Paths to the tasks to be submitted.
    run_all : bool
        If True, all tasks are run regardless of their dependencies. Default is False.

    Returns
    -------
    bool
        True if any tasks were submitted.
    """
    sbatch_executable = shutil.which('sbatch')
    if sbatch_executable is None:
        msg = 'sbatch executable not found in PATH'
        raise RuntimeError(msg)

    previous_jobid = None
    for task in tasks:
        if run_all or previous_jobid is not None or task.run():
            try:
                result = subprocess.run(  # noqa: S603
                    [
                        sbatch_executable,
                        *(
                            [f'--dependency=afterok:{previous_jobid}']
                            if previous_jobid is not None
                            else []
                        ),
                        '--export=ALL',
                        'batch.sh',
                    ],
                    cwd=task.output_folder / task.task_folder.name,
                    capture_output=True,
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print(f'Error submitting job: {e.stderr.decode()}')  # noqa: T201
                raise
            previous_jobid = result.stdout.decode().split()[-1]
    return previous_jobid is not None


def run_chain(*tasks: Task, run_all: bool = False) -> bool:
    """
    Run a chain of jobs directly.

    The jobs run sequentially in the task folder.

    Parameters
    ----------
    tasks : Task
        Paths to the tasks to be run.
    run_all : bool
        If True, all tasks are run regardless of their dependencies. Default is False.

    Returns
    -------
    bool
        True if any tasks ran.
    """
    previous_ran = run_all
    for task in tasks:
        if previous_ran or task.run():
            cwd = task.output_folder / task.task_folder.name
            batch_name = next(cwd.glob('batch.*'))
            try:
                result = subprocess.run(  # noqa: S603
                    [Path.cwd() / batch_name],
                    cwd=cwd,
                    capture_output=True,
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print(f'Error submitting job: {e.stderr.decode()}')  # noqa: T201
                raise
            print(result.stdout.decode())  # noqa: T201
            previous_ran = True
    return previous_ran
