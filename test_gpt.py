import pandas as pd
import openai
import streamlit as st

# OpenAI API 키 설정
openai.api_key = 'sk-proj-W8QTVZpNJVLvWcTNeFpqT3BlbkFJ5OCQwqKFLrMce3RMGOmt'

# 데이터 로드
gpt_df = pd.read_excel('data/profit_month/profit_month.xlsx')

def gpt(gpt_df):
    gpt_df['날짜'] = pd.to_datetime(gpt_df['날짜'])
    gpt_df['년도'] = gpt_df['날짜'].dt.year
    gpt_df['월'] = gpt_df['날짜'].dt.month
    gpt_df['날짜'] = pd.to_datetime(gpt_df['날짜']).dt.strftime('%Y-%m')
    data_analysis = gpt_df[gpt_df['년도'] == 2024]
    
    # 데이터프레임에 대한 설명 요청
    prompt = f"{data_analysis.to_string()} SIIC라는 CS 대행 서비스를 제공하는 업체의 월별 운영실적파일이야. 각 서비스 별로 전월대비 어떠한 변화가 있는지 유의미한 수치 변화가 있는지 분석해줘. 기본적으로 서비스 별로 최근 월이 전월대비 어떠한 변화가 있는지 설명해주고, 각 서비스별로 어떠한 수치적인 변화가 있는지 분석해줘. 또 인사이트가 있다면 제공해줘."
    response = ask_gpt(prompt)
    return response

# GPT에게 데이터프레임 설명 요청 함수
def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 CS 운영실적을 분석하는 컨설턴트야."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

# Streamlit 앱
st.title('월별 운영실적 분석')
if st.button('GPT 분석 실행'):
    result = gpt(gpt_df)
    st.session_state['gpt_result'] = result
    st.write(st.session_state['gpt_result'])
