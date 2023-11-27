import smtplib
from email.mime.text import MIMEText
import pandas as pd
import glob
import os
from tqdm import tqdm

def send_email(subject: str, body: str, send_emial_address:str, send_emial_password:str, receive_email_address: str, smtp_address:str='smtp.feishu.cn', smtp_port:int=465):
    # For SMTP, the email and password
    PASSWORD = send_emial_password  # Password

    msg = MIMEText(body)
    msg['From'] = send_emial_address
    msg['To'] = receive_email_address
    msg['Subject'] = subject

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL(smtp_address, smtp_port) as server:  # Using SMTP_SSL to connect
        server.login(send_emial_address, PASSWORD)
        server.sendmail(send_emial_address, receive_email_address, msg.as_string())

def local_to_df(path, partial_file_name, keep_file_name=False, sheet_num=1):
    all_data = pd.DataFrame()

    # 获取匹配的文件列表，并为其添加进度条
    file_list = list(glob.glob(f"{path}/**/*{partial_file_name}*.*", recursive=True))
    
    for file_name in tqdm(file_list, desc="Processing Files"):
        _, file_extension = os.path.splitext(file_name)
        file_extension = file_extension[1:]  # remove the leading dot

        if file_extension == "csv":
            file_data = pd.read_csv(file_name)
        elif file_extension == "xlsx":
            file_data = pd.read_excel(file_name, sheet_name=sheet_num - 1)
        else:
            continue  # Skip unsupported file types

        if keep_file_name:
            file_data["file_name"] = str(file_name)

        all_data = pd.concat([all_data, file_data])

    if all_data.empty:
        print("No matching file in the path")
        return None
    return all_data

def df_to_xlsx(df, directory_path, file_name):
    os.makedirs(directory_path, exist_ok=True)
    file_name = f"{file_name}.xlsx" if not file_name.endswith('.xlsx') else file_name
    df.to_excel(os.path.join(directory_path, file_name), index=False)
