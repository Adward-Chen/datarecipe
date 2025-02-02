import os
import yaml
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

def load_db_config(yaml_file_name: str, database: str, custom_path: Optional[str] = None) -> dict:
    """加载数据库配置"""
    file_path = os.path.join(custom_path, yaml_file_name) if custom_path else yaml_file_name
    with open(file_path, 'r') as stream:
        config = yaml.safe_load(stream)
    return config.get(database, {})

def connect_to_db(cfg: dict):
    """创建数据库连接"""
    try:
        url = URL.create(
            drivername='mysql+mysqldb',
            username=cfg['user'],
            password=cfg['password'],
            host=cfg['host'],
            port=cfg['port'],
            database=cfg['database']
        )
        engine = create_engine(url)
        return engine
    except KeyError as e:
        raise ValueError(f"配置中缺少必要的键：{e}")

def clean_dataframe(df: pd.DataFrame):
    """清理DataFrame中的无穷值"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        inf_values = df[numeric_cols].isin([np.inf, -np.inf]).any()
        cols_with_inf = inf_values[inf_values].index.tolist()
        if cols_with_inf:
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            print(f"警告：以下列包含无穷值，已替换为NaN：{cols_with_inf}")

def execute_sql(engine, sql_statement: str):
    """执行SQL语句"""
    try:
        with engine.begin() as conn:
            conn.execute(text(sql_statement))
    except Exception as e:
        raise ValueError(f"执行SQL时发生错误：{e}")

def update(
        raw_df: pd.DataFrame,
        database: str,
        table: str,
        yaml_file_name: str = 'cfg.yaml',
        clause: Optional[str] = None,
        date_col: Optional[str] = None,
        custom_path: Optional[str] = None
    ):
    try:
        df = raw_df.copy()
        if df.empty:
            raise ValueError("导入的数据集为空。")
        
        # 清理数据
        clean_dataframe(df)
        
        # 加载数据库配置
        cfg = load_db_config(yaml_file_name, database, custom_path)
        
        # 连接数据库
        engine = connect_to_db(cfg)
        
        # 测试写入一行数据
        test_df = df.iloc[[0]].copy()
        try:
            test_df.to_sql(table, engine, if_exists='append', index=False)
        except Exception as e:
            raise ValueError(f"测试写入数据失败，请检查数据格式：{str(e)}")
        
        # 如果指定了日期列，添加日期条件
        if date_col and date_col in df.columns:
            min_date = df[date_col].min()
            max_date = df[date_col].max()
            if clause:
                clause = f"{clause} AND {date_col} >= '{min_date}' AND {date_col} <= '{max_date}'"
            else:
                clause = f"{date_col} >= '{min_date}' AND {date_col} <= '{max_date}'"
        
        # 如果有条件子句，先删除符合条件的数据
        if clause:
            delete_sql = f"DELETE FROM {table} WHERE {clause}"
            execute_sql(engine, delete_sql)
        
        # 将数据写入数据库
        df.to_sql(table, engine, if_exists='append', index=False)
        
        print(f"成功更新 {len(df)} 条记录到 {database}.{table}")
        
    except Exception as e:
        raise Exception(f"更新数据时发生错误：{str(e)}")
