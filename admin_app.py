import streamlit as st
import pandas as pd
import os
import hashlib
import re
from supabase import create_client, Client
from datetime import datetime
import requests
from io import StringIO

# --- การตั้งค่า Supabase ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ กรุณาตั้งค่า SUPABASE_URL และ SUPABASE_KEY")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- การตั้งค่าหน้าเว็บ ---
st.set_page_config(
    page_title="ระบบจัดการเกียรติบัตร - Admin",
    page_icon="🔐",
    layout="wide"
)

# --- CSS ---
st.markdown("""
<style>
    /* Google Font Prompt */
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

    /* Apply Prompt font globally */
    html, body, [class*="css"], .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, p, span, div, input, button, label, textarea, select {
        font-family: 'Prompt', sans-serif !important;
    }

    /* Korean Minimal Style - Soft Pink Theme */
    .stApp {
        background: linear-gradient(180deg, #FFF5F5 0%, #FDF2F8 50%, #FCE7F3 100%);
    }

    .admin-header {
        background: linear-gradient(135deg, #FECDD3 0%, #FDA4AF 50%, #FB7185 100%);
        color: #881337;
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(251, 113, 133, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.6);
        position: relative;
        overflow: hidden;
    }

    .admin-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.3) 50%, transparent 70%);
        animation: softShine 4s ease-in-out infinite;
    }

    @keyframes softShine {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }

    .admin-header h1 {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
        letter-spacing: -0.5px;
    }

    .admin-header p {
        font-size: 1rem;
        font-weight: 400;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }

    .login-box {
        max-width: 420px;
        margin: 3rem auto;
        padding: 2.5rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        box-shadow: 0 4px 24px rgba(244, 114, 182, 0.12);
        border: 1px solid rgba(252, 231, 243, 0.8);
        backdrop-filter: blur(10px);
    }

    .login-box h2 {
        font-weight: 500;
        margin-bottom: 1rem;
        color: #9D174D;
    }

    /* Button styling - Soft Pink */
    .stButton>button {
        background: linear-gradient(135deg, #F9A8D4 0%, #F472B6 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 500;
        font-family: 'Prompt', sans-serif !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 12px rgba(244, 114, 182, 0.25);
        letter-spacing: 0.3px;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(244, 114, 182, 0.35);
        background: linear-gradient(135deg, #FBCFE8 0%, #F9A8D4 100%);
    }

    /* Input styling - Minimal */
    .stTextInput>div>div>input {
        border-radius: 12px !important;
        border: 1.5px solid #FECDD3 !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Prompt', sans-serif !important;
        transition: all 0.3s ease !important;
        background: #FFFBFC !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #F9A8D4 !important;
        box-shadow: 0 0 0 3px rgba(249, 168, 212, 0.2) !important;
        background: white !important;
    }

    /* Text area styling */
    .stTextArea>div>div>textarea {
        border-radius: 12px !important;
        border: 1.5px solid #FECDD3 !important;
        font-family: 'Prompt', sans-serif !important;
        background: #FFFBFC !important;
    }

    .stTextArea>div>div>textarea:focus {
        border-color: #F9A8D4 !important;
        box-shadow: 0 0 0 3px rgba(249, 168, 212, 0.2) !important;
    }

    /* Selectbox styling */
    .stSelectbox>div>div {
        border-radius: 12px !important;
        font-family: 'Prompt', sans-serif !important;
    }

    /* Radio button styling */
    .stRadio>label {
        font-family: 'Prompt', sans-serif !important;
        font-weight: 400;
        color: #9D174D;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-family: 'Prompt', sans-serif !important;
        font-weight: 500;
        background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%) !important;
        border-radius: 12px !important;
        border: 1px solid #FECDD3 !important;
    }

    /* Info/Alert box styling */
    .stAlert {
        border-radius: 16px !important;
        font-family: 'Prompt', sans-serif !important;
        border: none !important;
    }

    /* Metric styling */
    .css-1xarl3l {
        font-family: 'Prompt', sans-serif !important;
    }

    /* Metric card styling */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.8);
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #FECDD3;
        box-shadow: 0 2px 8px rgba(244, 114, 182, 0.08);
    }

    [data-testid="stMetricValue"] {
        color: #BE185D !important;
    }

    /* Sidebar styling - Korean Minimal */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFF1F2 0%, #FCE7F3 50%, #FBCFE8 100%);
        border-right: 1px solid #FECDD3;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #831843;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #9D174D !important;
        font-weight: 400;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        color: #BE185D !important;
    }

    /* Footer styling - Soft Pink */
    .footer-container {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: linear-gradient(135deg, #FECDD3 0%, #FDA4AF 100%);
        border-radius: 20px;
        color: #881337;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 4px 16px rgba(251, 113, 133, 0.15);
    }

    .footer-container p {
        margin: 0.3rem 0;
        font-family: 'Prompt', sans-serif !important;
    }

    .footer-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem !important;
        color: #9D174D;
    }

    .footer-copyright {
        font-size: 0.9rem;
        color: #BE185D;
    }

    .footer-school {
        font-size: 0.85rem;
        color: #9D174D;
        opacity: 0.9;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* DataTable styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #FECDD3;
    }

    /* DataTable font - Thai support */
    .stDataFrame table {
        font-family: 'Prompt', sans-serif !important;
    }

    .stDataFrame th, .stDataFrame td {
        font-family: 'Prompt', sans-serif !important;
    }

    [data-testid="stDataFrame"] {
        font-family: 'Prompt', sans-serif !important;
    }

    [data-testid="stDataFrame"] div {
        font-family: 'Prompt', sans-serif !important;
    }

    /* AG Grid / Dataframe cells */
    .ag-cell, .ag-header-cell-text {
        font-family: 'Prompt', sans-serif !important;
    }

    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #F9A8D4 0%, #F472B6 100%);
    }

    /* Success/Warning/Error messages */
    .stSuccess {
        background-color: #F0FDF4 !important;
        border-left: 4px solid #86EFAC !important;
    }

    .stWarning {
        background-color: #FFFBEB !important;
        border-left: 4px solid #FCD34D !important;
    }

    .stError {
        background-color: #FFF1F2 !important;
        border-left: 4px solid #FDA4AF !important;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #FECDD3, transparent);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- ฟังก์ชัน Authentication ---
def hash_password(password):
    """สร้าง hash ของ password"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    """ตรวจสอบ username และ password"""
    try:
        password_hash = hash_password(password)
        response = supabase.table('admin_users').select("*").eq('username', username).eq('password_hash', password_hash).execute()

        if response.data and len(response.data) > 0:
            return True, response.data[0]
        return False, None
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {str(e)}")
        return False, None

def logout():
    """Logout"""
    for key in ['logged_in', 'username', 'full_name']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def change_password(username, old_password, new_password):
    """เปลี่ยนรหัสผ่าน"""
    try:
        # ตรวจสอบรหัสผ่านเดิม
        old_hash = hash_password(old_password)
        response = supabase.table('admin_users').select("*").eq('username', username).eq('password_hash', old_hash).execute()

        if not response.data or len(response.data) == 0:
            return False, "รหัสผ่านเดิมไม่ถูกต้อง"

        # อัพเดทรหัสผ่านใหม่
        new_hash = hash_password(new_password)
        supabase.table('admin_users').update({
            'password_hash': new_hash
        }).eq('username', username).execute()

        return True, "เปลี่ยนรหัสผ่านสำเร็จ"
    except Exception as e:
        return False, f"เกิดข้อผิดพลาด: {str(e)}"

# --- ฟังก์ชันจัดการข้อมูล ---
def extract_google_sheet_id(link):
    """ดึง Sheet ID จาก Google Sheet link"""
    patterns = [
        r'docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
    return None

def read_google_sheet(sheet_url):
    """อ่านข้อมูลจาก Google Sheet (public)"""
    try:
        # ดึง Sheet ID
        sheet_id = extract_google_sheet_id(sheet_url)
        if not sheet_id:
            return None, "ไม่สามารถดึง Sheet ID ได้ กรุณาตรวจสอบ URL"

        # สร้าง CSV export URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

        # ดาวน์โหลดข้อมูล (เพิ่ม timeout เป็น 30 วินาที)
        response = requests.get(csv_url, timeout=30)

        if response.status_code == 200:
            # แก้ไข encoding สำหรับภาษาไทย
            response.encoding = 'utf-8'
            csv_text = response.text

            # อ่านเป็น DataFrame ด้วย encoding utf-8
            df = pd.read_csv(StringIO(csv_text), encoding='utf-8')
            return df, None
        else:
            return None, f"ไม่สามารถเข้าถึง Google Sheet (Status: {response.status_code})"

    except requests.exceptions.Timeout:
        return None, "การเชื่อมต่อหมดเวลา กรุณาลองใหม่อีกครั้ง"
    except requests.exceptions.ConnectionError:
        return None, "ไม่สามารถเชื่อมต่ออินเทอร์เน็ตได้ กรุณาตรวจสอบการเชื่อมต่อ"
    except Exception as e:
        return None, f"เกิดข้อผิดพลาด: {str(e)}"

def extract_google_drive_file_id(link):
    """ดึง File ID จาก Google Drive link"""
    patterns = [
        r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
        r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
    return None

def create_google_drive_file_link(file_id):
    """สร้างลิงค์ไฟล์ Google Drive"""
    # ลบ whitespace และ newlines
    file_id = str(file_id).strip()
    return f"https://drive.google.com/file/d/{file_id}/view"

def add_event(event_name, sheet_link, description, created_by):
    """เพิ่มกิจกรรมใหม่"""
    try:
        response = supabase.table('events').insert({
            "event_name": event_name,
            "google_drive_folder_link": sheet_link,  # ใช้เก็บ Google Sheet URL
            "description": description,
            "created_by": created_by,
            "created_at": datetime.now().isoformat()
        }).execute()
        return response.data[0]['id'] if response.data else None
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {str(e)}")
        return None

def add_certificate(event_id, name, order_number, file_link, file_name):
    """เพิ่มเกียรติบัตร"""
    try:
        supabase.table('certificates').insert({
            "event_id": event_id,
            "name": name,
            "order_number": order_number,
            "google_drive_file_link": file_link,
            "file_name": file_name,
            "created_at": datetime.now().isoformat()
        }).execute()
        return True
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {str(e)}")
        return False

def get_events():
    """ดึงรายการกิจกรรม"""
    try:
        response = supabase.table('events').select("*").order('id', desc=True).execute()
        return pd.DataFrame(response.data)
    except:
        return pd.DataFrame()

def get_certificates_by_event(event_id):
    """ดึงรายการเกียรติบัตรตามกิจกรรม"""
    try:
        response = supabase.table('certificates').select("*").eq('event_id', event_id).order('order_number').execute()
        return pd.DataFrame(response.data)
    except:
        return pd.DataFrame()

def delete_event(event_id):
    """ลบกิจกรรม"""
    try:
        supabase.table('events').delete().eq('id', event_id).execute()
        return True
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {str(e)}")
        return False

# --- ส่วน Login ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-box">
        <h2 style="text-align: center; color: #f5576c;">🔐 Admin Login</h2>
        <p style="text-align: center; color: #666;">ระบบจัดการเกียรติบัตร</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="รหัสผ่าน")
            submit = st.form_submit_button("เข้าสู่ระบบ", use_container_width=True)

            if submit:
                if username and password:
                    success, user_data = check_login(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.full_name = user_data.get('full_name', username)
                        st.success("เข้าสู่ระบบสำเร็จ!")
                        st.rerun()
                    else:
                        st.error("❌ Username หรือ Password ไม่ถูกต้อง")
                else:
                    st.warning("⚠️ กรุณากรอก Username และ Password")

        st.info("""
        **ข้อมูล Login เริ่มต้น:**
        - Username: `admin`
        - Password: `admin123`

        ⚠️ กรุณาเปลี่ยนรหัสผ่านหลังเข้าใช้งานครั้งแรก
        """)

        if st.button("← กลับหน้าหลัก"):
            st.switch_page("user_app.py")

    st.stop()

# --- ส่วน Admin Dashboard (หลัง Login) ---
st.markdown(f"""
<div class="admin-header">
    <h1>🎯 ระบบจัดการเกียรติบัตร - Admin Panel</h1>
    <p>ยินดีต้อนรับ คุณ {st.session_state.get('full_name', 'Admin')}</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.get('full_name', 'Admin')}")
    st.caption(f"Username: {st.session_state.username}")
    st.markdown("---")

    menu = st.radio(
        "เมนู",
        ["📊 Dashboard", "➕ เพิ่มกิจกรรมใหม่", "📋 จัดการกิจกรรม", "📥 ดาวน์โหลด Template", "🔑 เปลี่ยนรหัสผ่าน"],
        index=0
    )

    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        logout()

