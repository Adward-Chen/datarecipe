# datarecipe

## Introduction

`datarecipe` is an open-source package designed for data practitioners. It aims to provide comprehensive, robust, and user-friendly data tools.

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
- ChatGPT-4 response (Type: String)
- question cost, in dollars (Type: Number).
