import streamlit as st
import pandas as pd
import os
from pypdf import PdfReader, PdfWriter
from datetime import datetime
import io
from supabase import create_client, Client

# --- การตั้งค่า Supabase ---
# ⚠️ สำคัญมาก: ต้องตั้งค่าใน Streamlit Secrets หรือ Environment Variables
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))

# ตรวจสอบว่ามีการตั้งค่า Supabase หรือไม่
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ กรุณาตั้งค่า SUPABASE_URL และ SUPABASE_KEY ใน Streamlit Secrets")
    st.info("""
    **วิธีตั้งค่า:**
    1. ไปที่ https://supabase.com สมัครบัญชี (ฟรี)
    2. สร้าง Project ใหม่
    3. ไปที่ Settings > API > คัดลอก URL และ anon/public key
    4. สร้างไฟล์ `.streamlit/secrets.toml` แล้วใส่:
    ```
    SUPABASE_URL = "your-project-url"
    SUPABASE_KEY = "your-anon-key"
    ```
    """)
    st.stop()

# เชื่อมต่อ Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- การตั้งค่าเบื้องต้น ---
st.set_page_config(page_title="ระบบดาวน์โหลดเกียรติบัตร (Cloud Version)", layout="wide")

# --- ฟังก์ชันจัดการฐานข้อมูล Supabase ---
def init_db():
    """
    สร้างตารางใน Supabase (ทำครั้งเดียวตอนแรก)
    หรือใช้ Supabase Dashboard สร้างตารางด้วย SQL:

    CREATE TABLE events (
        id BIGSERIAL PRIMARY KEY,
        event_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );

    CREATE TABLE certificates (
        id BIGSERIAL PRIMARY KEY,
        event_id BIGINT REFERENCES events(id),
        name TEXT NOT NULL,
        file_path TEXT NOT NULL
    );
    """
    try:
        # ตรวจสอบว่าตารางมีอยู่แล้วหรือไม่
        response = supabase.table('events').select("*").limit(1).execute()
        return True
    except Exception as e:
        st.warning(f"⚠️ กรุณาสร้างตารางใน Supabase Database ก่อน: {str(e)}")
        st.code("""
-- คัดลอก SQL นี้ไปรันใน Supabase SQL Editor:

CREATE TABLE IF NOT EXISTS events (
    id BIGSERIAL PRIMARY KEY,
    event_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS certificates (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT REFERENCES events(id),
    name TEXT NOT NULL,
    file_path TEXT NOT NULL
);
        """, language="sql")
        return False

def add_event(event_name):
    """เพิ่มกิจกรรมใหม่"""
    response = supabase.table('events').insert({
        "event_name": event_name,
        "created_at": datetime.now().isoformat()
    }).execute()
    return response.data[0]['id']

def save_certificate_entry(event_id, name, file_path):
    """บันทึกข้อมูลเกียรติบัตรลง Database"""
    supabase.table('certificates').insert({
        "event_id": event_id,
        "name": name,
        "file_path": file_path
    }).execute()

def get_events():
    """ดึงรายการกิจกรรมทั้งหมด"""
    response = supabase.table('events').select("*").order('id', desc=True).execute()
    return pd.DataFrame(response.data)

def search_certificates(event_id, search_name):
    """ค้นหาเกียรติบัตรตามชื่อ"""
    response = supabase.table('certificates').select("*").eq('event_id', event_id).ilike('name', f'%{search_name}%').execute()
    return pd.DataFrame(response.data)

def upload_file_to_supabase(file_bytes, file_name, bucket_name="certificates"):
    """
    อัพโหลดไฟล์ไปยัง Supabase Storage

    ⚠️ ต้องสร้าง Storage Bucket ชื่อ 'certificates' ใน Supabase ก่อน
    และตั้งค่าเป็น Public หรือ Private ตามต้องการ
    """
    try:
        # อัพโหลดไฟล์
        response = supabase.storage.from_(bucket_name).upload(
            file_name,
            file_bytes,
            file_options={"content-type": "application/pdf", "upsert": "true"}
        )

        # สร้าง Public URL (ถ้า bucket เป็น public)
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
        return public_url
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอัพโหลด: {str(e)}")
        return None