# --- Dashboard ---
if menu == "📊 Dashboard":
    st.header("📊 Dashboard")

    events_df = get_events()

    col1, col2, col3 = st.columns(3)

    with col1:
        event_count = len(events_df) if not events_df.empty else 0
        st.metric("จำนวนกิจกรรมทั้งหมด", event_count)

    with col2:
        total_certs = 0
        if not events_df.empty and 'id' in events_df.columns:
            for event_id in events_df['id']:
                certs = get_certificates_by_event(event_id)
                total_certs += len(certs)
        st.metric("จำนวนเกียรติบัตรทั้งหมด", total_certs)

    with col3:
        st.metric("สถานะระบบ", "🟢 ออนไลน์")

    st.markdown("---")
    st.subheader("📋 กิจกรรมล่าสุด")

    if not events_df.empty and 'id' in events_df.columns:
        for idx, row in events_df.head(5).iterrows():
            with st.expander(f"🎯 {row['event_name']} (ID: {row['id']})"):
                st.write(f"**รายละเอียด:** {row.get('description', 'ไม่มี')}")
                st.write(f"**สร้างโดย:** {row.get('created_by', 'N/A')}")
                created_at = row.get('created_at', '')
                if created_at and len(str(created_at)) >= 10:
                    st.write(f"**วันที่สร้าง:** {str(created_at)[:10]}")

                certs = get_certificates_by_event(row['id'])
                st.write(f"**จำนวนเกียรติบัตร:** {len(certs)} ใบ")
    else:
        st.info("ยังไม่มีกิจกรรมในระบบ")

