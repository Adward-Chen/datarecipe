import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
import glob
import os
from tqdm import tqdm
import chardet

def send_email(subject:str, body:str, send_email_address:str, send_email_password:str, receive_email_address:str, attachment_path=None, attachment_list=None, smtp_address='smtp.feishu.cn', smtp_port=465):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = send_email_address
    msg['To'] = receive_email_address
    msg['Subject'] = subject

    # Add body text
    msg.attach(MIMEText(body, 'plain'))
    if attachment_path is not None and attachment_list is not None:
        # Add multiple attachments
        attachment_paths = [os.path.join(attachment_path, attachment) for attachment in attachment_list]
        for each_path in attachment_paths:
            attachment_filename = each_path.split("/")[-1]
            with open(each_path, "rb") as f:
                attach = MIMEApplication(f.read(), Name=attachment_filename)
            attach['Content-Disposition'] = f'attachment; filename="{attachment_filename}"'
            msg.attach(attach)

    # Send the email
    with smtplib.SMTP_SSL(smtp_address, smtp_port) as server:
        server.login(send_email_address, send_email_password)
        server.sendmail(send_email_address, receive_email_address, msg.as_string())

def local_to_df(path, partial_file_name, skip_rows=0, keep_file_name=False, sheet_num=1, encoding='auto', sep=','):
    all_data = pd.DataFrame()

    # 获取匹配的文件列表，并为其添加进度条
    file_list = list(glob.glob(f"{path}/**/*{partial_file_name}*.*", recursive=True))
    
    for file_name in tqdm(file_list, desc="Processing Files"):
        _, file_extension = os.path.splitext(file_name)
        file_extension = file_extension[1:]  # remove the leading dot
        
        # 识别文件编码类型
        if encoding=='auto':
            with open(file_name, 'rb') as file:
                result = chardet.detect(file.read())
                encoding = result['encoding']
        
        if file_extension == "csv":
            file_data = pd.read_csv(file_name, encoding=encoding, skiprows=skip_rows, sep=sep)
        elif file_extension == "xlsx":
            file_data = pd.read_excel(file_name, sheet_name=sheet_num - 1, skiprows=skip_rows)
        else:
            continue  # Skip unsupported file types

        if keep_file_name:
            file_data["file_name"] = str(file_name)

        all_data = pd.concat([all_data, file_data])

    if all_data.empty:
        print("No matching file in the path or empty data found")
        return None
    return all_data

def df_to_xlsx(df, directory_path, file_name):
    os.makedirs(directory_path, exist_ok=True)
    file_name = f"{file_name}.xlsx" if not file_name.endswith('.xlsx') else file_name
    df.to_excel(os.path.join(directory_path, file_name), index=False)

def df_to_csv(df, directory_path, file_name):
    os.makedirs(directory_path, exist_ok=True)
    file_name = f"{file_name}.csv" if not file_name.endswith('.csv') else file_name
    df.to_csv(os.path.join(directory_path, file_name), index=False)