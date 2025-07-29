"""Executes tasks based on yaml configuration."""

import argparse
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

import churn

parser = argparse.ArgumentParser(
    description='Execute tasks based on yaml configuration.'
)

parser.add_argument(
    '--dry-run',
    action='store_true',
    help='Run the script in dry run mode without executing any tasks.',
)

parser.add_argument(
    'template_directory',
    type=Path,
    help='Path to the directory containing the template files.',
)

args = parser.parse_args()

with (args.template_directory / 'run.yaml').open() as config_file:
    config = yaml.safe_load(config_file)

churn.Configurator(
    config['context'],
    Path(config['output_folder']),
    args.template_directory,
).render()


def task_generator(tasks: list[dict[str, Any]]) -> Iterable[churn.Task]:
    """
    Generate tasks from the configuration.

    Parameters
    ----------
    tasks : list[dict[str, Any]]
        List of tasks to generate.

    Returns
    -------
    Iterable[churn.Task]
        Generator of Task objects.
    """
    return (
        churn.Task(
            task['name'],
            args.template_directory,
            Path(config['output_folder']),
            list(map(Path, task['output_files'])),
            list(map(Path, task.get('extra_input_files', []))),
        )
        for task in tasks
    )


if not args.dry_run:
    if (pre_tasks := config.get('pre_tasks')) is not None:
        churn.run_chain(*task_generator(pre_tasks))
    churn.create_batch_chain(*task_generator(config['tasks']))
