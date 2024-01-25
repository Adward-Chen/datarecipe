import numpy as np

def check_empty(df, columns=None, output_cols=None):
    if columns is not None and not isinstance(columns, list):
        columns = [columns]
    # 创建临时DataFrame
    tmp_df = df[columns].copy() if columns else df.copy()

    # 替换空白字符串和None为 np.nan
    tmp_df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    tmp_df.fillna(value=np.nan, inplace=True)

    # 计算每列的缺失值数量
    missing_counts = tmp_df.isnull().sum().sort_values(ascending=False)

    # 总行数
    total_rows = len(df)

    # 可视化缺失数据占比
    if missing_counts.any():
        print("缺失数据：")
        for col, count in missing_counts.items():
            num_chars = int((count / total_rows) * 10)  # 根据比例计算字符数量
            print(f"{col}: {'█' * num_chars}{'.' * (10 - num_chars)} ({count} rows)")
        null_data = df[tmp_df.isnull().any(axis=1)]
        if output_cols: 
            null_data = null_data[output_cols].drop_duplicates()
        return null_data
    else:
        print("DataFrame 数据完整。")