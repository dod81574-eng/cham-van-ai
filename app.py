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

api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- BƯỚC QUAN TRỌNG: TỰ ĐỘNG TÌM MODEL ---
        # Code này sẽ tự lấy cái model đầu tiên mà tài khoản bạn được phép dùng
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if available_models:
            # Ưu tiên lấy bản flash hoặc pro nếu có, không thì lấy cái đầu tiên
            model_to_use = available_models[0]
            for m in available_models:
                if "1.5-flash" in m:
                    model_to_use = m
                    break
            
            model = genai.GenerativeModel(model_name=model_to_use)
            st.sidebar.success(f"Đang dùng: {model_to_use}") # Hiện tên model cho bạn yên tâm
            
            de_bai = st.text_input("Đề bài:", placeholder="Ví dụ: Phân tích Truyện Kiều...")
            bai_lam = st.text_area("Bài làm của học sinh:", height=250)
            
            if st.button("Bắt đầu chấm bài"):
                if bai_lam:
                    with st.spinner('Đang phân tích bài làm...'):
                        prompt = f"Bạn là giáo viên Ngữ văn. Hãy chấm bài dựa trên đề: {de_bai}. Nội dung: {bai_lam}. Trả về điểm và nhận xét chi tiết."
                        response = model.generate_content(prompt)
                        st.success("Đã chấm xong!")
                        st.markdown("---")
                        st.markdown(response.text)
                else:
                    st.warning("Vui lòng nhập bài làm!")
        else:
            st.error("Tài khoản của bạn chưa có model nào khả dụng. Hãy thử tạo Key mới.")
            
    except Exception as e:
        st.error(f"Lỗi: {e}")
else:
    st.info("Vui lòng dán API Key vào bên trái.")