def download_file_from_supabase(file_path, bucket_name="certificates"):
    """ดาวน์โหลดไฟล์จาก Supabase Storage"""
    try:
        # แยกชื่อไฟล์จาก URL
        file_name = file_path.split('/')[-1]
        response = supabase.storage.from_(bucket_name).download(file_name)
        return response
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการดาวน์โหลด: {str(e)}")
        return None

def sanitize_filename(filename):
    """ลบอักขระพิเศษออกจากชื่อไฟล์"""
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '-', '_', '.')]).rstrip()

# --- เริ่มต้นระบบ ---
db_ready = init_db()

# --- ส่วนติดต่อผู้ใช้ (UI) ---
st.title("🎓 ระบบดาวน์โหลดเกียรติบัตรออนไลน์ (Cloud Version)")
st.caption("✅ รองรับการใช้งานบน Cloud โดยใช้ Supabase (PostgreSQL + Storage)")

if not db_ready:
    st.stop()

# สร้าง Tabs แยกฝั่ง Admin และ User
tab1, tab2 = st.tabs(["🔍 สำหรับผู้ใช้งาน (User)", "🛠️ สำหรับผู้ดูแลระบบ (Admin)"])

# ==========================================
# 🟢 ส่วนของ USER: ค้นหาและดาวน์โหลด
# ==========================================
with tab1:
    st.header("ค้นหาเกียรติบัตรของคุณ")

    events_df = get_events()

    if events_df.empty:
        st.info("ยังไม่มีรายการกิจกรรมในระบบ")
    else:
        # 1. เลือกกิจกรรม
        event_options = dict(zip(events_df['id'], events_df['event_name']))
        selected_event_id = st.selectbox("เลือกโครงการอบรม / กิจกรรม", options=list(event_options.keys()), format_func=lambda x: event_options[x])

        # 2. ช่องค้นหาชื่อ
        search_query = st.text_input("ระบุชื่อ-นามสกุล ของคุณ (ไม่ต้องใส่คำนำหน้า)", placeholder="ตัวอย่าง: สมชาย ใจดี")

        if st.button("ค้นหา", type="primary"):
            if search_query:
                results = search_certificates(selected_event_id, search_query)

                if not results.empty:
                    st.success(f"พบข้อมูลจำนวน {len(results)} รายการ")
                    for index, row in results.iterrows():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"📄 **คุณ{row['name']}**")
                        with col2:
                            # ดาวน์โหลดไฟล์จาก Supabase Storage
                            file_name = row['file_path'].split('/')[-1] if '/' in row['file_path'] else row['file_path']

                            try:
                                file_bytes = download_file_from_supabase(file_name)
                                if file_bytes:
                                    st.download_button(
                                        label="ดาวน์โหลด PDF",
                                        data=file_bytes,
                                        file_name=file_name,
                                        mime="application/pdf",
                                        key=f"dl_{row['id']}"
                                    )
                                else:
                                    st.error("ไม่สามารถดาวน์โหลดไฟล์ได้")
                            except Exception as e:
                                st.error(f"เกิดข้อผิดพลาด: {str(e)}")
                else:
                    st.warning("ไม่พบรายชื่อนี้ในระบบ กรุณาตรวจสอบการสะกดคำ หรือเลือกกิจกรรมให้ถูกต้อง")
            else:
                st.warning("กรุณากรอกชื่อเพื่อค้นหา")

