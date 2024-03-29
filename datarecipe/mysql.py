import numpy as np
# sqlalchemy ==1.4.16
from sqlalchemy import create_engine
from typing import Optional
import yaml
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import os
from sqlalchemy.exc import ResourceClosedError


def load_db_config(yaml_file_name, database, custom_path=None):
    file_path = os.path.join(custom_path, yaml_file_name) if custom_path else yaml_file_name
    with open(file_path, 'r') as stream:
        config = yaml.safe_load(stream)
    return config[database]


def connect_to_db(cfg):
    return create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s:%s/%s") % 
                         (cfg['user'], cfg['password'], cfg['host'], cfg['port'], cfg['database']))

def clean_dataframe(df):
    for col in df.columns:
        # 检查列是否为数值型
        if pd.api.types.is_numeric_dtype(df[col]):
            # 如果是数值型列，检查是否包含无穷值
            if np.isinf(df[col]).any():
                df[col].replace([np.inf, -np.inf], np.nan, inplace=True)
                print(f"Warning: Column '{col}' contains infinite values, they have been changed to NaN.")

def execute_sql(engine, sql_statement):
    with engine.connect() as conn:
        conn.execute(sql_statement)

def update_data(raw_df, yaml_file_name, database, 
                table, 
                add_data = False, 
                df_date_col: Optional[str] = None, 
                db_date_col: Optional[str] = None,
                custom_path=None):
    try:
        df = raw_df.copy()
        cfg = load_db_config(yaml_file_name, database, custom_path)
        engine = connect_to_db(cfg)
        
        if df.shape[0] == 0:
            raise ValueError("Imported dataset is empty.")
        
        clean_dataframe(df)

        chunk_size = 1000  # 每次上传的数据量
        num_chunks = (len(df) - 1) // chunk_size + 1

        if add_data:
            for i in tqdm(range(num_chunks), desc="Adding Data"):
                start_idx = i * chunk_size
                end_idx = start_idx + chunk_size
                df.iloc[start_idx:end_idx].to_sql(table, engine, if_exists='append', index=False)
            print_action_result(table, "added", df, df_date_col)
        else:
            start_date= min(df[df_date_col])
            end_date = max(df[df_date_col])
            df.iloc[0:1].to_sql(table, engine, if_exists='append', index=False)
            delete_sql = f"DELETE FROM {table} WHERE {db_date_col} BETWEEN '{start_date}' AND '{end_date}'"
            execute_sql(engine, delete_sql)
            for i in tqdm(range(num_chunks), desc="Updating Data"):
                start_idx = i * chunk_size
                end_idx = start_idx + chunk_size
                df.iloc[start_idx:end_idx].to_sql(table, engine, if_exists='append', index=False)
            print_action_result(table, "updated", df, df_date_col)
    except Exception as e:
        raise ValueError(f"{e}")

def print_action_result(table, action, df, df_date_col):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    if df_date_col:
        date_range = f"{df[df_date_col].min()} to {df[df_date_col].max()}"
        print(f"{table} data has been {action}: {current_time}\nData date range: {date_range}")
    else:
        print(f"{table} data has been {action}: {current_time}")

def clear_db(yaml_file_name, database, table, custom_path=None):
    cfg = load_db_config(yaml_file_name, database, custom_path)
    engine = connect_to_db(cfg)
    delete_sql = f"DELETE FROM {table}"
    execute_sql(engine, delete_sql)

def fetch_table_data(yaml_file_name, database, table, date_col=None, start_date=None, end_date=None, custom_path=None):
    cfg = load_db_config(yaml_file_name, database, custom_path)
    engine = connect_to_db(cfg)
    if date_col:
        sql = f"SELECT * FROM {table} WHERE {date_col} BETWEEN '{start_date}' AND '{end_date}'"
    else:
        sql = f"SELECT * FROM {table} "
    df = pd.read_sql(sql, engine)
    return df

def sql_query(yaml_file_name, database, sql, custom_path=None):
    cfg = load_db_config(yaml_file_name, database, custom_path)
    engine = connect_to_db(cfg)
    if sql.strip().upper().startswith("SELECT"):
        # 若为查询语句，执行查询操作并返回DataFrame
        try:
            df = pd.read_sql(sql, engine)
            return df
        except ResourceClosedError:
            print('查询完成，但没有返回任何数据。')
    else:
        # 执行非查询操作
        execute_sql(engine, sql)
        print('操作完成。')
            