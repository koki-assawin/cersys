import streamlit as st
import pandas as pd
import sqlite3
import os
from pypdf import PdfReader, PdfWriter
import shutil
from datetime import datetime

# --- การตั้งค่าเบื้องต้น ---
st.set_page_config(page_title="ระบบดาวน์โหลดเกียรติบัตร", layout="wide")
UPLOAD_FOLDER = "certificates_storage"
DB_FILE = "certificate_db.sqlite"

# สร้างโฟลเดอร์เก็บไฟล์ถ้ายังไม่มี
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- ส่วนจัดการฐานข้อมูล (Database) ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # ตารางกิจกรรม (Events)
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_name TEXT,
                  created_at TEXT)''')
    # ตารางเกียรติบัตร (Certificates)
    c.execute('''CREATE TABLE IF NOT EXISTS certificates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_id INTEGER,
                  name TEXT,
                  file_path TEXT,
                  FOREIGN KEY(event_id) REFERENCES events(id))''')
    conn.commit()
    conn.close()

def add_event(event_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO events (event_name, created_at) VALUES (?, ?)", 
              (event_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    event_id = c.lastrowid
    conn.commit()
    conn.close()
    return event_id

def save_certificate_entry(event_id, name, file_path):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO certificates (event_id, name, file_path) VALUES (?, ?, ?)", 
              (event_id, name, file_path))
    conn.commit()
    conn.close()

def get_events():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM events ORDER BY id DESC", conn)
    conn.close()
    return df

def search_certificates(event_id, search_name):
    conn = sqlite3.connect(DB_FILE)
    query = "SELECT * FROM certificates WHERE event_id = ? AND name LIKE ?"
    df = pd.read_sql_query(query, conn, params=(event_id, f'%{search_name}%'))
    conn.close()
    return df

def sanitize_filename(filename):
    # ลบอักขระพิเศษออกจากชื่อไฟล์เพื่อป้องกัน error
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).rstrip()

# --- เริ่มต้นระบบ ---
init_db()

# --- ส่วนติดต่อผู้ใช้ (UI) ---
st.title("🎓 ระบบดาวน์โหลดเกียรติบัตรออนไลน์")

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
                            # อ่านไฟล์เพื่อเตรียมดาวน์โหลด
                            if os.path.exists(row['file_path']):
                                with open(row['file_path'], "rb") as file:
                                    st.download_button(
                                        label="ดาวน์โหลด PDF",
                                        data=file,
                                        file_name=os.path.basename(row['file_path']),
                                        mime="application/pdf",
                                        key=f"dl_{row['id']}"
                                    )
                            else:
                                st.error("ไม่พบไฟล์ต้นฉบับ")
                else:
                    st.warning("ไม่พบรายชื่อนี้ในระบบ กรุณาตรวจสอบการสะกดคำ หรือเลือกกิจกรรมให้ถูกต้อง")
            else:
                st.warning("กรุณากรอกชื่อเพื่อค้นหา")

# ==========================================
# 🔴 ส่วนของ ADMIN: เพิ่มข้อมูลและประมวลผลไฟล์
# ==========================================
with tab2:
    st.header("จัดการข้อมูลเกียรติบัตร")
    
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
                
                # 2. สร้างโฟลเดอร์สำหรับ Event นี้
                event_folder = os.path.join(UPLOAD_FOLDER, str(event_id))
                os.makedirs(event_folder, exist_ok=True)
                
                # 3. เตรียมอ่าน PDF
                pdf_reader = PdfReader(uploaded_pdf)
                total_pages = len(pdf_reader.pages)
                total_rows = len(df_preview)
                
                # ตรวจสอบจำนวนหน้า vs จำนวนรายชื่อ
                if total_pages != total_rows:
                    st.warning(f"⚠️ คำเตือน: จำนวนหน้า PDF ({total_pages}) ไม่เท่ากับจำนวนรายชื่อใน Excel ({total_rows}) ระบบจะประมวลผลตามจำนวนที่น้อยกว่า")
                
                limit = min(total_pages, total_rows)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 4. ลูปเพื่อตัดไฟล์ PDF ทีละหน้า
                for i in range(limit):
                    # ดึงชื่อจาก Excel
                    user_name = str(df_preview.iloc[i][name_column]).strip()
                    safe_name = sanitize_filename(user_name)
                    
                    # ตัดหน้า PDF
                    pdf_writer = PdfWriter()
                    pdf_writer.add_page(pdf_reader.pages[i])
                    
                    # ตั้งชื่อไฟล์และบันทึก
                    output_filename = f"{i+1}_{safe_name}.pdf"
                    output_path = os.path.join(event_folder, output_filename)
                    
                    with open(output_path, "wb") as out_file:
                        pdf_writer.write(out_file)
                    
                    # 5. บันทึกลง DB
                    save_certificate_entry(event_id, user_name, output_path)
                    
                    # อัปเดต Progress
                    progress = (i + 1) / limit
                    progress_bar.progress(progress)
                    status_text.text(f"กำลังประมวลผล: {user_name} ({i+1}/{limit})")
                
                st.success(f"✅ ประมวลผลเสร็จสิ้น! นำเข้าข้อมูล {limit} รายการเรียบร้อยแล้ว")
                st.balloons()
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")

st.markdown("---")
st.caption("ระบบแยกไฟล์เกียรติบัตรอัตโนมัติ | พัฒนาด้วย Python & Streamlit")