# datarecipe

## Introduction

`datarecipe` is an open-source package designed for data practitioners. It aims to provide comprehensive, robust, and user-friendly data tools.

## Dependencies

- `sqlalchemy`: <2.0

## Functions

### chat()

#### Purpose
The `chat()` function allows you to pass in a small dataset and a user question. It then returns an answer from ChatGPT-4 based on the data and the cost of generating this answer. Additionally, the function creates a YAML file in the working directory, recording the date of the query, the question, and the cost.

#### Parameters
- `df`: The small dataset you want to analyze (Type: DataFrame).
- `question`: The question we want answered (Type: String).
- `key`: Your ChatGPT API key (Type: String).
- `yaml_name`: The file name of the yaml file (Type: String).
- `system`: The messages describe the behavior of the AI assistant (Type: String).
- `cost`: Whether to return the problem cost, True returns the problem cost, False returns the problem token number, default is True. (True/False).
- `daily_cost_limit`: Single-day question spending limit, default is 10 (Type: Number).

#### Return Values
- ChatGPT response (Type: String)
- question cost, in dollars (Type: Number).

#### Example
```python
# Initialize your question
user_question = "What is the average value in Column1?"

# Call the chat() function
response, cost = datarecipe.chat(df=df, question=user_question, key=your_api_key)

# Output the response and cost
print(response)
print(cost)
```
---
### send_email()

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
### update_data()

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
- `start_date`: Update date range (Type: String).
- `end_date`: Update date range (Type: String).

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
    start_date='2023-01-01', 
    end_date='2023-04-01'
)
```
