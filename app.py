import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Chấm Ngữ Văn AI", layout="centered")
st.title("📝 Trình Chấm bài Ngữ văn Thông minh")

# Nhập Key từ Google AI Studio
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Sử dụng gemini-1.5-flash trực tiếp, không có models/ phía trước
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        de_bai = st.text_input("Đề bài:", placeholder="Ví dụ: Phân tích bài thơ...")
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
        # Nếu vẫn lỗi 404, thử đổi model thành gemini-pro
        st.error(f"Lỗi: {e}. Thử đổi model trong code thành 'gemini-pro'.")
else:
    st.info("Vui lòng dán API Key từ Google AI Studio vào bên trái.")
