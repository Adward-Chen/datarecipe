import requests
import json
import os
import time
import gzip
from io import BytesIO
import yaml
import pymysql
import inspect
import concurrent.futures
import pandas as pd
pymysql.install_as_MySQLdb()

def get_credentials(config_name='cfg.yaml'):
    """
    从配置文件读取Amazon Ads API凭证
    
    参数:
    - config_name: 配置文件名，默认为'cfg.yaml'
    """
    try:
        config_path = os.path.join(os.getcwd(), config_name)
        with open(config_path) as f:
            config = yaml.safe_load(f).get('api_vc', {})
            
        return (
            config.get('client_id'),
            config.get('client_secret'),
            config.get('refresh_token'),
        )
    except (FileNotFoundError, yaml.YAMLError) as e:
        raise Exception(f"Error when reading config file: {e}")
    except KeyError as e:
        raise Exception(f"config.yaml does not have : {e}")
    
def get_access_token(refresh_token, client_id, client_secret, max_wait_seconds=300):
    """
    获取Amazon SP-API的访问令牌，失败时进行等待时间递增重试
    
    参数:
    - refresh_token: 刷新令牌
    - client_id: 客户端ID
    - client_secret: 客户端密钥
    - max_wait_seconds: 最大等待时间(秒)，默认5分钟
    
    返回:
    - 成功时返回access_token，失败时抛出异常
    """
    url = "https://api.amazon.com/auth/o2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    
    total_wait = 0
    attempt = 0
    base_wait = 2  # 基础等待时间2秒
    
    while total_wait < max_wait_seconds:
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            return response.json().get("access_token")
            
        except requests.exceptions.RequestException as e:
            wait_time = min(base_wait * (2 ** attempt), max_wait_seconds - total_wait)
            if wait_time <= 0:
                break
                
            print(f"获取访问令牌失败 (已等待 {total_wait} 秒): {str(e)}")
            print(f"等待 {wait_time} 秒后重试...")
            
            time.sleep(wait_time)
            total_wait += wait_time
            attempt += 1
    
    raise Exception(f"获取访问令牌失败，已等待 {total_wait} 秒")

