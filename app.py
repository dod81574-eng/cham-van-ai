import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Chấm Ngữ Văn AI", layout="centered")

# Giao diện xanh lá cho Khang
st.markdown("""
    <style>
    .stButton>button { background-color: #2e7d32 !important; color: white !important; border-radius: 10px; width: 100%; font-weight: bold; }
    h1 { color: #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Trình Chấm bài Ngữ văn Thông minh")

api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Chiến thuật thử lần lượt các model để tránh lỗi 404
        model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        model = None
        
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                # Thử tạo một nội dung ngắn để test model có sống không
                model.generate_content("test", generation_config={"max_output_tokens": 1})
                break 
            except:
                continue

        if model:
            de_bai = st.text_input("Đề bài:")
            bai_lam = st.text_area("Bài làm của học sinh:", height=250)
            
            if st.button("Bắt đầu chấm bài"):
                if bai_lam:
                    with st.spinner('Đang phân tích bài làm...'):
                        prompt = f"Bạn là giáo viên Ngữ văn. Hãy chấm bài dựa trên đề: {de_bai}. Nội dung: {bai_lam}. Trả về điểm và nhận xét."
                        response = model.generate_content(prompt)
                        st.success("Xong!")
                        st.markdown(response.text)
                else:
                    st.warning("Vui lòng nhập bài làm!")
        else:
            st.error("Không tìm thấy model khả dụng. Hãy kiểm tra lại API Key của bạn.")
            
    except Exception as e:
        st.error(f"Lỗi: {e}")
else:
    st.info("Vui lòng dán API Key vào bên trái.")
