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

    /* Button styling - สีเขียวมิ้นท์ */
    .stButton>button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Prompt', sans-serif !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
        background: linear-gradient(135deg, #34D399 0%, #10B981 100%);
    }

    /* Link button styling - สีฟ้า */
    .stLinkButton>a {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
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
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%) !important;
    }

    /* LINE Browser Warning */
    .line-warning {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border: 1px solid #F59E0B;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        color: #92400E;
    }

    .line-warning-title {
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Privacy link */
    .privacy-link {
        color: rgba(255,255,255,0.8);
        text-decoration: underline;
        cursor: pointer;
    }

    .privacy-link:hover {
        color: white;
    }

    /* Modal/Popup Styling */
    .modal-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
    }

    .modal-header img {
        height: 60px;
        object-fit: contain;
    }

    .modal-logo-school {
        text-align: center;
        margin-bottom: 1rem;
    }

    .modal-logo-school img {
        height: 100px;
        object-fit: contain;
    }

    .modal-content-box {
        background: #f9fafb;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    .contact-admin-box {
        text-align: center;
        padding: 1.5rem;
    }

    .contact-admin-box img {
        max-width: 250px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .contact-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1rem;
    }

    .contact-subtitle {
        color: #6b7280;
        margin-bottom: 1.5rem;
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
        padding: 2.5rem 2rem;
        margin-top: 3rem;
        background: linear-gradient(135deg, #1F2937 0%, #374151 100%);
        border-radius: 15px;
        color: white;
    }

    .footer-container p {
        margin: 0.3rem 0;
        font-family: 'Prompt', sans-serif !important;
    }

    .footer-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.75rem !important;
        color: #F9FAFB;
    }

    .footer-org {
        font-size: 0.95rem;
        color: #E5E7EB;
        margin-bottom: 0.5rem !important;
    }

    .footer-copyright {
        font-size: 0.85rem;
        color: #9CA3AF;
        margin-top: 1rem !important;
    }

    .footer-privacy {
        font-size: 0.8rem;
        color: #9CA3AF;
        margin-top: 0.5rem !important;
    }

    .footer-privacy a {
        color: #60A5FA;
        text-decoration: none;
    }

    .footer-privacy a:hover {
        text-decoration: underline;
    }

    .footer-dev {
        font-size: 0.75rem;
        color: #6B7280;
        margin-top: 1rem !important;
        padding-top: 1rem;
        border-top: 1px solid #4B5563;
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

# --- Dialog สำหรับนโยบายความเป็นส่วนตัว ---
@st.dialog("📋 นโยบายความเป็นส่วนตัว", width="large")
def show_privacy_policy():
    st.markdown("### โรงเรียนเตรียมอุดมศึกษาภาคใต้")

    st.markdown("""
    **โรงเรียนเตรียมอุดมศึกษาภาคใต้** ให้ความสำคัญกับการคุ้มครองข้อมูลส่วนบุคคลของท่าน โดยนโยบายความเป็นส่วนตัวฉบับนี้ได้อธิบายแนวปฏิบัติเกี่ยวกับการเก็บรวบรวม ใช้ หรือเปิดเผยข้อมูลส่วนบุคคล
    """)

    st.markdown("""
    #### 1. ข้อมูลที่เก็บรวบรวม
    - ชื่อ-นามสกุล ของผู้เข้าร่วมกิจกรรม
    - ข้อมูลการเข้าร่วมกิจกรรม/โครงการ

    #### 2. วัตถุประสงค์ในการใช้ข้อมูล
    - เพื่อออกเกียรติบัตรอิเล็กทรอนิกส์
    - เพื่อยืนยันการเข้าร่วมกิจกรรม
    - เพื่อการติดต่อประสานงานที่เกี่ยวข้อง

    #### 3. การเปิดเผยข้อมูล
    - ข้อมูลจะถูกใช้เพื่อวัตถุประสงค์ที่ระบุไว้เท่านั้น
    - ไม่มีการเปิดเผยข้อมูลแก่บุคคลภายนอก ยกเว้นได้รับความยินยอมจากเจ้าของข้อมูล

    #### 4. การรักษาความปลอดภัยข้อมูล
    - ข้อมูลถูกจัดเก็บในระบบที่มีมาตรการรักษาความปลอดภัยที่เหมาะสม
    - มีการควบคุมการเข้าถึงข้อมูลเฉพาะผู้ที่ได้รับอนุญาตเท่านั้น

    #### 5. สิทธิของเจ้าของข้อมูล
    - สิทธิในการเข้าถึงและขอรับสำเนาข้อมูลส่วนบุคคล
    - สิทธิในการขอแก้ไขข้อมูลส่วนบุคคลให้ถูกต้อง
    - สิทธิในการขอลบข้อมูลส่วนบุคคล

    #### 6. การติดต่อ
    หากมีข้อสงสัยเกี่ยวกับนโยบายความเป็นส่วนตัว กรุณาติดต่อ:
    - โรงเรียนเตรียมอุดมศึกษาภาคใต้
    - อำเภอพระพรหม จังหวัดนครศรีธรรมราช
    """)

    if st.button("ปิด", key="close_privacy", use_container_width=True):
        st.session_state.show_privacy_dialog = False
        st.rerun()

# --- Dialog สำหรับติดต่อผู้ดูแลระบบ ---
@st.dialog("📞 ติดต่อผู้ดูแลระบบ", width="small")
def show_contact_admin():
    st.markdown("""
    <div class="contact-admin-box">
        <div class="contact-title">ติดต่อผู้ดูแลระบบ</div>
        <div class="contact-subtitle">สแกน QR Code เพื่อเพิ่มเพื่อนใน LINE</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("images/lineadmin.jpg", caption="LINE ผู้ดูแลระบบ", use_container_width=True)

    st.markdown("""
    ---
    **หมายเหตุ:** กรุณาแจ้งชื่อ-นามสกุล และรายละเอียดปัญหาที่พบ
    """)

    if st.button("ปิด", key="close_contact", use_container_width=True):
        st.session_state.show_contact_dialog = False
        st.rerun()

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

            # คำเตือนสำหรับผู้ใช้ LINE Browser
            st.markdown("""
            <div class="line-warning">
                <div class="line-warning-title">⚠️ หากเปิดผ่านแอป LINE</div>
                <div>กรุณาคัดลอกลิงค์ไปเปิดในเบราว์เซอร์ (Chrome, Safari) เพื่อดาวน์โหลดไฟล์<br>
                <strong>วิธี:</strong> กดปุ่ม ⋮ มุมขวาบน → เลือก "เปิดใน Chrome/Safari"</div>
            </div>
            """, unsafe_allow_html=True)

            for index, row in results.iterrows():
                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                col_info, col_action = st.columns([3, 1])

                with col_info:
                    st.markdown(f"### 📄 {row['name']}")

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

# ใช้ session_state เพื่อจัดการ dialog
if "show_privacy_dialog" not in st.session_state:
    st.session_state.show_privacy_dialog = False
if "show_contact_dialog" not in st.session_state:
    st.session_state.show_contact_dialog = False

# Footer พร้อมลิงค์
st.markdown("""
<div class="footer-container">
    <p class="footer-title">ระบบออกเกียรติบัตรอิเล็กทรอนิกส์</p>
    <p class="footer-org">โรงเรียนเตรียมอุดมศึกษาภาคใต้</p>
    <p class="footer-copyright">© 2567 สงวนลิขสิทธิ์ โรงเรียนเตรียมอุดมศึกษาภาคใต้</p>
    <p class="footer-dev">พัฒนาโดย นายอัศวิน จุลมูล</p>
</div>
""", unsafe_allow_html=True)

# ลิงค์ข้อความ
st.markdown("""
<style>
    .footer-link-btn button {
        background: transparent !important;
        border: none !important;
        color: #9CA3AF !important;
        padding: 0 !important;
        font-size: 0.8rem !important;
        box-shadow: none !important;
    }
    .footer-link-btn button:hover {
        color: #60A5FA !important;
        text-decoration: underline !important;
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

col_link1, col_link2, col_link3 = st.columns([1, 1, 1])
with col_link1:
    st.markdown('<div class="footer-link-btn">', unsafe_allow_html=True)
    if st.button("นโยบายความเป็นส่วนตัว", key="btn_privacy"):
        st.session_state.show_privacy_dialog = True
        st.session_state.show_contact_dialog = False
    st.markdown('</div>', unsafe_allow_html=True)
with col_link2:
    st.markdown('<div class="footer-link-btn">', unsafe_allow_html=True)
    if st.button("ติดต่อผู้ดูแลระบบ", key="btn_contact"):
        st.session_state.show_contact_dialog = True
        st.session_state.show_privacy_dialog = False
    st.markdown('</div>', unsafe_allow_html=True)

# แสดง Dialog ตาม session_state
if st.session_state.show_privacy_dialog:
    show_privacy_policy()
if st.session_state.show_contact_dialog:
    show_contact_admin()

# Link ไปหน้า Admin (ซ่อนไว้ใน sidebar)
with st.sidebar:
    st.markdown("---")
    if st.button("🔐 เข้าสู่ระบบ Admin"):
        st.switch_page("admin_app.py")
