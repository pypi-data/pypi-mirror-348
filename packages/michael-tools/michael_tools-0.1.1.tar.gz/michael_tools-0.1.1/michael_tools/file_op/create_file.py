import os

# 创建的目录位置：当前工作目录
def create_file(file_path):
    if os.path.exists(file_path):
        print(f"文件 '{file_path}' 已存在。")
    else:
        with open(file_path, 'w') as file:
            pass  # 创建一个空文件
        print(f"文件 '{file_path}' 创建成功。")