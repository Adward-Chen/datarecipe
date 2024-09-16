import os
import yaml
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import ResourceClosedError

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
    """更新数据库表中的数据"""
    try:
        df = raw_df.copy()
        if df.empty:
            raise ValueError("导入的数据集为空。")

        cfg = load_db_config(yaml_file_name, database, custom_path)
        engine = connect_to_db(cfg)
        clean_dataframe(df)

        if clause or date_col:
            # 删除满足条件的数据
            conditions = []
            if clause:
                conditions.append(clause)
            if date_col:
                start_date, end_date = df[date_col].min(), df[date_col].max()
                conditions.append(f"{date_col} BETWEEN '{start_date}' AND '{end_date}'")
            delete_sql = f"DELETE FROM {table} WHERE {' AND '.join(conditions)}"
            execute_sql(engine, delete_sql)

        # 使用chunksize参数上传数据
        df.to_sql(table, engine, if_exists='append', index=False, chunksize=1000, method='multi')
        print_action_result(table, "更新", df, date_col)

    except Exception as e:
        raise ValueError(f"更新过程发生错误：{e}")

def print_action_result(table: str, action: str, df: pd.DataFrame, df_date_col: Optional[str] = None):
    """打印操作结果"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    if df_date_col:
        date_range = f"{df[df_date_col].min()} 至 {df[df_date_col].max()}"
        print(f"{table} 数据已{action}：{current_time}\n数据日期范围：{date_range}")
    else:
        print(f"{table} 数据已{action}：{current_time}")

def sql_query(
        database: str,
        sql: str,
        yaml_file_name: str='cfg.yaml',
        custom_path: Optional[str] = None
    ) -> Optional[pd.DataFrame]:
    """执行SQL查询"""
    cfg = load_db_config(yaml_file_name, database, custom_path)
    engine = connect_to_db(cfg)
    try:
        if sql.strip().upper().startswith("SELECT"):
            df = pd.read_sql(sql, engine)
            return df
        else:
            execute_sql(engine, sql)
            print('操作完成。')
    except ResourceClosedError:
        print('查询完成，但没有返回任何数据。')
    except Exception as e:
        raise ValueError(f"执行SQL查询时发生错误：{e}")