# --- เพิ่มกิจกรรมใหม่ ---
elif menu == "➕ เพิ่มกิจกรรมใหม่":
    st.header("➕ เพิ่มกิจกรรมใหม่")

    st.subheader("📝 ข้อมูลกิจกรรม")

    event_name = st.text_input("ชื่อกิจกรรม/โครงการ *", placeholder="เช่น: โครงการอบรม Python 2026", key="event_name_input")
    description = st.text_area("รายละเอียด", placeholder="รายละเอียดเพิ่มเติมเกี่ยวกับกิจกรรม", key="description_input")

    st.markdown("---")
    st.subheader("📊 Google Sheet")

    st.info("""
    **วิธีการเตรียม Google Sheet:**
    1. สร้าง Google Sheet ใหม่
    2. สร้างคอลัมน์ 3 คอลัมน์:
       - ลำดับที่
       - ชื่อ-สกุล
       - URL (ลิงค์ไฟล์ PDF จาก Google Drive)
    3. กรอกข้อมูล
    4. แชร์ Google Sheet: "Anyone with the link can VIEW"
    5. คัดลอก URL ของ Google Sheet มาใส่ด้านล่าง

    **ตัวอย่าง Google Sheet:**
    | ลำดับที่ | ชื่อ-สกุล | URL |
    |---------|----------|-----|
    | 1 | นายสมชาย ใจดี | https://drive.google.com/file/d/... |
    | 2 | นางสาวสมหญิง รักดี | https://drive.google.com/file/d/... |
    """)

    sheet_link = st.text_input(
        "ลิงค์ Google Sheet *",
        placeholder="https://docs.google.com/spreadsheets/d/xxxxx/edit",
        help="Google Sheet ต้องแชร์เป็น 'Anyone with the link can view'",
        key="sheet_link_input"
    )

    # ปุ่มทดสอบอ่าน Google Sheet (อยู่นอก form)
    col_test, col_space = st.columns([1, 2])
    with col_test:
        test_button = st.button("🔍 ทดสอบอ่าน Google Sheet", use_container_width=True)

    if test_button and sheet_link:
        with st.spinner("กำลังอ่าน Google Sheet..."):
            df, error = read_google_sheet(sheet_link)

            if error:
                st.error(f"❌ {error}")
                st.warning("""
                **กรุณาตรวจสอบ:**
                - Google Sheet ต้องแชร์เป็น "Anyone with the link can VIEW"
                - URL ต้องเป็น URL ของ Google Sheet
                - ตัวอย่าง: https://docs.google.com/spreadsheets/d/xxxxx/edit
                """)
            else:
                st.success(f"✅ อ่าน Google Sheet สำเร็จ จำนวน {len(df)} รายการ")
                st.dataframe(df.head(10))
                st.info(f"คอลัมน์ที่พบ: {', '.join(df.columns.tolist())}")
    elif test_button and not sheet_link:
        st.warning("⚠️ กรุณาใส่ลิงค์ Google Sheet ก่อน")

    st.markdown("---")

    # Form สำหรับสร้างกิจกรรม
    with st.form("add_event_form"):
        submit = st.form_submit_button("🚀 สร้างกิจกรรม", type="primary", use_container_width=True)

        if submit:
            if not event_name or not sheet_link:
                st.error("❌ กรุณากรอกชื่อกิจกรรมและลิงค์ Google Sheet")
            else:
                with st.spinner("กำลังอ่าน Google Sheet..."):
                    # อ่าน Google Sheet
                    df, error = read_google_sheet(sheet_link)

                    if error:
                        st.error(f"❌ {error}")
                        st.stop()

                    # ตรวจสอบคอลัมน์ที่จำเป็น
                    required_columns = ['ลำดับที่', 'ชื่อ-สกุล', 'URL']
                    missing_columns = [col for col in required_columns if col not in df.columns]

                    if missing_columns:
                        st.error(f"❌ Google Sheet ขาดคอลัมน์: {', '.join(missing_columns)}")
                        st.info(f"คอลัมน์ที่มี: {', '.join(df.columns.tolist())}")
                        st.warning("""
                        **Google Sheet ต้องมีคอลัมน์:**
                        - ลำดับที่
                        - ชื่อ-สกุล
                        - URL
                        """)
                        st.stop()

                    st.success(f"✅ อ่าน Google Sheet สำเร็จ จำนวน {len(df)} รายการ")

                with st.spinner("กำลังสร้างกิจกรรม..."):
                    # สร้าง Event
                    event_id = add_event(
                        event_name,
                        sheet_link,
                        description,
                        st.session_state.username
                    )

                    if event_id:
                        st.success(f"✅ สร้างกิจกรรม ID: {event_id} สำเร็จ")

                        # สร้างเกียรติบัตรจาก Google Sheet
                        progress_bar = st.progress(0)
                        success_count = 0
                        error_count = 0

                        for idx, row in df.iterrows():
                            try:
                                order_num = int(row['ลำดับที่'])
                                name = str(row['ชื่อ-สกุล']).strip()
                                file_url = str(row['URL']).strip()

                                if not name or name.lower() == 'nan':
                                    st.warning(f"⚠️ แถวที่ {idx+1}: ไม่มีชื่อ")
                                    error_count += 1
                                    continue

                                if not file_url or file_url.lower() == 'nan':
                                    st.warning(f"⚠️ แถวที่ {idx+1}: ไม่มี URL")
                                    error_count += 1
                                    continue

                                file_name = f"{order_num}.pdf"

                                # บันทึกลง Database
                                if add_certificate(event_id, name, order_num, file_url, file_name):
                                    success_count += 1
                                else:
                                    error_count += 1

                            except Exception as e:
                                st.warning(f"⚠️ แถวที่ {idx+1}: {str(e)}")
                                error_count += 1

                            progress_bar.progress((idx + 1) / len(df))

                        if error_count > 0:
                            st.warning(f"⚠️ สร้างเกียรติบัตรสำเร็จ {success_count}/{len(df)} ใบ ({error_count} ข้ามไป)")
                        else:
                            st.success(f"✅ สร้างเกียรติบัตรสำเร็จ {success_count}/{len(df)} ใบ")
                            st.balloons()
                    else:
                        st.error("❌ ไม่สามารถสร้างกิจกรรมได้")

