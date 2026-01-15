-- ============================================
-- Database Setup V2 - Google Drive Version
-- สำหรับระบบดาวน์โหลดเกียรติบัตร
-- ============================================

-- ลบตารางเก่า (ถ้ามี)
DROP TABLE IF EXISTS certificates CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS admin_users CASCADE;

-- ============================================
-- ตาราง admin_users (สำหรับ Login)
-- ============================================
CREATE TABLE admin_users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE admin_users IS 'ตารางเก็บข้อมูล Admin สำหรับ Login';

-- สร้าง Admin เริ่มต้น (username: admin, password: admin123)
-- Password hash ของ "admin123" (ใช้ SHA256)
INSERT INTO admin_users (username, password_hash, full_name) VALUES
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'ผู้ดูแลระบบ');

-- ============================================
-- ตาราง events (รายการกิจกรรม)
-- ============================================
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_name TEXT NOT NULL,
    google_drive_folder_link TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by TEXT
);

COMMENT ON TABLE events IS 'ตารางเก็บรายการกิจกรรม/โครงการที่มีการแจกเกียรติบัตร';
COMMENT ON COLUMN events.google_drive_folder_link IS 'ลิงค์โฟลเดอร์ Google Drive ที่เก็บไฟล์ PDF';

-- ============================================
-- ตาราง certificates (เกียรติบัตร)
-- ============================================
CREATE TABLE certificates (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    order_number INTEGER NOT NULL,
    google_drive_file_link TEXT NOT NULL,
    file_name TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE certificates IS 'ตารางเก็บข้อมูลเกียรติบัตรของแต่ละคน (เชื่อมกับ Google Drive)';
COMMENT ON COLUMN certificates.order_number IS 'ลำดับที่ (ตรงกับลำดับใน Excel)';
COMMENT ON COLUMN certificates.google_drive_file_link IS 'ลิงค์ไฟล์ PDF ใน Google Drive';

-- ============================================
-- สร้าง Index เพื่อเพิ่มความเร็วในการค้นหา
-- ============================================
CREATE INDEX idx_certificates_event_id ON certificates(event_id);
CREATE INDEX idx_certificates_name ON certificates(name);
CREATE INDEX idx_certificates_order ON certificates(order_number);
CREATE INDEX idx_events_created_at ON events(created_at DESC);
CREATE INDEX idx_admin_username ON admin_users(username);

-- ============================================
-- เพิ่มข้อมูลตัวอย่าง (สำหรับทดสอบ)
-- ============================================
INSERT INTO events (event_name, description) VALUES
    ('โครงการอบรมตัวอย่าง 2026', 'กิจกรรมทดสอบระบบ');

-- ============================================
-- แสดงผลลัพธ์
-- ============================================
SELECT 'Database V2 setup completed successfully!' as status;

SELECT 'Created ' || count(*) || ' admin users' as admin_count
FROM admin_users;

SELECT 'Created ' || count(*) || ' events' as events_count
FROM events;

SELECT 'Default admin username: admin' as note1;
SELECT 'Default admin password: admin123' as note2;
SELECT 'Please change the password after first login!' as important_note;
