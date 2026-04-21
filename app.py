import streamlit as st
import google.generativeai as genai

# Cấu hình trang web
st.set_page_config(page_title="Chấm Ngữ Văn AI", layout="centered")

# Giao diện màu xanh lá đặc trưng sư phạm
st.markdown("""
    <style>
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
        height: 3em;
    }
    h1 { color: #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Trình Chấm Bài Ngữ Văn Thông Minh")
st.info("Phiên bản hỗ trợ Model Gemini 2.5 Flash")

# Lấy API Key từ hệ thống bảo mật Secrets của Streamlit
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Chưa cấu hình API Key trong phần Secrets của Streamlit Cloud!")
    else:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Sử dụng Model 2.5 Flash mới nhất
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Giao diện nhập liệu
        topic = st.text_input("Đề bài:", placeholder="Ví dụ: Nghị luận về lòng dũng cảm...")
        essay = st.text_area("Bài làm của học sinh:", height=350, placeholder="Dán nội dung bài làm vào đây...")

        if st.button("Bắt đầu chấm bài"):
            if essay.strip():
                with st.spinner('Hệ thống AI 2.5 đang phân tích và chấm điểm...'):
                    # Prompt chuyên sâu dành cho giáo viên Ngữ văn
                    prompt = f"""
                    Bạn là một giáo viên Ngữ văn giàu kinh nghiệm. Hãy chấm bài văn sau:
                    Đề bài: {topic}
                    Nội dung bài làm: {essay}
                    
                    Yêu cầu kết quả trả về bao gồm:
                    1. Điểm số (Thang điểm 10).
                    2. Nhận xét chi tiết về nội dung, hình thức và sáng tạo.
                    3. Chỉ ra các lỗi chính tả hoặc diễn đạt (nếu có).
                    4. Lời khuyên cụ thể để học sinh viết tốt hơn.
                    """
                    
                    response = model.generate_content(prompt)
                    st.success("Đã hoàn thành việc chấm bài!")
                    st.markdown("---")
                    st.markdown(response.text)
            else:
                st.warning("Vui lòng nhập nội dung bài làm trước khi nhấn nút chấm.")

except Exception as e:
    st.error(f"Lỗi hệ thống: {e}")
    st.info("Mẹo: Nếu lỗi 403, hãy tạo API Key mới và cập nhật lại trong mục Secrets.")
