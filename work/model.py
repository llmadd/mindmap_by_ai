from openai import OpenAI
import os
import qianfan
import warnings
from dotenv import load_dotenv
from typing import List, Dict, Union, Optional
import os
load_dotenv()




# os.environ["QIANFAN_ACCESS_KEY"] = os.getenv("QIANFAN_ACCESS_KEY")
# os.environ["QIANFAN_SECRET_KEY"] = os.getenv("QIANFAN_SECRET_KEY")
class Chat_Model():

    def __init__(self, model_type: str = "baidu",
                model_name: str = "ernie-speed-128k",
                system_message: bool = False) -> None:
        """
            初始化chat_model
            Args:
                model_type (str): 模型厂商，默认为"baidu";
                model_name (str): 模型名称，默认为"ernie-speed-128k";
                system_message (bool): 模型是否有system_message角色，默认为True;

            Returns:
                None
        """

        self.model_type = model_type
        if self.model_type == "baidu":
            self.model_name = model_name
            self.system_message = system_message
            # self.model_client = qianfan.ChatCompletion(model = self.model_name)            
        elif self.model_type == "openai":
            self.model_name = model_name
            self.system_message = system_message
            # self.model_client = OpenAI()
        else:
            warnings.warn("模型厂商暂不支持,切换为默认厂商baidu，模型为ernie-speed-128k")
            self.model_name = "ernie-speed-128k"
            self.system_message = False
            self.model_client = qianfan.ChatCompletion(model = self.model_name)  

    def chat(self, user_input: str, 
                    user_prompt: Optional[str] = None, 
                    system_prompt: Optional[str] = None, 
                    history: Optional[List[Dict[str, str]]] = None,
                    streaming: bool = False,
                    input_prompt: Optional[Dict[str, str]] = None,
                    **kwargs):
        """
            与chat_model进行对话
            Args:
                user_input (str): 用户输入
                user_prompt (str): 用户提示
                system_prompt (str): 系统提示
                history (list): 对话历史
                streaming (bool): 是否流式输出
                **kwargs: 其他参数

            Returns:
                response (str): 模型回复
        """
        if self.model_type == "baidu":
            chat_comp = qianfan.ChatCompletion()
            user_content = user_prompt.format(user_input = user_input,**input_prompt) if user_prompt else user_input
            messages = history if history else []
            messages.append({"role": "user", "content": user_content})
            # print(messages)
            
            resp = chat_comp.do(model=self.model_name, messages=messages, stream=streaming, **kwargs)
            return resp
        elif self.model_type == "openai":
            client = OpenAI(base_url = os.getenv("BASE_URL"))
            user_content = user_prompt.format(user_input = user_input, **input_prompt) if user_prompt else user_input
            if system_prompt:
                messages = [{"role": "system", "content": system_prompt}]
            else:
                messages = []
            if history:
                messages += history
            messages.append({"role": "user", "content": user_content})
            # print(messages)
            completion = client.chat.completions.create(model=self.model_name, messages=messages, stream=streaming, **kwargs)
            return completion

# 示例用法
# system = "你的名字是李白"
# history = [
#     {"role": "user", "content": "你好"},
#     {"role": "assistant", "content": "你好，我是李白，有什么可以帮助你的吗？"}
# ]
# chat_model = Chat_Model(model_type = "openai", model_name = "gpt-3.5-turbo")
# chat_model = Chat_Model(model_name = "ERNIE-Speed-8K")
# response = chat_model.chat("你好,你的名字叫什么", streaming= True)
# # print(response["body"]["result"])
# for i in response:
#     print(i.choices[0].delta.content)
#     print("-"*80)
