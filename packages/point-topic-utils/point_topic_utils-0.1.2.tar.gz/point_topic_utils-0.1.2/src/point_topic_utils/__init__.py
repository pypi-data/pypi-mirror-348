from datetime import datetime
from typing import List, Optional

from .db.mongodb import MongoDBClient
from .models.project import Project
from .get_secrets import get_secrets

import argparse

__version__ = "0.1.0"


def update_status(
    project_name: str,
    raw_args: list[str]
) -> Project:
    """
    Updates the status of a project in MongoDB.

    Args:
        project_name (str): Name of the project to update
        raw_args (list[str]): List of command line arguments to parse

    Returns:
        Project: Updated project object with new status, logs and timestamps

    Raises:
        ValueError: If status argument is not one of: running, finished, failed
    """

    # Add argument parser
    parser = argparse.ArgumentParser(description='Update project run status')
    parser.add_argument('--status', required=True, help='Current run status')
    parser.add_argument('--logs', default='', help='List of log messages')
    parser.add_argument('--command', help='Last run command')

    args = parser.parse_args()

    # check args
    if args.status not in ['running', 'finished', 'failed']:
        raise ValueError('Invalid status')

    print(f"Updating UPC_Core status to '{args.status}' with {len(args.logs.split('\n'))} logs and command: '{args.command or 'None'}'")

    current_run_status = args.status
    logs = args.logs
    last_run_command = args.command

    client = MongoDBClient()
    return client.update_project_status(
        project_name=project_name,
        current_run_status=current_run_status,
        last_run_date=datetime.now(),
        logs=logs,
        last_run_command=last_run_command
    ) 