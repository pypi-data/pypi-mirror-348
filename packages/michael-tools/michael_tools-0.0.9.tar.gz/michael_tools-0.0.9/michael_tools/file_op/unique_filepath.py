import os

# 如果文件已存在，则自动在文件名后加 _1, _2 等，直到找到未使用的文件名。
def get_unique_filepath(file_name):
    if not os.path.exists(file_name):
        return file_name

    directory, filename = os.path.dirname(file_name), os.path.basename(file_name)
    name, ext = os.path.splitext(filename)
    counter = 1

    while True:
        new_filename = f"{name}_{counter}{ext}"
        new_filepath = os.path.join(directory, new_filename)
        if not os.path.exists(new_filepath):
            return new_filepath
        counter += 1