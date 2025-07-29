import os

def create_file(filename):
    if os.path.exists(filename):
        print(f"文件 '{filename}' 已存在。")
    else:
        with open(filename, 'w') as file:
            pass  # 创建一个空文件
        print(f"文件 '{filename}' 创建成功。")