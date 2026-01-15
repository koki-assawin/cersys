import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client
import re

# --- การตั้งค่า Supabase ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ กรุณาตั้งค่า SUPABASE_URL และ SUPABASE_KEY")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- การตั้งค่าหน้าเว็บ ---
st.set_page_config(
    page_title="ค้นหาและดาวน์โหลดเกียรติบัตร",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS สำหรับตกแต่ง ---
st.markdown("""
<style>
    /* Google Font Prompt */
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

    /* Apply Prompt font globally */
    html, body, [class*="css"], .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, p, span, div, input, button, label, textarea, select {
        font-family: 'Prompt', sans-serif !important;
    }

    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }

    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 3s infinite linear;
    }

    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }

    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }

    .search-box {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 5px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }

    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Prompt', sans-serif !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    /* Link button styling */
    .stLinkButton>a {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-family: 'Prompt', sans-serif !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
    }

    .stLinkButton>a:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }

    /* Input styling */
    .stTextInput>div>div>input {
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Prompt', sans-serif !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
    }

    /* Selectbox styling */
    .stSelectbox>div>div {
        border-radius: 10px !important;
        font-family: 'Prompt', sans-serif !important;
    }

    /* Info box styling */
    .stAlert {
        border-radius: 12px !important;
        font-family: 'Prompt', sans-serif !important;
    }

    /* Footer styling */
    .footer-container {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
    }

    .footer-container p {
        margin: 0.3rem 0;
        font-family: 'Prompt', sans-serif !important;
    }

    .footer-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem !important;
    }

    .footer-copyright {
        font-size: 0.9rem;
        opacity: 0.9;
    }

    .footer-school {
        font-size: 0.85rem;
        opacity: 0.85;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- ฟังก์ชันดึงข้อมูล ---
def get_events():
    """ดึงรายการกิจกรรมทั้งหมด"""
    try:
        response = supabase.table('events').select("*").order('id', desc=True).execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {str(e)}")
        return pd.DataFrame()

def search_certificates(event_id, search_name):
    """ค้นหาเกียรติบัตรตามชื่อ"""
    try:
        response = supabase.table('certificates').select("*").eq('event_id', event_id).ilike('name', f'%{search_name}%').execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {str(e)}")
        return pd.DataFrame()

def extract_file_id(link):
    """ดึง File ID จาก Google Drive link"""
    if not link:
        return None

    # Pattern สำหรับ Google Drive links
    patterns = [
        r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
        r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)

    return None

def convert_to_download_link(link):
    """แปลงเป็นลิงค์ดาวน์โหลดโดยตรง"""
    file_id = extract_file_id(link)
    if file_id:
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return link

def convert_to_preview_link(link):
    """แปลงเป็นลิงค์ดูไฟล์ (googleusercontent)"""
    file_id = extract_file_id(link)
    if file_id:
        return f"https://lh3.googleusercontent.com/d/{file_id}"
    return link

# --- ส่วน Header ---
st.markdown("""
<div class="main-header">
    <h1>🎓 ระบบดาวน์โหลดเกียรติบัตรออนไลน์</h1>
    <p style="font-size: 1.2rem;">ค้นหาและดาวน์โหลดเกียรติบัตรของคุณ</p>
</div>
""", unsafe_allow_html=True)

# --- ส่วนค้นหา ---
events_df = get_events()

if events_df.empty:
    st.info("📋 ยังไม่มีรายการกิจกรรมในระบบ")
    st.stop()

# แบ่ง layout เป็น 2 คอลัมน์
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 ค้นหาเกียรติบัตร")

    # เลือกกิจกรรม
    event_options = dict(zip(events_df['id'], events_df['event_name']))
    selected_event_id = st.selectbox(
        "เลือกโครงการอบรม / กิจกรรม",
        options=list(event_options.keys()),
        format_func=lambda x: event_options[x],
        key="event_select"
    )

    # แสดงรายละเอียดกิจกรรม
    if selected_event_id:
        event_info = events_df[events_df['id'] == selected_event_id].iloc[0]
        if event_info.get('description'):
            st.caption(f"📝 {event_info['description']}")

    # ช่องค้นหาชื่อ
    search_query = st.text_input(
        "ระบุชื่อ หรือนามสกุลของคุณ",
        placeholder="ตัวอย่าง: สมชาย",
        help="ไม่ต้องใส่คำนำหน้า เช่น นาย, นาง, นางสาว"
    )

    search_button = st.button("🔍 ค้นหา", type="primary", use_container_width=True)

with col2:
    st.info("""
    **📌 วิธีการใช้งาน:**
    1. เลือกกิจกรรม/โครงการ
    2. ใส่ชื่อ-นามสกุลของคุณ
    3. คลิกปุ่ม "ค้นหา"
    4. ดาวน์โหลดเกียรติบัตร

    **💡 เคล็ดลับ:**
    - ไม่ต้องใส่คำนำหน้า
    - ใส่เฉพาะชื่อหรือนามสกุลก็ได้
    - ตรวจสอบการสะกดให้ถูกต้อง
    """)

# --- ส่วนแสดงผลการค้นหา ---
if search_button:
    if not search_query:
        st.warning("⚠️ กรุณากรอกชื่อเพื่อค้นหา")
    else:
        with st.spinner("กำลังค้นหา..."):
            results = search_certificates(selected_event_id, search_query)

        if not results.empty:
            st.success(f"✅ พบข้อมูลจำนวน {len(results)} รายการ")

            for index, row in results.iterrows():
                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                col_info, col_action = st.columns([3, 1])

                with col_info:
                    st.markdown(f"### 📄 {row['name']}")
                    if row.get('order_number'):
                        st.caption(f"ลำดับที่: {row['order_number']}")
                    if row.get('file_name'):
                        st.caption(f"ไฟล์: {row['file_name']}")

                with col_action:
                    if row.get('google_drive_file_link'):
                        # แปลงลิงค์เป็น direct download และ preview
                        download_link = convert_to_download_link(row['google_drive_file_link'])
                        preview_link = convert_to_preview_link(row['google_drive_file_link'])

                        # ปุ่มดาวน์โหลด
                        st.link_button(
                            "📥 ดาวน์โหลด",
                            download_link,
                            use_container_width=True
                        )

                        # ปุ่มดูไฟล์
                        st.link_button(
                            "👁️ ดูไฟล์",
                            preview_link,
                            use_container_width=True
                        )
                    else:
                        st.error("ไม่พบลิงค์ไฟล์")

                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("❌ ไม่พบรายชื่อนี้ในระบบ")
            st.info("""
            **กรุณาตรวจสอบ:**
            - การสะกดชื่อให้ถูกต้อง
            - เลือกกิจกรรมที่ถูกต้อง
            - ลองค้นหาด้วยนามสกุลแทน
            """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div class="footer-container">
    <p class="footer-title">ระบบดาวน์โหลดเกียรติบัตรออนไลน์ V3.0</p>
    <p class="footer-copyright">Copyright 2026 นายอัศวิน จุลมูล</p>
    <p class="footer-school">โรงเรียนเตรียมอุดมศึกษาภาคใต้</p>
</div>
""", unsafe_allow_html=True)

# Link ไปหน้า Admin (ซ่อนไว้ใน sidebar)
with st.sidebar:
    st.markdown("---")
    if st.button("🔐 เข้าสู่ระบบ Admin"):
        st.switch_page("admin_app.py")
