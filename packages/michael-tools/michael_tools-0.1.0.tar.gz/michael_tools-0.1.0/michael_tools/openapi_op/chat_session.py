import json
import os
import time
from datetime import datetime

from michael_tools.file_op.dir_op import path_join
from michael_tools.file_op.read_file import read_file
from michael_tools.file_op.write_file import write_to_file
from michael_tools.json_op.json_op import str_to_dict, dict_to_str
from michael_tools.openapi_op.call_model import create_client, process_non_stream_response, process_stream_response


# 多轮对话会话类，支持对话历史管理和存储
class ChatSession:
    def __init__(self, session_id=None, model_name="deepseek-r1"):
        self.model_name = model_name
        self.messages = []
        self.client = create_client()

        if session_id is None:
            self.session_id = f"chat_{datetime.now().strftime('%Y_%m_%d__%H%M%S')}"
        else:
            self.session_id = session_id

        self._load_session()

    def _get_session_file_path(self):
        history_dir = "chat_history"
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)
        return path_join(history_dir, f"{self.session_id}.json")

    def _load_session(self):
        file_path = self._get_session_file_path()
        content = read_file(file_path)
        if content:
            try:
                session_data = str_to_dict(content)
                self.messages = session_data.get("messages", [])
                self.model_name = session_data.get("model_name", self.model_name)
                print(f"已加载会话 {self.session_id}")
            except json.JSONDecodeError:
                print(f"会话文件 {file_path} 格式错误，将创建新会话")

    def _save_session(self):
        file_path = self._get_session_file_path()
        session_data = {
            "session_id": self.session_id,
            "model_name": self.model_name,
            "messages": self.messages,
            "last_updated": datetime.now().isoformat(sep=' ')
        }
        write_to_file(file_path, dict_to_str(session_data))

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        self._save_session()

    def send_message(self, message, show_process=True, stream=False):
        self.add_message("user", message)

        start_time = time.time()

        request_params = {
            "model": self.model_name,
            "messages": self.messages
        }

        if stream:
            request_params["stream"] = True

        # 发送请求
        completion = self.client.chat.completions.create(**request_params)

        if stream:
            thinking_process, complete_reply = process_stream_response(completion, show_process)
        else:
            thinking_process, complete_reply = process_non_stream_response(completion, show_process)

        # 添加助手回复到对话历史
        self.add_message("assistant", complete_reply)

        end_time = time.time()
        elapsed_time = end_time - start_time

        if show_process:
            print(f"\n花费时间: {elapsed_time:.2f} 秒")

        return thinking_process, complete_reply

    def clear_history(self):
        self.messages = []
        self._save_session()
        print(f"已清空会话 {self.session_id} 的历史记录")

    def get_history(self):
        return self.messages

    def set_model(self, model_name):
        """设置模型名称"""
        self.model_name = model_name
        self._save_session()
        print(f"已将模型设置为 {model_name}")


def chat_demo():
    chat = ChatSession()

    # 第一轮对话
    print("=" * 20 + "第一轮对话" + "=" * 20)
    thinking, reply = chat.send_message("你好", show_process=True, stream=True)

    # # 第二轮对话
    # print("=" * 20 + "第二轮对话" + "=" * 20)
    # thinking, reply = chat.send_message("你是谁", show_process=True, stream=False)

    # 显示完整对话历史
    print("=" * 20 + "对话历史" + "=" * 20)
    for msg in chat.get_history():
        print(f"{msg['role']}: {msg['content']}")
