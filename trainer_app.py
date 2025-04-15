import pandas as pd
import streamlit as st
import random
import re

# ✅ 페이지 설정
st.set_page_config(page_title="Korean-English Trainer", layout="centered")

st.title("🇰🇷 Korean-English Sentence Trainer 🇺🇸")

# ✅ CSV 파일에서 데이터 로드
# 파일명은 반드시 'sentences.csv'로 저장되어 있어야 함
data = pd.read_csv("sentences.csv")

# ✅ 상태 초기화
if 'current_row' not in st.session_state:
    st.session_state.current_row = None
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'first_try_correct' not in st.session_state:
    st.session_state.first_try_correct = set()
if 'attempt_count' not in st.session_state:
    st.session_state.attempt_count = {}
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0  # 입력창 리셋 트리거용 key

# ✅ 아직 안 맞춘 문장 인덱스만 선택
available_indices = [
    i for i in range(len(data))
    if i not in st.session_state.first_try_correct
]

# ✅ 모든 문장을 맞춘 경우
if not available_indices:
    st.success("🎉 한 번에 모든 문장을 맞추셨어요! 대단해요!")
else:
    # ✅ Next 클릭 시 입력창도 초기화
    if st.session_state.current_row is None or st.button("🔁 Next Random Sentence"):
        st.session_state.current_row = random.choice(available_indices)
        st.session_state.answered = False
        st.session_state.feedback = ""
        st.session_state.input_key += 1  # 입력창 초기화 트리거

    # ✅ 현재 문장 표시
    korean_sentence = data.iloc[st.session_state.current_row]['Korean']
    english_answer = data.iloc[st.session_state.current_row]['English']
    st.markdown(f"### 🇰🇷 {korean_sentence}")

    # ✅ 입력 + 엔터 제출
    with st.form(key="answer_form"):
        user_input = st.text_input(
            "✍️ Type your English translation:",
            key=f"user_input_{st.session_state.input_key}"
        )
        submitted = st.form_submit_button("✅ Check Answer")

        if submitted and not st.session_state.answered:
            st.session_state.attempt_count.setdefault(st.session_state.current_row, 0)
            st.session_state.attempt_count[st.session_state.current_row] += 1

            def normalize(text):
                return re.sub(r'[^a-zA-Z0-9]', '', text.lower())

            if normalize(user_input) == normalize(english_answer):
                if st.session_state.attempt_count[st.session_state.current_row] == 1:
                    st.session_state.first_try_correct.add(st.session_state.current_row)
                st.session_state.feedback = "✅ Correct! Well done."
            else:
                st.session_state.feedback = f"❌ Incorrect. Correct answer: **{english_answer}**"
            st.session_state.answered = True

    # ✅ 피드백 표시
    if st.session_state.feedback:
        st.info(st.session_state.feedback)
