import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang web - Chế độ Wide giúp không gian rộng rãi hơn
st.set_page_config(
    page_title="Chấm Ngữ Văn AI 2.5", 
    page_icon="🌿", 
    layout="wide"
)

# 2. CSS "Xịn" để làm đẹp giao diện
st.markdown("""
    <style>
    /* Màu nền và font chữ */
    .main { background-color: #f9fbf9; }
    
    /* Làm đẹp tiêu đề chính */
    .main-title {
        color: #2e7d32;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    /* Tùy chỉnh nút bấm */
    .stButton>button {
        background: linear-gradient(90deg, #2e7d32, #43a047) !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.3);
    }
    
    /* Bo góc các ô nhập liệu */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 15px !important;
        border: 1px solid #e0e0e0 !important;
    }

    /* Tạo khung cho kết quả */
    .result-card {
        background-color: white;
        padding: 2rem;
        border-radius: 20px;
        border-left: 10px solid #2e7d32;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Thanh bên (Sidebar) - Nơi để hướng dẫn
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3426/3426653.png", width=100)
    st.title("Hướng dẫn")
    st.write("""
    1. **Nhập đề bài** chính xác.
    2. **Dán bài văn** vào ô bên phải.
    3. **Nhấn nút Chấm bài** và đợi AI 2.5 phân tích.
    """)
    st.divider()
    st.caption("Sản phẩm hỗ trợ giảng dạy Ngữ văn - Model Gemini 2.5 Flash")

# 4. Nội dung chính
st.markdown('<h1 class="main-title">🌿 Trình Chấm Bài Văn Thông Minh</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Cố vấn học tập 24/7 cho Sinh viên & Giáo viên Sư phạm</p>", unsafe_allow_html=True)

try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Chưa cấu hình API Key trong Secrets!")
    else:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Chia cột giao diện nhập liệu
        col1, col2 = st.columns([1, 1.5], gap="large")

        with col1:
            st.subheader("📌 Thông tin bài viết")
            topic = st.text_input("Đề bài bài văn:", placeholder="Ví dụ: Phân tích bài thơ Sang Thu...")
            st.write("---")
            st.info("💡 **Mẹo:** Cung cấp đề bài rõ ràng sẽ giúp AI chấm điểm công bằng hơn.")

        with col2:
            st.subheader("🖋️ Nội dung bài làm")
            essay = st.text_area("Nhập văn bản của học sinh:", height=400, placeholder="Dán nội dung bài văn vào đây...")
            
            # Nút bấm nằm ngay dưới ô nhập liệu
            btn_col_1, btn_col_2, btn_col_3 = st.columns([1, 2, 1])
            with btn_col_2:
                click_process = st.button("🚀 Bắt đầu chấm bài ngay")

        # 5. Xử lý chấm bài
        if click_process:
            if essay.strip():
                with st.status("🛠️ Đang phân tích cấu trúc bài viết...", expanded=True) as status:
                    st.write("Đang kiểm tra lỗi chính tả...")
                    st.write("Đang đối chiếu với yêu cầu đề bài...")
                    
                    prompt = f"""
                    Bạn là một giáo viên Ngữ văn giỏi. Hãy chấm bài văn này một cách chuyên sâu.
                    Đề bài: {topic}
                    Bài làm: {essay}
                    
                    Hãy trình bày kết quả theo định dạng Markdown đẹp mắt:
                    - **Điểm số**: (Ghi điểm/10 kèm lời khen/nhắc nhở ngắn)
                    - **Ưu điểm**: (Các ý tốt)
                    - **Hạn chế**: (Những gì cần sửa)
                    - **Gợi ý sửa lỗi**: (Sửa lỗi diễn đạt, chính tả)
                    - **Bài học kinh nghiệm**: (Cách để viết tốt hơn lần sau)
                    """
                    
                    response = model.generate_content(prompt)
                    status.update(label="✅ Đã phân tích xong!", state="complete", expanded=False)

                # Hiển thị kết quả trong khung đẹp
                st.markdown("### 📊 Kết quả đánh giá chi tiết")
                st.markdown(f'<div class="result-card">{response.text}</div>', unsafe_allow_html=True)
                
                # Thêm nút tải về hoặc chia sẻ (Giả lập)
                st.balloons()
            else:
                st.warning("Bạn chưa nhập nội dung bài làm!")

except Exception as e:
    st.error(f"⚠️ Đã xảy ra lỗi: {e}")
