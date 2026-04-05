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

# Lấy API Key từ Secrets (Không hiện ra giao diện nữa)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Tự động lấy model khả dụng
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_to_use = "gemini-1.5-flash" if any("1.5-flash" in m for m in available_models) else available_models[0]
    model = genai.GenerativeModel(model_name=model_to_use)

    de_bai = st.text_input("Đề bài:", placeholder="Ví dụ: Phân tích Truyện Kiều...")
    bai_lam = st.text_area("Bài làm của học sinh:", height=300)

    if st.button("Bắt đầu chấm bài"):
        if bai_lam:
            with st.spinner('AI đang phân tích bài làm...'):
                prompt = f"Bạn là giáo viên Văn. Hãy chấm bài dựa trên đề: {de_bai}. Nội dung: {bai_lam}. Trả về điểm và nhận xét."
                response = model.generate_content(prompt)
                st.success("Đã chấm xong!")
                st.markdown("---")
                st.markdown(response.text)
        else:
            st.warning("Vui lòng nhập bài làm!")
            
except Exception as e:
    st.error("Hệ thống đang bảo trì hoặc thiếu API Key.")
