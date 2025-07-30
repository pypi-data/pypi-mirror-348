def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()  # 读取文件的所有内容
    except FileNotFoundError:
        print("文件 '%s' 未找到，请检查文件路径是否正确。" % file_path)
        return None
    except Exception as e:
        print(f"发生错误：{e}")
        return None
