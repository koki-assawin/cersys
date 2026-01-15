-- ============================================
-- Supabase Database Setup Script
-- สำหรับระบบดาวน์โหลดเกียรติบัตร
-- ============================================

-- ลบตารางเก่า (ถ้ามี) เพื่อเริ่มต้นใหม่
DROP TABLE IF EXISTS certificates CASCADE;
DROP TABLE IF EXISTS events CASCADE;

-- ============================================
-- สร้างตาราง events (รายการกิจกรรม/โครงการ)
-- ============================================
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE events IS 'ตารางเก็บรายการกิจกรรม/โครงการที่มีการแจกเกียรติบัตร';
COMMENT ON COLUMN events.id IS 'รหัสกิจกรรม (Primary Key)';
COMMENT ON COLUMN events.event_name IS 'ชื่อกิจกรรม/โครงการ';
COMMENT ON COLUMN events.created_at IS 'วันเวลาที่สร้าง';

-- ============================================
-- สร้างตาราง certificates (เกียรติบัตร)
-- ============================================
CREATE TABLE certificates (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE certificates IS 'ตารางเก็บข้อมูลเกียรติบัตรของแต่ละคน';
COMMENT ON COLUMN certificates.id IS 'รหัสเกียรติบัตร (Primary Key)';
COMMENT ON COLUMN certificates.event_id IS 'รหัสกิจกรรม (Foreign Key)';
COMMENT ON COLUMN certificates.name IS 'ชื่อ-นามสกุลผู้รับเกียรติบัตร';
COMMENT ON COLUMN certificates.file_path IS 'ตำแหน่งไฟล์ใน Storage';
COMMENT ON COLUMN certificates.created_at IS 'วันเวลาที่สร้าง';

-- ============================================
-- สร้าง Index เพื่อเพิ่มความเร็วในการค้นหา
-- ============================================
CREATE INDEX idx_certificates_event_id ON certificates(event_id);
CREATE INDEX idx_certificates_name ON certificates(name);
CREATE INDEX idx_events_created_at ON events(created_at DESC);

-- ============================================
-- เพิ่มข้อมูลตัวอย่าง (สำหรับทดสอบ)
-- ============================================
INSERT INTO events (event_name) VALUES
    ('โครงการอบรมทดสอบระบบ'),
    ('การอบรมตัวอย่าง 2026');

INSERT INTO certificates (event_id, name, file_path) VALUES
    (1, 'สมชาย ใจดี', 'event_1/1_สมชาย_ใจดี.pdf'),
    (1, 'สมหญิง รักดี', 'event_1/2_สมหญิง_รักดี.pdf'),
    (2, 'ทดสอบ ระบบ', 'event_2/1_ทดสอบ_ระบบ.pdf');

-- ============================================
-- แสดงผลลัพธ์
-- ============================================
SELECT 'Database setup completed successfully!' as status;

SELECT
    'Created ' || count(*) || ' events' as events_count
FROM events;

SELECT
    'Created ' || count(*) || ' certificates' as certificates_count
FROM certificates;

-- แสดงข้อมูลทั้งหมด
SELECT
    e.id as event_id,
    e.event_name,
    count(c.id) as certificate_count
FROM events e
LEFT JOIN certificates c ON e.id = c.event_id
GROUP BY e.id, e.event_name
ORDER BY e.id;

SELECT '✅ Setup complete! You can now run the app.' as final_message;
