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
The `chat()` function allows you to pass in a small dataset and a user question. It then returns an answer from ChatGPT-4 based on the data and the cost of generating this answer. Additionally, the function creates a YAML file in the working directory, recording the date of the query, the question, and the cost.
The `send_email()` function can be used in scripts to send emails to specified addresses for various purposes such as exception reminders or periodic script reports.

#### Parameters
- `subject`: Your e-mail subject (Type: str).
- `body`: Your e-mail content (Type: str).
- `send_email_address`: E-mail address of the sender (Type: str).
- `send_email_password`: E-mail password of the sender (Type: str).
- `receive_email_address`: E-mail address of the receiver (Type: str).
- `smtp_address`: SMTP address of sender's e-mail (Type: str).
- `smtp_port`: SMTP port of sender's e-mail (Type: int).

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
