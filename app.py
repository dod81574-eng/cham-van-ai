import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Chấm Ngữ Văn AI", layout="centered")

# Giao diện xanh lá
st.markdown("""
    <style>
    .stButton>button { background-color: #2e7d32 !important; color: white !important; border-radius: 10px; width: 100%; font-weight: bold; }
    h1 { color: #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Trình Chấm bài Ngữ văn Thông minh")

# Lấy Key từ Secrets
try:
    # Đảm bảo tên trong ngoặc vuông này khớp y hệt tên bạn đặt trong Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Gọi thẳng model 2.5 flash
    model = genai.GenerativeModel('gemini-2.5-flash')

    de_bai = st.text_input("Đề bài:", placeholder="Nhập đề bài tại đây...")
    bai_lam = st.text_area("Bài làm của học sinh:", height=300)

    if st.button("Bắt đầu chấm bài"):
        if bai_lam:
            with st.spinner('AI 2.5 đang chấm bài...'):
                prompt = f"Bạn là giáo viên Văn. Hãy chấm bài dựa trên đề: {de_bai}. Nội dung: {bai_lam}. Trả về điểm và nhận xét."
                response = model.generate_content(prompt)
                st.success("Đã chấm xong!")
                st.markdown("---")
                st.markdown(response.text)
        else:
            st.warning("Vui lòng nhập bài làm!")
            
except Exception as e:
    st.error(f"Lỗi kết nối: {e}")
    st.info("Kiểm tra lại xem bạn đã đặt tên GEMINI_API_KEY trong phần Secrets chưa nhé.")
