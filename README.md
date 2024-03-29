# datarecipe

## Introduction

`datarecipe` is an open-source package designed for data practitioners. It aims to provide comprehensive, robust, and user-friendly data tools.

## Dependencies

- `sqlalchemy`: ==1.4.16

## Functions

### 1. send_email()

#### Purpose
The `send_email()` function can be used in scripts to send emails to specified addresses for various purposes such as exception reminders or periodic script reports.

#### Parameters
- `subject`: Your e-mail subject (Type: String).
- `body`: Your e-mail content (Type: String).
- `send_email_address`: E-mail address of the sender (Type: String).
- `send_email_password`: E-mail password of the sender (Type: String).
- `receive_email_address`: E-mail address of the receiver (Type: String).
- `smtp_address`: SMTP address of sender's e-mail (Type: String).
- `smtp_port`: SMTP port of sender's e-mail (Type: Int).

#### Return Values
- None

#### Example
```python
datarecipe.send_email(
    subject='your_email_title', 
    body='your_email_content', 
    send_emial_address='sender_emial_address', 
    send_emial_password='sender_emial_password',
    receive_email_address='your_email_address'
)
```
---
### 2. update_data()

#### Purpose
The `update_data()` function allows for both overwriting and incremental updates of data within the MySQL database.

#### Parameters
- `raw_df`: Dataframe added to database (Type: DataFrame).
- `yaml_file_name`: Yaml file containing database information (Type: String).
- `database`: The name of database set in yaml file (Type: String).
- `table`: Updated table (Type: String).
- `add_data`: True for incremental update and False for overwriting (Type: Bool).
- `df_date_col`: Column name of date value for dataframe (Type: String).
- `db_date_col`: Column name of date value for database table (Type: String).
- `custom_path`: None for working directory or specific cfg file directory (Type: String).

#### Return Values
- None

#### Example

Example of yaml_file:
```yaml
database_1:
  user: your_database_user
  password: your_database_password
  host: your_database_host
  database: your_database_name
  port: 3306
```

Example of function:
```python
datarecipe.update_data(
    raw_df=df,
    yaml_file_name="cfg.yaml",
    database="database_1",
    table="updated_table_in_database",
    add_data=False, 
    df_date_col='date', 
    db_date_col='date',
    custom_path=r"C:\Users\Administrator"
)
```
---
### 3. local_to_df()

#### Purpose
Read local csv or excel files, support automatic encoding type recognition and files combination.

#### Return Values
- Dataframe

#### Example
```python
df = datarecipe.local_to_df(
    path = "absolute or relative path to the files directory",
    partial_file_name = "part of files' name",
    skip_rows = 0,
    keep_file_name = False,
    sheet_num = 1,
    encoding = 'auto',
    sep=','
)
```
---
### 4. df_to_xlsx()

#### Purpose
Export df to excel file

#### Return Values
- None

#### Example
```python
datarecipe.df_to_xlsx(
    df,
    directory_path = "directory to save df",
    file_name = "excel file name"
)
```
---
### 5. df_to_csv()

#### Purpose
Export df to csv file

#### Return Values
- None
  
#### Example
```python
datarecipe.df_to_csv(
    df,
    directory_path = "directory to save df",
    file_name = "csv file name"
)
```
---
### 6. check_empty()

#### Purpose
Check whether there are space string, None or np.nan value in df, return data summary and visualization of these missing value.

#### Return Values
- Missing Value found: missing value df
- No missing Value found: text printed
  
#### Example
```python
missing_df = datarecipe.check_empty(
    df,
    columns = "List of specific columns to check or None for all columns",
    output_cols = "List of specific columns or None for all columns"
    )
```
---
### 7. clear_db()

#### Purpose
Clear data from a table in MySQL database

#### Return Values
- None
  
#### Example
```python
datarecipe.clear_db(
    yaml_file_name = "cfg.yaml",
    database = "database name",
    table = "table name",
    custom_path= "None for working directory or specific cfg file directory"
)
```
---
### 8. fetch_table_data()

#### Purpose
Load table in MySQL database into Dataframe. Same as SQL "Select * from table".

#### Return Values
- Dataframe
  
#### Example
```python
datarecipe.clear_db( 
    yaml_file_name = "cfg.yaml",
    database = "database name",
    table = "table name",
    date_col = "None or date column name in table",
    start_date = "None or start date of data",
    end_date =  "None or end date of data", 
    custom_path= "None for working directory or specific cfg file directory"
)
```
---
### 9. sql_query()

#### Purpose
Run sql in python, support addition, deletion, modification and query.

#### Return Values
- DataFrame
- None

#### Example
```python
datarecipe.sql_query(yaml_file_name, database, sql, custom_path=None
    yaml_file_name = "cfg.yaml",
    database = "database name",
    sql = "Select * from table_name"
    custom_path= "None for working directory or specific cfg file directory"
)
```
---
