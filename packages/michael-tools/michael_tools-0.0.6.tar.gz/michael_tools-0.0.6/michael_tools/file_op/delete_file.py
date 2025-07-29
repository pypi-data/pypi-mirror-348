import os


def delete_file(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"文件 '{file_path}' 已成功删除。")
        except Exception as e:
            print(f"删除文件时发生错误：{e}")
    else:
        print(f"文件 '{file_path}' 不存在。")
