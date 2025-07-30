# point-topic-utils

A utility package for centralizing shared logic across Point Topic DBT projects, focused on managing project run status in MongoDB and secure configuration management.

**Note:** This package is primarily intended for internal use within Point Topic to standardize and simplify project status tracking and configuration. While it is installable from PyPI, it is not intended for general public use.

## Features

- **MongoDB Project Status Management**: Update and track project run status, last run date, logs, and last run command in the `OversightProjects` collection. Maintains a history of previous runs.
- **AWS Secrets Manager Integration**: Securely fetch MongoDB credentials from AWS Secrets Manager.
- **Centralized Config Management**: Easy configuration for MongoDB connection and collection.
- **Structured Project Data Model**: Use of a `Project` dataclass for consistent project status data.
- **Command Line Interface**: Direct command-line tool for updating project status without wrapper scripts.

## Installation

```bash
pip install point-topic-utils
```

## Usage

### Command Line Interface

The package provides a `pt-update-status` command for updating project status directly from the command line:

```bash
pt-update-status --project-name "UPC_Core" --status "running" --command "dbt run"
```

Available arguments:

- `--project-name`: (Required) Name of the project to update
- `--status`: (Required) Current run status (must be one of: running, finished, failed)
- `--logs`: (Optional) List of log messages
- `--command`: (Optional) Last run command

### Python API

```python
from point_topic_utils import update_status

# Example: update status from within a script
update_status(
    project_name="UPC_Core",
    raw_args=[
        "--status", "running",
        "--logs", "Started run...",
        "--command", "dbt run"
    ]
)
```

## Configuration

- MongoDB credentials are fetched from AWS Secrets Manager (see `get_secrets.py`).
- Default database: `research-app`, collection: `OversightProjects` (see `config.py`).

## AWS Authentication

This package uses `boto3` to access AWS Secrets Manager. **You do not need to pass AWS credentials as parameters.**

boto3 will automatically look for credentials in the following locations (in order):

1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, etc.)
2. AWS credentials file (usually `~/.aws/credentials`)
3. AWS config file (usually `~/.aws/config`)
4. IAM role (if running on AWS infrastructure like EC2, ECS, or Lambda)

As long as valid credentials are available in one of these locations, the package will authenticate successfully with AWS.

For more details, see the [boto3 credentials documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).

## Future Features

This package is under active development. More utilities and shared logic will be added as needed by Point Topic projects.

---

For internal use by Point Topic. For questions or contributions, contact the data team.
