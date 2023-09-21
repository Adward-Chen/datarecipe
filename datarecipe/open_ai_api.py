
import openai
import os
import pandas as pd
import yaml
from datetime import date

def model_list(api_key):
  openai.api_key = os.getenv(api_key)
  return pd.DataFrame(openai.Model.list())

def load_yaml(file_name="question_records.yaml"):
    try:
        with open(file_name, "r") as file:
            return yaml.safe_load(file) or []
    except FileNotFoundError:
        return []

def yaml_sum(yaml, col_name):
    return sum(entry[col_name] for entry in yaml)

def save_yaml(data, file_name="question_records.yaml"):
    with open(file_name, "w") as file:
        yaml.dump(data, file)

def chat(df, question, key, yaml_name="question_records.yaml", system='You are a data scientist assistant', cost = True, daily_cost_limit=10):
  # constraint dataframe size and cost
  records_yaml = load_yaml(file_name=yaml_name)
  current_cost = sum(record['cost'] for record in records_yaml if record['date'] == date.today())
  if current_cost >= daily_cost_limit:
    return "Today's question limit has been reached, please try again tomorrow or contact the data administrator to request an increase in the limit.", 0
  elif df.size > 200: 
    return 'Too much data, please reduce table size.', 0
  else:
    openai.api_key = key
    # convert df to json
    assistant_msg = df.to_json(orient='split')
    # Create an array of user and assistant messages
    user_assistant = [question, assistant_msg]
    assert isinstance(system, str), "`system` should be a string"
    assert isinstance(user_assistant, list), "`user_assistant` should be a list"
    system_msg = [{"role": "system", "content": system}]
    user_assistant_msgs = [
        {"role": "assistant", "content": user_assistant[i]} if i % 2 else {"role": "user", "content": user_assistant[i]}
        for i in range(len(user_assistant))]
    msgs = system_msg + user_assistant_msgs
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=msgs,
                                            temperature=0,
                                            max_tokens = 1000)
    status_code = response["choices"][0]["finish_reason"] # type: ignore
    assert status_code == "stop", f"The status code was {status_code}."
    question_cost = response["usage"]["completion_tokens"]/1000*0.004 + response["usage"]["prompt_tokens"]/1000*0.003 # type: ignore
    records_yaml.append({"date":date.today(), "question": question, "cost": question_cost})
    save_yaml(records_yaml, yaml_name)
    if cost:
      return response["choices"][0]["message"]["content"], question_cost # type: ignore
    else:
      return response["choices"][0]["message"]["content"], "output_token:" + str(response["usage"]["completion_tokens"]) + "input_token:" + str(response["usage"]["prompt_tokens"]) # type: ignore
