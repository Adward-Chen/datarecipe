
# DataRecipe

## Table of Contents 目录
1. [Overview 概览](#overview)
2. [Functions 功能](#functions)
   - [General Features 通用功能](#general-features)
     - [send_email 发送邮件](#send_email)
   - [Data Validation and Cleaning 数据检验与清洗](#data-validation-and-cleaning)
     - [check_empty 检查空值](#check_empty)
     - [clean_dataframe 清理数据框](#clean_dataframe)
   - [Data Import/Export 数据导入/导出](#data-importexport)
     - [local_to_df 本地到数据框](#local_to_df)
     - [df_to_xlsx DataFrame到Excel](#df_to_xlsx)
     - [df_to_csv DataFrame到CSV](#df_to_csv)
   - [Database Operations 数据库操作](#database-operations)
     - [update 更新](#update)
     - [sql_query SQL查询](#sql_query)
3. [Contact Information 联系信息](#contact-information)

## Overview 概览
This toolkit provides a variety of Python functions to facilitate common data manipulation, data import/export, and database operations. 

此工具包提供多种Python函数，以方便常见的数据操作、数据导入/导出和数据库操作。

## Functions 功能

### General Features 通用功能
#### send_email 发送邮件
Sends an email using SMTP with SSL/TLS options.
使用SMTP的SSL/TLS选项发送邮件。
- **Parameters 参数**:
  - `subject`: Email subject as a string 邮件主题。
  - `body`: Main content of the email 邮件正文。
  - `send_email_address`: Sender's email address 发件人邮箱地址。
  - `send_email_password`: Sender's email password for SMTP authentication SMTP认证的发件人邮箱密码。
  - `receive_email_address`: Recipient's email address 收件人邮箱地址。
  - `smtp_address`: SMTP server address (default: 'smtp.feishu.cn') SMTP服务器地址（默认为 'smtp.feishu.cn'）。
  - `smtp_port`: SMTP server port (default: 465) SMTP服务器端口（默认为465）。
  - `type`: 'SSL' or 'TLS' connection type 连接类型 'SSL' 或 'TLS'。

**Example with SSL 使用SSL的例子:**
```python
send_email("Test", "Hello, this is a test email.", "sender@example.com", "password123", "receiver@example.com")
```

**Example with TLS 使用TLS的例子:**
```python
send_email("Test", "Hello, this is a test email.", "sender@example.com", "password123", "receiver@example.com", smtp_address="smtp.gmail.com", smtp_port=587, type='TLS')
```

### Data Validation and Cleaning 数据检验与清洗
#### check_empty 检查空值
Checks for empty entries in specified DataFrame columns.
检查指定DataFrame列中的空条目。
- **Parameters 参数**:
  - `df`: DataFrame to check 检查的DataFrame。
  - `columns`: Columns to check for missing values 检查缺失值的列。
  - `output_cols`: Columns to include in the output 输出中包含的列。

**Example 示例:**
```python
empty_data = check_empty(df, columns=["name", "email"])
```

#### clean_dataframe 清理数据框
Cleans DataFrame by replacing infinite values with NaN.
通过替换无穷大值为NaN来清理DataFrame。
- **Parameters 参数**:
  - `df`: DataFrame to clean 需要清理的DataFrame。

**Example 示例:**
```python
clean_dataframe(df)
```

### Data Import/Export 数据导入/导出
#### local_to_df 本地到数据框
Converts files from a local directory to a pandas DataFrame.
将本地目录中的文件转换为pandas DataFrame。
- **Parameters 参数**:
  - `path`: Directory path to search for files 搜索文件的目录路径。
  - `partial_file_name`: File name pattern to match 匹配的文件名模式。
  - `skip_rows`: Number of rows to skip at the start of each file 每个文件开始跳过的行数。
  - `keep_file_name`: If True, adds a column with the file name 如果为True，则添加包含文件名的列。
  - `sheet_num`: For Excel files, specifies the sheet number to read 对于Excel文件，指定要读取的工作表号。
  - `encoding`: Character encoding of the files 文件的字符编码。

**Example with CSV files CSV文件的例子:**
```python
df = local_to_df("./data", "sample", keep_file_name=True)
```

**Example with Excel files Excel文件的例子:**
```python
df = local_to_df("./data", "report", sheet_num=2, encoding='utf-8')
```

#### df_to_xlsx DataFrame到Excel
Saves a DataFrame to an Excel file.
将DataFrame保存为Excel文件。
- **Parameters 参数**:
  - `df`: DataFrame to save 保存的DataFrame。
  - `directory_path`: Path to directory where the file will be saved 保存文件的目录路径。
  - `file_name`: Name of the output file 输出文件的名称。

**Example 示例:**
```python
df_to_xlsx(df, "./output", "output_data")
```

#### df_to_csv DataFrame到CSV
Saves a DataFrame to a CSV file.
将DataFrame保存为CSV文件。
- **Parameters 参数**:
  - `df`: DataFrame to save 保存的DataFrame。
  - `directory_path`: Path to directory where the file will be saved 保存文件的目录路径。
  - `file_name`: Name of the output file 输出文件的名称。

**Example 示例:**
```python
df_to_csv(df, "./output", "output_data")
```

### Database Operations 数据库操作
#### update 更新
Updates records in a database table based on conditions.
根据条件更新数据库表中的记录。
- **Parameters 参数**:
  - `raw_df`: DataFrame containing new data to update 包含要更新的新数据的DataFrame。
  - `database`: Database name 数据库名称。
  - `table`: Table name 表名。
  - `yaml_file_name`: YAML file name with DB configuration 带有DB配置的YAML文件名。
  - `clause`: SQL clause for record deletion 记录删除的SQL子句。
  - `date_col`: Column name containing date data 包含日期数据的列名。
  - `custom_path`: Path to directory containing the YAML file 包含YAML文件的目录路径。

**Example 示例:**
```python
update(df, "test_db", "user_data", clause="user_id > 10")
```

#### sql_query SQL查询
Executes a SELECT SQL query and returns a DataFrame.
执行SELECT SQL查询并返回一个DataFrame。
- **Parameters 参数**:
  - `database`: Database name 数据库名。
  - `sql`: SQL SELECT statement SQL SELECT语句。
  - `yaml_file_name`: YAML file name with DB configuration 带有DB配置的YAML文件名。
  - `custom_path`: Optional path to directory containing the YAML file 可选的包含YAML文件的目录路径。

**Example 示例:**
```python
result_df = sql_query("test_db", "SELECT * FROM users")
```

## Contact Information 联系信息
For any questions or suggestions regarding the toolkit, please contact us at:
如果您对工具包有任何疑问或建议，请通过以下方式联系我们：
- Email: HanfanC@outlook.com
- GitHub: [DataRecipe GitHub Repository](https://github.com/DataRecipe)
