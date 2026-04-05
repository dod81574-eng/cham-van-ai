import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Chấm Ngữ Văn AI", layout="centered")
st.title("📝 Trình Chấm bài Ngữ văn Thông minh")

# Nhập Key từ Google AI Studio
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        de_bai = st.text_input("Đề bài:")
        bai_lam = st.text_area("Bài làm của học sinh:", height=300)
        if st.button("Bắt đầu chấm bài"):
            if bai_lam:
                with st.spinner('Đang chấm...'):
                    prompt = f"Bạn là giáo viên Văn. Chấm bài dựa trên đề: {de_bai}. Nội dung: {bai_lam}. Trả về điểm số và nhận xét chi tiết."
                    response = model.generate_content(prompt)
                    st.success("Xong!")
                    st.markdown(response.text)
    except Exception as e:
        st.error(f"Lỗi: {e}")
else:
    st.info("Vui lòng dán API Key từ Google AI Studio vào bên trái.")
