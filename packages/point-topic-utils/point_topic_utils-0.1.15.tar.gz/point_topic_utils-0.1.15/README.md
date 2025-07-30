# point-topic-utils

A utility package for centralizing shared logic across Point Topic DBT projects, focused on managing project run status in MongoDB, Google Sheets export, and secure configuration management.

**Note:** This package is primarily intended for internal use within Point Topic to standardize and simplify project status tracking and configuration. While it is installable from PyPI, it is not intended for general public use.

## Features

- **MongoDB Project Status Management**: Update and track project run status, last run date, logs, and last run command in the `OversightProjects` collection. Maintains a history of previous runs.
- **Google Sheets to CSV Export**: Export one or more Google Sheets worksheets to CSV files, with CLI and Python API support.
- **AWS Secrets Manager Integration**: Securely fetch MongoDB and Google credentials from AWS Secrets Manager.
- **Centralized Config Management**: Easy configuration for MongoDB connection and collection.
- **Structured Project Data Model**: Use of a `Project` dataclass for consistent project status data.
- **Command Line Interface**: Direct command-line tools for updating project status and exporting Google Sheets.

## Installation

```bash
pip install point-topic-utils
```

## Usage

### Command Line Interface

#### Update Project Status

```bash
pt-update-status --project-name "UPC_Core" --status "running" --command "dbt run"
```

#### Export Google Sheets to CSV

**Single worksheet:**

```bash
pt-export-gsheet --worksheet-key <SHEET_KEY> --worksheet-name <WORKSHEET_NAME> --output-path <CSV_PATH>
```

**Multiple worksheets:**

```bash
pt-export-gsheet --worksheet-key <SHEET_KEY> --multi --worksheet-configs '[{"name": "Sheet1", "output_path": "out1.csv"}, {"name": "Sheet2", "output_path": "out2.csv"}]'
```

Common options:

- `--worksheet-key`: (Required) Google Sheet key/ID
- `--worksheet-name`: (Required for single export) Worksheet name
- `--output-path`: (Required for single export) CSV output path
- `--multi`: Use for multiple worksheet export
- `--worksheet-configs`: (Required for multi) JSON list of worksheet configs
- `--credentials-secret-name`: (Optional) Secret name for Google credentials (default: `google_sheets_api_key`)

### Python API

#### Update Project Status

```python
from point_topic_utils import update_status

update_status(
    project_name="UPC_Core",
    status="running",
    logs="Started run...",
    command="dbt run"
)
```

#### Export Google Sheets to CSV

```python
from point_topic_utils import export_worksheet_to_csv, export_worksheets_to_csv

# Single worksheet
export_worksheet_to_csv(
    worksheet_key="1mosBg3CkIgRQyGNcAP5wTthyEy7Quh47ej3K8lckJCg",
    worksheet_name="operator_meta",
    output_path="seeds/operator_meta.csv"
)

# Multiple worksheets
export_worksheets_to_csv(
    worksheet_key="1mosBg3CkIgRQyGNcAP5wTthyEy7Quh47ej3K8lckJCg",
    worksheet_configs=[
        {"name": "operator_meta", "output_path": "seeds/operator_meta.csv"},
        {"name": "other_sheet", "output_path": "seeds/other_sheet.csv"}
    ]
)
```

## Configuration

- MongoDB credentials are fetched from AWS Secrets Manager (see `get_secrets.py`).
- Google Sheets credentials are fetched from AWS Secrets Manager (see `get_secrets.py`).
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
