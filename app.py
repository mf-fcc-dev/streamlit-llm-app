
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 環境変数（APIキー）を読み込む
load_dotenv()

# モデルの準備（gpt-4oなどに変えてもOK）
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# 専門家ごとのシステムメッセージ（プロンプト）
expert_prompts = {
    "登山の専門家": "あなたは熟練した登山ガイドです。登山者に分かりやすく、安全に関するアドバイスや山の情報を丁寧に伝えてください。",
    "地球科学の専門家": "あなたは地球科学の専門家です。地質や気象、火山、地震などに関する質問に、専門的かつやさしい言葉で答えてください。"
}

# 回答を生成する関数
def generate_response(user_input, expert_type):
    system_prompt = expert_prompts.get(expert_type, "")
    
    template = """
    以下の制約に従って質問に回答してください。
    
    [専門家としての指針]
    {system_prompt}
    
    [ユーザーの質問]
    {question}
    
    [回答]
    """

    prompt = PromptTemplate(
        input_variables=["system_prompt", "question"],
        template=template
    )

    final_prompt = prompt.format(system_prompt=system_prompt, question=user_input)
    
    return llm.invoke(final_prompt)

# --- Streamlit UI ---

st.title("🧠 LLMに聞いてみよう！")
st.markdown("このアプリでは、登山や地球科学の専門家になりきったAIに質問できます。ラジオボタンで専門家を選び、質問を入力してください。")

# 専門家の選択
expert = st.radio("専門家を選んでください：", ["登山の専門家", "地球科学の専門家"])

# ユーザーの質問
user_question = st.text_input("質問を入力してください", placeholder="例：夏におすすめの登山ルートは？")

# ボタンで送信
if st.button("質問する"):
    if user_question.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("考え中..."):
            answer = generate_response(user_question, expert)
            st.success("回答が届きました！")
            st.write(answer.content)