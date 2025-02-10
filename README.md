
# DataRecipe

## Table of Contents
1. [Overview](#overview)
2. [Functions](#functions)
   - [General Features](#general-features)
     - [send_email](#send_email)
   - [Data Validation and Cleaning](#data-validation-and-cleaning)
     - [check_empty](#check_empty)
     - [clean_dataframe](#clean_dataframe)
   - [Data Import/Export](#data-importexport)
     - [local_to_df](#local_to_df)
     - [df_to_xlsx](#df_to_xlsx)
     - [df_to_csv](#df_to_csv)
   - [Database Operations](#database-operations)
     - [update](#update)
     - [sql_query](#sql_query)
   - [API](#api)
     - [fetch_sp_api_reports](#fetch_sp_api_reports)
3. [Contact Information](#contact-information)

## Overview
This toolkit provides a variety of Python functions to facilitate common data manipulation, data import/export, and database operations.

## Functions

### General Features
#### send_email
Sends an email using SMTP with SSL/TLS options, supporting attachments if provided.
- **Parameters**:
  - `subject`: Email subject as a string.
  - `body`: Main content of the email.
  - `send_email_address`: Sender's email address.
  - `send_email_password`: Sender's email password for SMTP authentication.
  - `receive_email_address`: Recipient's email address.
  - `attachment_path`: Directory path where attachments are stored (optional).
  - `attachment_list`: List of filenames to be attached (optional).
  - `smtp_address`: SMTP server address (default: 'smtp.feishu.cn').
  - `smtp_port`: SMTP server port (default: 465).

**Example with Attachments:**
```python
send_email(
    "Meeting Documents", 
    "Please see attached documents for the upcoming meeting.", 
    "sender@example.com", 
    "password123", 
    "receiver@example.com", 
    attachment_path="/path/to/documents", 
    attachment_list=["agenda.pdf", "minutes.docx"]
)
```

### Data Validation and Cleaning
#### check_empty
Checks for empty entries in specified DataFrame columns.
- **Parameters**:
  - `df`: DataFrame to check.
  - `columns`: Columns to check for missing values.
  - `output_cols`: Columns to include in the output.

**Example:**
```python
empty_data = check_empty(df, columns=["name", "email"])
```

#### clean_dataframe
Cleans DataFrame by replacing infinite values with NaN.
- **Parameters**:
  - `df`: DataFrame to clean.

**Example:**
```python
clean_dataframe(df)
```

### Data Import/Export
#### local_to_df
Converts files from a local directory to a pandas DataFrame.
- **Parameters**:
  - `path`: Directory path to search for files.
  - `partial_file_name`: File name pattern to match.
  - `skip_rows`: Number of rows to skip at the start of each file.
  - `keep_file_name`: If True, adds a column with the file name.
  - `sheet_num`: For Excel files, specifies the sheet number to read.
  - `encoding`: Character encoding of the files.

**Example with CSV files:**
```python
df = local_to_df("./data", "sample", keep_file_name=True)
```

**Example with Excel files:**
```python
df = local_to_df("./data", "report", sheet_num=2, encoding='utf-8')
```

#### df_to_xlsx
Saves a DataFrame to an Excel file.
- **Parameters**:
  - `df`: DataFrame to save.
  - `directory_path`: Path to directory where the file will be saved.
  - `file_name`: Name of the output file.

**Example:**
```python
df_to_xlsx(df, "./output", "output_data")
```

#### df_to_csv
Saves a DataFrame to a CSV file.
- **Parameters**:
  - `df`: DataFrame to save.
  - `directory_path`: Path to directory where the file will be saved.
  - `file_name`: Name of the output file.

**Example:**
```python
df_to_csv(df, "./output", "output_data")
```

### Database Operations
#### update
Updates records in a database table based on conditions.
- **Parameters**:
  - `raw_df`: DataFrame containing new data to update.
  - `database`: Database name.
  - `table`: Table name.
  - `yaml_file_name`: YAML file name with DB configuration.
  - `clause`: SQL clause for record deletion.
  - `date_col`: Column name containing date data.
  - `custom_path`: Path to directory containing the YAML file.

**Example:**
```python
update(df, "test_db", "user_data", clause="user_id > 10")
```

#### sql_query
Executes a SELECT SQL query and returns a DataFrame.
- **Parameters**:
  - `database`: Database name.
  - `sql`: SQL SELECT statement.
  - `yaml_file_name`: YAML file name with DB configuration.
  - `custom_path`: Optional path to directory containing the YAML file.

**Example:**
```python
result_df = sql_query("test_db", "SELECT * FROM users")
```

### API
#### fetch_sp_api_reports
Fetches reports from Amazon Selling Partner API with concurrent processing support.
- **Parameters**:
  - `report_requests`: List or dictionary containing report request information.
  - `max_wait_seconds`: Maximum wait time in seconds (default: 300)
  - `max_workers`: Maximum number of concurrent worker threads (default: 3)
- **Returns**: Tuple containing:
  - `results`: Dictionary with report names as keys and report data/status as values
  - `all_success`: Boolean indicating if all reports were fetched successfully

**Example:**
```python
report_requests = [
    {
        "name": "daily_sales",
        "body": {
            "reportType": "GET_VENDOR_SALES_REPORT",
            "reportOptions": {
            "distributorView": "MANUFACTURING",
            "reportPeriod": "DAY",
            "sellingProgram": "RETAIL"
            },
            "dataStartTime": '2025-01-01',
            "dataEndTime": '2025-01-02',
            "marketplaceIds": [
            "ATVPDKIKX0DER"
            ]
        }
    }
]

results, all_success = fetch_sp_api_reports(report_requests)
```

## Contact Information
For any questions or suggestions regarding the toolkit, please contact us at:
- Email: HanfanC@outlook.com
- PyPI: [PyPI Project](https://pypi.org/project/datarecipe/)
