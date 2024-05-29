from .model import Chat_Model
from . import _PROMPT
from typing import Optional


class Star_Work():

    def __init__(self, model_type: str = "baidu",
                model_name: str = "ernie-speed-128k",) -> None:
        self.chat_model = Chat_Model(model_type = model_type, model_name = model_name)

    def markdown_run(self, title: str, chapter: str, paragraph : Optional[str] = None):
        # date_file_path = f"date/{title}/{chapter}/{paragraph}.docx"
        date_file_path = f"md_date/{title}/{chapter}.md"
        with open(date_file_path, "r", encoding="utf-8") as f:
            date_content = f.read()
        # chat_model = Chat_Model()
        result = self.chat_model.chat(user_input = date_content, user_prompt = _PROMPT._MARKDOWN_USER_PROMPT, streaming = True, input_prompt={"chapter": chapter})
        
        return result
    
    def summrize_run(self, title: str, chapter: str, paragraph : Optional[str] = None):
        # date_file_path = f"date/{title}/{chapter}/{paragraph}.docx"
        date_file_path = "date/人教版高中数学A必修一/第一章/第一节.docx"
        with open(date_file_path, "r", encoding="utf-8") as f:
            date_content = f.read()
        chat_model = Chat_Model()
        result = chat_model.chat(user_input = date_content, user_prompt = _PROMPT._SUMMARIZE_USER_PROMPT)

        return result
        
# 测试
# if __name__ == "__main__":
#     work = Star_Work()
#     result = work.markdown_run("人教版高中数学A必修一", "第一章", "第一节")

# title = "人教版高中数学A必修一"
# chapter = "第一章"
# paragraph = "第一节"
# # date_file_path = "work/date/人教版高中数学A必修一/第一章/第一节.docx"
# date_file_path = f"work/date/{title}/{chapter}/{paragraph}.docx"
# with open(date_file_path, "r", encoding="utf-8") as f:
#     date_content = f.read()
# print(date_content)