from datetime import datetime

from .db.mongodb import MongoDBClient
from .models.project import Project
from .get_secrets import get_secrets

import argparse

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

def main():
    """CLI entrypoint for updating project status"""
    import sys
    parser = argparse.ArgumentParser(description='Update project run status')
    parser.add_argument('--project-name', required=True, help='Name of the project to update')
    parser.add_argument('--status', required=True, help='Current run status')
    parser.add_argument('--command', help='Last run command')
    parser.add_argument('--logs', help='List of log messages')
    
    args = parser.parse_args()
    
    # Convert args to the format expected by update_status
    cmd_args = []
    if args.status:
        cmd_args.extend(['--status', args.status])
    if args.command:
        cmd_args.extend(['--command', args.command])
    if args.logs:
        cmd_args.extend(['--logs', args.logs])
    
    return update_status(
        project_name=args.project_name,
        raw_args=cmd_args
    )

if __name__ == '__main__':
    main() 