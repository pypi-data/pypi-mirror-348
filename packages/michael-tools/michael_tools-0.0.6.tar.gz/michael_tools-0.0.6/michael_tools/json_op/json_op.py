import json


# dumps 是俗人，将 dict，转为 str（野蛮的）
def dict_to_str(python_obj):
    return json.dumps(python_obj, ensure_ascii=False, indent=4)


# loads 是优雅的，将野蛮的 str，转为 dict，好处理
def str_to_dict(json_str):
    return json.loads(json_str)


def read_file_to_dict(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


def write_dict_to_file(python_obj, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(python_obj, f, ensure_ascii=False, indent=4)

# 删除 Json 对象
# del save_dir_json["dwd"]