def get_report_id(access_token, report_request_body, max_wait_seconds=300):
    """
    请求创建报告并获取报告ID，失败时进行重试
    
    参数:
    - access_token: API访问令牌
    - report_request_body: 报告请求体
    - max_wait_seconds: 最大等待时间(秒)，默认5分钟
    
    返回:
    - 成功时返回report_id，失败时返回None
    """
    url = "https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/reports"
    headers = {
        "Content-Type": "application/json",
        "x-amz-access-token": access_token,
    }
    
    total_wait = 0
    attempt = 0
    base_wait = 2  # 基础等待时间2秒
    
    while total_wait < max_wait_seconds:
        try:
            response = requests.post(url, headers=headers, json=report_request_body)
            response_data = response.json()
            
            if response.status_code == 202:
                print(f"报告请求已成功提交。正在等待报告生成...")
                return response_data.get("reportId")
                
            wait_time = min(base_wait * (2 ** attempt), max_wait_seconds - total_wait)
            if wait_time <= 0:
                break
                
            print(f"创建报告失败 (已等待 {total_wait} 秒). 状态码: {response.status_code}")
            print(f"等待 {wait_time} 秒后重试...")
            
            time.sleep(wait_time)
            total_wait += wait_time
            attempt += 1
            
        except Exception as e:
            print(f"请求异常: {str(e)}")
            wait_time = min(base_wait * (2 ** attempt), max_wait_seconds - total_wait)
            if wait_time <= 0:
                break
                
            print(f"等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
            total_wait += wait_time
            attempt += 1
            
    print(f"获取报告ID失败，已等待 {total_wait} 秒")
    return None

def check_report_status(access_token, report_id, max_wait_seconds=300):
    """
    检查报告生成状态，使用重试机制
    
    参数:
    - access_token: API访问令牌
    - report_id: 报告ID
    - max_wait_seconds: 最大等待时间(秒)，默认5分钟
    
    返回:
    - 成功时返回状态响应，失败时返回None
    """
    url = f"https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/reports/{report_id}"
    headers = {
        "x-amz-access-token": access_token,
    }
    
    total_wait = 0
    attempt = 0
    base_wait = 2  # 基础等待时间2秒
    
    print(f'报告正在生成中，请等待...')
    while total_wait < max_wait_seconds:
        status_response = requests.get(url, headers=headers)
        
        if status_response.status_code == 200:
            report_status = status_response.json().get("processingStatus")
            print(f'当前报告状态：{report_status} (已等待 {total_wait} 秒)')

            if report_status == 'DONE':
                report_document_id = status_response.json().get("reportDocumentId")
                print(f'报告已生成!')
                print(f"Report Document ID: {report_document_id}")
                return status_response
            
        wait_time = min(base_wait * (2 ** attempt), max_wait_seconds - total_wait)
        if wait_time <= 0:
            break
            
        print(f"等待 {wait_time} 秒后重试...")
        time.sleep(wait_time)
        total_wait += wait_time
        attempt += 1
            
    print(f'报告生成超时，已等待 {total_wait} 秒')
    return None

def download_and_process_report(access_token, report_document_id):
    """
    使用 report_document_id 下载报告数据，解压缩并解析为 JSON 格式。
    
    :param access_token: API 访问令牌
    :param report_document_id: 用于下载报告的 document ID
    :return: 解析后的 JSON 数据，如果失败则返回 None
    """

    url = f"https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/documents/{report_document_id}"
    headers = {
        "x-amz-access-token": access_token,
        'compressionAlgorithm': 'GZIP'

    }
    # 发起请求以获取下载 URL
    report_response = requests.get(url, headers=headers)
    if report_response.status_code == 200:
        # 获取下载 URL
        download_url = report_response.json().get("url")

        # 检查是否成功获取到下载链接
        if not download_url:
            print(f"Error: No download URL found in the response.")
            return None

        # 下载 URL 获取报告内容, stream=True 流式下载 减少内存占用
        response = requests.get(download_url, stream=True)

        # 检查响应状态是否成功
        if response.status_code == 200:
            try:
                # 解压缩报告数据并解析为 JSON 格式
                with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
                    json_data = json.load(gz)
                    print(f"报告数据已下载并解析为 JSON 格式")
                    return json_data
            except Exception as e:
                print(f"Error: Failed to parse report data as JSON: {e}")
                return None
        else:
            print(f'Error: 已获取报告下载链接，但无法下载报告数据，状态码：{response.status_code}')
            return None

    else:
        print(f'Error: 无法获取报告下载链接，状态码：{report_response.status_code}')
        return None

def process_json_to_df(json_data):
    """
    将JSON格式的报告数据转换为DataFrame
    
    参数:
    - json_data: JSON格式的报告数据
    
    返回:
    - pandas DataFrame
    """
    try:
        if not json_data:
            return None
            
        # 直接将JSON数据转换为DataFrame
        df = pd.json_normalize(json_data)
        return df
            
    except Exception as e:
        print(f"处理报告数据时发生错误: {str(e)}")
        return None

def process_single_report(access_token, request, max_wait_seconds=300):
    """
    处理单个报告的完整流程
    
    参数:
    - access_token: API访问令牌
    - request: 报告请求信息
    - max_wait_seconds: 最大等待时间(秒)
    
    返回:
    - 元组 (报告名称, 结果字典)
    """
    report_name = request["name"]
    report_body = request["body"]
    
    print(f"\n开始获取 {report_name} 报告...")
    
    result = {
        "data": None,
        "status": "failed",
        "message": ""
    }
    
    # 1. 创建报告请求
    report_id = get_report_id(access_token, report_body, max_wait_seconds)
    if not report_id:
        result["message"] = "获取报告ID失败"
        print(f"{result['message']}")
        return report_name, result
        
    # 2. 检查报告状态并获取 document ID
    status_response = check_report_status(access_token, report_id, max_wait_seconds)
    if not status_response:
        result["message"] = "获取报告状态失败"
        print(f"{result['message']}")
        return report_name, result
        
    report_document_id = status_response.json().get("reportDocumentId")
    if not report_document_id:
        result["message"] = "未找到报告文档ID"
        print(f"{result['message']}")
        return report_name, result
        
    # 3. 下载并处理报告
    json_data = download_and_process_report(access_token, report_document_id)
    if json_data:
        # 4. 转换为DataFrame
        df = process_json_to_df(json_data)
        if df is not None and not df.empty:
            result["data"] = df
            result["status"] = "success"
            result["message"] = "报告获取成功"
            return report_name, result
        else:
            result["message"] = "处理报告数据失败或数据为空"
            print(f"{result['message']}")
            return report_name, result
    else:
        result["message"] = "获取报告数据失败"
        print(f"{result['message']}")
        return report_name, result

def fetch_sp_api_reports(report_requests, max_wait_seconds=300, max_workers=3):
    """
    集成获取认证和请求报告的完整流程，使用并发处理多个报告请求，支持单个或多个报告请求
    
    参数:
    - report_requests: 列表或字典，包含报告请求信息。格式为:
        单个请求: {
            "name": "报告名称",
            "body": {
                "reportType": "报告类型",
                "reportOptions": {
                    // 报告选项
                },
                "marketplaceIds": ["市场ID"]    # 美国: ["ATVPDKIKX0DER"]
            }
        }
        多个请求: [请求1, 请求2, ...]
    - max_wait_seconds: 最大等待时间(秒)，默认5分钟
    - max_workers: 最大并发工作线程数，默认3
    
    返回:
    - 元组 (results, all_success)
      results: 字典，键为报告名称，值为包含以下字段的字典:
        - data: DataFrame格式的报告数据
        - status: 'success' 或 'failed'
        - message: 状态消息
      all_success: 布尔值，表示是否所有报告都成功获取
    """
    try:
        # 确保report_requests是列表格式
        if isinstance(report_requests, dict):
            report_requests = [report_requests]
            
        # 1. 获取认证信息
        client_id, client_secret, refresh_token = get_credentials()
        
        # 2. 获取访问令牌
        access_token = get_access_token(refresh_token, client_id, client_secret, max_wait_seconds)
        
        results = {}
        all_success = True
        
        # 3. 使用线程池并发处理报告请求
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_report = {
                executor.submit(process_single_report, access_token, request, max_wait_seconds): request["name"]
                for request in report_requests
            }
            
            # 获取结果
            for future in concurrent.futures.as_completed(future_to_report):
                report_name = future_to_report[future]
                try:
                    name, result = future.result()
                    results[name] = result
                    if result["status"] != "success":
                        all_success = False
                except Exception as e:
                    error_result = {
                        "data": None,
                        "status": "failed",
                        "message": f"处理报告时发生错误: {str(e)}"
                    }
                    results[report_name] = error_result
                    all_success = False
                    print(f"{error_result['message']}")
                
        return results, all_success
            
    except Exception as e:
        error_message = f"获取报告过程中发生错误: {str(e)}"
        print(f"{error_message}")
        return None, False

# # 使用示例
# # 设置起止时间 (年月日时分秒)
# start_time = "2024-09-01T00:00:00Z"
# end_time = "2024-09-02T00:00:00Z"

# # 定义报告请求体
# report_requests = [
#     {
#         "name": "daily_sales",
#         "body": {
#             "reportType": "GET_VENDOR_SALES_REPORT",
#             "reportOptions": {
#             "distributorView": "MANUFACTURING",
#             "reportPeriod": "DAY",
#             "sellingProgram": "RETAIL"
#             },
#             "dataStartTime": start_time,
#             "dataEndTime": end_time,
#             "marketplaceIds": [
#             "ATVPDKIKX0DER"
#             ]
#         }
#     },
#     {
#         "name": "promotion",
#         "body": {
#             "reportType": 'GET_PROMOTION_PERFORMANCE_REPORT',
#             "reportOptions": {
#                 "promotionStartDateFrom": start_time,
#                 "promotionStartDateTo": end_time
#             },
#             "marketplaceIds": ["ATVPDKIKX0DER"]
#         }
#     },
#     {
#         "name": "coupon",
#         "body": {
#             "reportType": 'GET_COUPON_PERFORMANCE_REPORT',
#             "reportOptions": {
#                 "campaignStartDateFrom": start_time,
#                 "campaignStartDateTo": end_time
#             },
#             "marketplaceIds": ["ATVPDKIKX0DER"]
#         }
#     }
# ]

# # 获取报告数据
# results, all_success = s3_api.fetch_sp_api_reports(report_requests)