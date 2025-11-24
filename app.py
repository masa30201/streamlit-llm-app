# 各種ライブラリの読み込み
# 変更
import streamlit as st
from dotenv import load_dotenv  # ローカル開発用（本番は secrets を推奨）

# ★ ここを新APIに変更
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 環境変数の読み込み（ローカル用。クラウドは secrets で設定）
load_dotenv()

def get_llm_response(user_message, selected_theme):
    """
    LLMからの回答を取得する処理
    """
    # ★ model_name -> model / そして invoke を使う
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

    # テーマ分岐
    if selected_theme == "運動":
        system_message = """
あなたは運動の専門家です。...（略）...
"""
    else:
        system_message = """
あなたは睡眠の専門家です。...（略）...
"""

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message)
    ]

    # ★ ここが新API（__call__ ではなく invoke）
    response = llm.invoke(messages)
    return response.content

st.title("運動・睡眠のチャット相談アプリ")
st.write("運動・睡眠に関する生成AIチャット相談アプリです。...")

theme_1 = "運動"
theme_2 = "睡眠"
selected_theme = st.radio("【テーマ】", [theme_1, theme_2])
st.divider()

user_message = st.text_input(label="相談内容を入力してください")

if st.button("送信"):
    st.divider()
    try:
        response = get_llm_response(user_message, selected_theme)
        st.write(response)
    except Exception as e:
        st.error("回答生成中にエラーが発生しました。設定や依存関係をご確認ください。")
        st.exception(e)
