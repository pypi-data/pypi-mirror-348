import os
import re


def sanitize_file_name(file_name):
    # 清理文件名中的非法字符（使用正则表达式移除非法字符（包括换行符、制表符等）
    # sanitized_name = re.sub(r'[<>:"/\\|?*\r\n]', '_', file_name)
    sanitized_name = re.sub(r'[<>:"|?*\r\n]', '_', file_name)
    return sanitized_name.strip()  # 去掉首尾的空白字符


def clear_str(file_name):
    sanitized_name = re.sub(r'[<>:"|?*\r\n\s「」\[\]]', '', file_name)
    return sanitized_name.strip()


# 确保目标目录存在，如果不存在则创建。
def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not directory:
        return

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)  # 递归创建目录
            print(f"目录已创建: {directory}")
        except Exception as e:
            print(f"创建目录时发生错误: {e}")


def handle_file_operation(file_path, content, mode):
    try:
        ensure_directory_exists(file_path)  # 确保目录存在
        with open(sanitize_file_name(file_path), mode, encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        operation = "保存" if mode == "w" else "追加"
        print(f"\n\n{operation}文件时发生错误：{e}")


def write_to_file(file_path, content):
    handle_file_operation(file_path, content, "w")


def append_to_file(file_path, content):
    handle_file_operation(file_path, content, "a")
