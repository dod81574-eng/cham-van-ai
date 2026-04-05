import streamlit as st
import google.generativeai as genai

# 1. Cấu hình giao diện và màu sắc xanh lá
st.set_page_config(page_title="Chấm Ngữ Văn AI", layout="centered")

# Thêm CSS để đổi màu nút bấm và tiêu đề sang xanh lá (Đã sửa lỗi unsafe_allow_html)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 10px;
        border: None;
        width: 100%;
        height: 3em;
        font-weight: bold;
    }
    h1 {
        color: #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Trình Chấm bài Ngữ văn Thông minh")
st.subheader("Dành cho sinh viên và giáo viên Ngữ văn")

# Nhập Key từ Google AI Studio
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Sử dụng gemini-pro để ổn định nhất
        model = genai.GenerativeModel('gemini-pro')
        
        de_bai = st.text_input("Đề bài:", placeholder="Ví dụ: Ý nghĩa của lòng dũng cảm...")
        bai_lam = st.text_area("Bài làm của học sinh:", height=300)
        
        if st.button("Bắt đầu chấm bài"):
            if bai_lam:
                with st.spinner('AI đang đọc và chấm bài...'):
                    prompt = f"Bạn là giáo viên Văn chuyên nghiệp. Hãy chấm bài dựa trên đề: {de_bai}. Nội dung: {bai_lam}. Trả về: 1. Điểm số (thang 10), 2. Nhận xét ưu/nhược, 3. Cách cải thiện."
                    response = model.generate_content(prompt)
                    st.success("Đã chấm xong!")
                    st.markdown("---")
                    st.markdown(response.text)
            else:
                st.error("Vui lòng dán nội dung bài làm!")
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
else:
    st.info("Vui lòng dán API Key từ Google AI Studio vào ô bên trái để bắt đầu.")