# --- จัดการกิจกรรม ---
elif menu == "📋 จัดการกิจกรรม":
    st.header("📋 จัดการกิจกรรม")

    events_df = get_events()

    if events_df.empty:
        st.info("ยังไม่มีกิจกรรมในระบบ")
    else:
        for idx, event in events_df.iterrows():
            with st.expander(f"🎯 {event['event_name']} (ID: {event['id']})"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**รายละเอียด:** {event.get('description', 'ไม่มี')}")
                    st.write(f"**ลิงค์โฟลเดอร์:** {event.get('google_drive_folder_link', 'ไม่มี')}")
                    st.write(f"**สร้างโดย:** {event.get('created_by', 'N/A')}")

                    certs = get_certificates_by_event(event['id'])
                    st.write(f"**จำนวนเกียรติบัตร:** {len(certs)} ใบ")

                    if not certs.empty:
                        st.dataframe(certs[['order_number', 'name', 'file_name']].head(10))

                with col2:
                    if st.button(f"🗑️ ลบ", key=f"del_{event['id']}"):
                        if delete_event(event['id']):
                            st.success("ลบสำเร็จ")
                            st.rerun()

# --- คู่มือ Google Sheet ---
elif menu == "📥 ดาวน์โหลด Template":
    st.header("📊 วิธีสร้าง Google Sheet")

    st.info("""
    **ระบบใหม่ใช้ Google Sheet แทน Excel**

    ข้อดี:
    - ไม่ต้องอัพโหลดไฟล์
    - แก้ไขได้ทันที (แก้ Google Sheet จะอัพเดทระบบอัตโนมัติ)
    - คุณเตรียม URL ไฟล์เองได้
    """)

    st.markdown("---")
    st.subheader("📝 ขั้นตอนการสร้าง Google Sheet")

    st.markdown("""
    ### 1. สร้าง Google Sheet ใหม่
    - เข้า Google Drive
    - คลิก "New" → "Google Sheets" → "Blank spreadsheet"

    ### 2. สร้างคอลัมน์ 3 คอลัมน์
    | ลำดับที่ | ชื่อ-สกุล | URL |
    |---------|----------|-----|
    | 1 | นายสมชาย ใจดี | https://drive.google.com/file/d/... |
    | 2 | นางสาวสมหญิง รักดี | https://drive.google.com/file/d/... |
    | 3 | นายทดสอบ ระบบ | https://drive.google.com/file/d/... |

    **สำคัญ:** ชื่อคอลัมน์ต้องเป็น `ลำดับที่`, `ชื่อ-สกุล`, `URL` (ตัวพิมพ์ต้องตรง)

    ### 3. กรอกข้อมูล
    - **ลำดับที่:** เรียงจาก 1, 2, 3, ...
    - **ชื่อ-สกุล:** ชื่อผู้รับเกียรติบัตร
    - **URL:** ลิงค์ไฟล์ PDF จาก Google Drive

    ### 4. แชร์ Google Sheet
    - คลิก "Share" (มุมบนขวา)
    - เปลี่ยนเป็น **"Anyone with the link"**
    - ตั้งเป็น **"Viewer"**
    - คลิก "Copy link"

    ### 5. นำลิงค์ไปใช้ในระบบ
    - ไปที่เมนู "เพิ่มกิจกรรมใหม่"
    - วางลิงค์ Google Sheet
    - คลิก "ทดสอบอ่าน Google Sheet" เพื่อตรวจสอบ
    - สร้างกิจกรรม
    """)

    st.markdown("---")
    st.subheader("📥 ดาวน์โหลด CSV Template")

    template_csv = "template_google_sheet.csv"

    if os.path.exists(template_csv):
        with open(template_csv, "rb") as file:
            st.download_button(
                label="📥 ดาวน์โหลด CSV Template",
                data=file,
                file_name="template_google_sheet.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.success("✅ ดาวน์โหลด CSV Template แล้วนำไป Import ใน Google Sheet")

        st.markdown("""
        **วิธี Import:**
        1. เปิด Google Sheet
        2. File → Import → Upload
        3. เลือกไฟล์ CSV ที่ดาวน์โหลด
        4. แก้ไข URL เป็นลิงค์จริงของคุณ
        """)

    else:
        st.warning("กำลังสร้าง Template...")
        # สร้าง Template ถ้ายังไม่มี
        data = {
            'ลำดับที่': [1, 2, 3],
            'ชื่อ-สกุล': ['นายสมชาย ใจดี', 'นางสาวสมหญิง รักดี', 'นายทดสอบ ระบบ'],
            'URL': [
                'https://drive.google.com/file/d/1UP4SLbS2fDN2jx_0Di8iD9KzhTG_oljU/view',
                'https://drive.google.com/file/d/1ABC123DEF456GHI789/view',
                'https://drive.google.com/file/d/1XYZ789PQR456STU123/view'
            ]
        }
        df_template = pd.DataFrame(data)
        df_template.to_csv(template_csv, index=False, encoding='utf-8-sig')
        st.rerun()

    st.markdown("---")
    st.subheader("📋 ตัวอย่าง Google Sheet")

    example_data = {
        'ลำดับที่': [1, 2, 3],
        'ชื่อ-สกุล': ['นายสมชาย ใจดี', 'นางสาวสมหญิง รักดี', 'นายทดสอบ ระบบ'],
        'URL': [
            'https://drive.google.com/file/d/1UP4SLbS2fDN2jx_0Di8iD9KzhTG_oljU/view',
            'https://drive.google.com/file/d/1ABC123DEF456GHI789/view',
            'https://drive.google.com/file/d/1XYZ789PQR456STU123/view'
        ]
    }
    st.dataframe(pd.DataFrame(example_data))

# --- เปลี่ยนรหัสผ่าน ---
elif menu == "🔑 เปลี่ยนรหัสผ่าน":
    st.header("🔑 เปลี่ยนรหัสผ่าน")

    st.info(f"กำลังเปลี่ยนรหัสผ่านสำหรับ: **{st.session_state.username}**")

    with st.form("change_password_form"):
        old_password = st.text_input("รหัสผ่านเดิม", type="password", placeholder="กรอกรหัสผ่านเดิม")
        new_password = st.text_input("รหัสผ่านใหม่", type="password", placeholder="กรอกรหัสผ่านใหม่ (อย่างน้อย 6 ตัวอักษร)")
        confirm_password = st.text_input("ยืนยันรหัสผ่านใหม่", type="password", placeholder="กรอกรหัสผ่านใหม่อีกครั้ง")

        submit = st.form_submit_button("🔄 เปลี่ยนรหัสผ่าน", type="primary", use_container_width=True)

        if submit:
            if not old_password or not new_password or not confirm_password:
                st.error("❌ กรุณากรอกข้อมูลให้ครบทุกช่อง")
            elif len(new_password) < 6:
                st.error("❌ รหัสผ่านใหม่ต้องมีอย่างน้อย 6 ตัวอักษร")
            elif new_password != confirm_password:
                st.error("❌ รหัสผ่านใหม่ไม่ตรงกัน")
            elif old_password == new_password:
                st.error("❌ รหัสผ่านใหม่ต้องไม่เหมือนรหัสผ่านเดิม")
            else:
                success, message = change_password(st.session_state.username, old_password, new_password)
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                    st.info("กรุณา Login ใหม่ด้วยรหัสผ่านใหม่")
                    # Logout หลังเปลี่ยนรหัสผ่าน
                    import time
                    time.sleep(2)
                    logout()
                else:
                    st.error(f"❌ {message}")

    st.markdown("---")
    st.warning("""
    **คำแนะนำการตั้งรหัสผ่าน:**
    - ควรมีความยาวอย่างน้อย 6 ตัวอักษร
    - ควรมีตัวอักษรผสมตัวเลข
    - ไม่ควรใช้ข้อมูลส่วนตัวที่เดาง่าย
    """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div class="footer-container">
    <p class="footer-title">ระบบจัดการเกียรติบัตร - Admin Panel V3.0</p>
    <p class="footer-copyright">Copyright 2026 นายอัศวิน จุลมูล</p>
    <p class="footer-school">โรงเรียนเตรียมอุดมศึกษาภาคใต้</p>
</div>
""", unsafe_allow_html=True)
