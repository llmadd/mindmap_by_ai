import streamlit as st
from streamlit_markmap import markmap
from work.work import Star_Work
import os
import pymysql
from appdb import sql_db
import datetime
import random

def generate_datetime_with_random_number():
    # 获取当前的年月日时
    current_datetime = datetime.datetime.now().strftime("%Y%m%d%H")
    # 生成一个四位随机数
    random_number = random.randint(1000, 9999)
    # 将它们拼接在一起
    return f"{current_datetime}{random_number}"

config = {
    'host': os.getenv("MYSQL_HOST"),
    'user': os.getenv("MYSQL_USER"),
    'password': os.getenv("MYSQL_PASSWORD"),
    'db': os.getenv("MYSQL_DB")
}


db_corn = pymysql.connect(**config)

st.set_page_config(layout="wide")

if "title" not in st.session_state:
    st.session_state.title = ""
if "chapter" not in st.session_state:
    st.session_state.chapter = ""
if "paragraph" not in st.session_state:
    st.session_state.paragraph = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "model_type" not in st.session_state:
    st.session_state.model_type = {
        "model_type": "baidu",
        "model_name": "ernie-speed-8k" 
    }
if "pro_key" not in st.session_state:
    st.session_state.pro_key = ""
hcol1, hcol2 = st.columns(2)
with hcol1:
    st.title("AI-:blue[爱学帮] :sunglasses:")
with hcol2:
    with st.expander("有问题请联系我！"):
        st.markdown("* WX: useai_cn")
        st.markdown("* [Email: xunqichen@126.com](mailto:xunqichen@126.com)")
st.subheader('帮助学生更好的梳理繁杂的知识，提高学习效率', divider='rainbow')

tcol1, tcol2 = st.columns(2)
with tcol1:
    st.session_state.pro_key = st.text_input("请输入专业版密钥",type = "password")
    st.text('请选择需要学习的章节：')
with tcol2:
    model_type = st.selectbox(
        "请选择版本",
        ("普通版","专业版")
    )
    if model_type == "专业版":
        if st.session_state.pro_key != os.getenv("MY_KEY"):
            st.warning('专业版需要输入专业版密钥', icon="⚠️")
            model_type = "普通版"
        else:
            st.session_state.model_type = {
                "model_type": "openai",
                "model_name": "gpt-4o" 
            }
        st.session_state.model_type = {
            "model_type": "openai",
            "model_name": "gpt-4o" 
        }
    st.success('您选择了:blue[{}]'.format(model_type), icon="✅")
col1, col2, col3, col4 = st.columns(4)

with col1:
    title_option = st.selectbox(
    " ",
    ("人教版高中数学必修一","人教版高中数学必修二"))
    st.session_state.title = title_option
    if title_option == "人教版高中数学必修一":
        st.image("output_images/page_1.png", width = 160)
    elif title_option == "人教版高中数学必修二":
        st.image("output_images/2page_1.png", width = 160)

with col2:
    if st.session_state.title == "人教版高中数学必修一":
        chapter_option = st.selectbox(
            " ",
            ("第一章集合与常用逻辑用语","第二章一元二次函数、方程和不等式", "第三章函数的概念与性质","第四章指数函数与对数函数","第五章三角函数"))
        st.session_state.chapter = chapter_option
    elif st.session_state.title == "人教版高中数学必修二":
        chapter_option = st.selectbox(
            " ",
            ("第六章平面向量及其应用","第七章复数","第八章立体几何初步","第九章统计","第十章概率"))
        st.session_state.chapter = chapter_option

with col3:
    paragraph_option = st.selectbox(
        " ",
        ("更细致生成每节内容整理，暂不支持",),
        disabled=True
        )
    st.session_state.paragraph = paragraph_option

with col4:
    st.text(" ")
    st.text(" ")
    start = st.button(label = "生成助学笔记", type = "primary")

if start:
    with st.spinner("正在生成学习笔记..."):
        model = Star_Work(st.session_state.model_type["model_type"], st.session_state.model_type["model_name"])
        result = model.markdown_run(st.session_state.title, st.session_state.chapter, st.session_state.paragraph)
        # st.session_state.answer = result["body"]["result"]
        st.subheader(f"{st.session_state.chapter}-:blue[主要内容]", divider="rainbow") 
        answer_content = ""
        answer_placeholder = st.empty()
        if st.session_state.model_type["model_type"] == "baidu":
            for mes in result:
                answer_content += mes["body"]["result"]
                answer_placeholder.write(answer_content) 
        
        elif st.session_state.model_type["model_type"] == "openai":
            for mes in result:
                # print(mes)
                if mes.choices[0].delta.content:
                    answer_content += mes.choices[0].delta.content
                    answer_placeholder.write(answer_content)
        answer_placeholder.write(answer_content)
        sql_db.insert_id_first_chat(db_corn, question_id = str(generate_datetime_with_random_number()),
                                     question = st.session_state.model_type["model_type"],
                                     first_chat = answer_content,)
        st.session_state.answer = answer_content
        st.subheader(f"{st.session_state.chapter}-:blue[思维导图]", divider="rainbow")
        svg = markmap(st.session_state.answer,height=800)