# ==========================================
# 🔴 ส่วนของ ADMIN: เพิ่มข้อมูลและประมวลผลไฟล์
# ==========================================
with tab2:
    st.header("จัดการข้อมูลเกียรติบัตร")

    # แสดงคำเตือนเรื่อง Storage Bucket
    with st.expander("⚠️ คำเตือน: ต้องสร้าง Storage Bucket ก่อนใช้งาน"):
        st.markdown("""
        **ขั้นตอนการสร้าง Storage Bucket ใน Supabase:**
        1. ไปที่ Supabase Dashboard > Storage
        2. คลิก "New Bucket"
        3. ตั้งชื่อว่า `certificates`
        4. เลือก **Public** (ถ้าต้องการให้ดาวน์โหลดได้โดยตรง) หรือ **Private** (ถ้าต้องการควบคุมการเข้าถึง)
        5. คลิก "Create bucket"
        """)

    st.subheader("1. สร้างกิจกรรมใหม่")
    new_event_name = st.text_input("ชื่อโครงการ / การอบรม")

    st.subheader("2. อัปโหลดไฟล์รายชื่อ (Excel)")
    uploaded_excel = st.file_uploader("อัปโหลดไฟล์รายชื่อ (.xlsx)", type=['xlsx'])

    st.subheader("3. อัปโหลดไฟล์เกียรติบัตร (PDF รวม)")
    uploaded_pdf = st.file_uploader("อัปโหลดไฟล์ PDF รวม (.pdf)", type=['pdf'])

    if uploaded_excel is not None:
        # อ่านไฟล์ Excel เพื่อให้ Admin เลือกคอลัมน์ชื่อ
        df_preview = pd.read_excel(uploaded_excel)
        st.write("ตัวอย่างข้อมูลในไฟล์ Excel:")
        st.dataframe(df_preview.head(3))

        # เลือกคอลัมน์ที่เป็นชื่อ
        name_column = st.selectbox("เลือกคอลัมน์ที่เก็บ 'ชื่อ-นามสกุล' ของผู้รับ", df_preview.columns)

    # ปุ่มดำเนินการ
    if st.button("🚀 เริ่มประมวลผลและนำเข้าสู่ระบบ"):
        if not new_event_name or not uploaded_excel or not uploaded_pdf:
            st.error("กรุณากรอกชื่อกิจกรรม และอัปโหลดไฟล์ให้ครบถ้วน")
        else:
            try:
                # 1. สร้าง Event ใน DB
                event_id = add_event(new_event_name)
                st.info(f"✅ สร้างกิจกรรม ID: {event_id}")

                # 2. เตรียมอ่าน PDF
                pdf_reader = PdfReader(uploaded_pdf)
                total_pages = len(pdf_reader.pages)
                total_rows = len(df_preview)

                # ตรวจสอบจำนวนหน้า vs จำนวนรายชื่อ
                if total_pages != total_rows:
                    st.warning(f"⚠️ คำเตือน: จำนวนหน้า PDF ({total_pages}) ไม่เท่ากับจำนวนรายชื่อใน Excel ({total_rows}) ระบบจะประมวลผลตามจำนวนที่น้อยกว่า")

                limit = min(total_pages, total_rows)

                progress_bar = st.progress(0)
                status_text = st.empty()

                # 3. ลูปเพื่อตัดไฟล์ PDF ทีละหน้า
                for i in range(limit):
                    # ดึงชื่อจาก Excel
                    user_name = str(df_preview.iloc[i][name_column]).strip()
                    safe_name = sanitize_filename(user_name)

                    # ตัดหน้า PDF
                    pdf_writer = PdfWriter()
                    pdf_writer.add_page(pdf_reader.pages[i])

                    # เขียน PDF ลง Memory (BytesIO)
                    pdf_output = io.BytesIO()
                    pdf_writer.write(pdf_output)
                    pdf_output.seek(0)

                    # ตั้งชื่อไฟล์
                    output_filename = f"event_{event_id}/{i+1}_{safe_name}.pdf"

                    # 4. อัพโหลดไปยัง Supabase Storage
                    file_url = upload_file_to_supabase(pdf_output.read(), output_filename)

                    if file_url:
                        # 5. บันทึกลง Database
                        save_certificate_entry(event_id, user_name, output_filename)

                        # อัปเดต Progress
                        progress = (i + 1) / limit
                        progress_bar.progress(progress)
                        status_text.text(f"กำลังประมวลผล: {user_name} ({i+1}/{limit})")
                    else:
                        st.error(f"❌ ไม่สามารถอัพโหลดไฟล์ของ {user_name} ได้")

                st.success(f"✅ ประมวลผลเสร็จสิ้น! นำเข้าข้อมูล {limit} รายการเรียบร้อยแล้ว")
                st.balloons()

            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

st.markdown("---")
st.caption("ระบบแยกไฟล์เกียรติบัตรอัตโนมัติ (Cloud Version) | พัฒนาด้วย Python, Streamlit & Supabase")
