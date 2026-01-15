-- ============================================
-- Supabase Storage Policies Setup
-- สำหรับระบบดาวน์โหลดเกียรติบัตร
-- ============================================

-- ลบ Policies เก่า (ถ้ามี)
DROP POLICY IF EXISTS "Allow public read access" ON storage.objects;
DROP POLICY IF EXISTS "Allow public upload" ON storage.objects;
DROP POLICY IF EXISTS "Allow public update" ON storage.objects;
DROP POLICY IF EXISTS "Allow public delete" ON storage.objects;

-- ============================================
-- Policy 1: อนุญาตให้อ่าน/ดาวน์โหลดได้ทุกคน
-- ============================================
CREATE POLICY "Allow public read access"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'certificates');

-- ============================================
-- Policy 2: อนุญาตให้อัพโหลดได้ทุกคน
-- ============================================
CREATE POLICY "Allow public upload"
ON storage.objects FOR INSERT
TO public
WITH CHECK (bucket_id = 'certificates');

-- ============================================
-- Policy 3: อนุญาตให้อัพเดตได้ทุกคน
-- ============================================
CREATE POLICY "Allow public update"
ON storage.objects FOR UPDATE
TO public
USING (bucket_id = 'certificates')
WITH CHECK (bucket_id = 'certificates');

-- ============================================
-- Policy 4: อนุญาตให้ลบได้ทุกคน (ถ้าต้องการ)
-- ============================================
-- หมายเหตุ: ถ้าไม่ต้องการให้ลบได้ ให้ comment บรรทัดนี้ออก
CREATE POLICY "Allow public delete"
ON storage.objects FOR DELETE
TO public
USING (bucket_id = 'certificates');

-- ============================================
-- แสดงผลลัพธ์
-- ============================================
SELECT '✅ Storage Policies created successfully!' as status;

-- แสดง Policies ที่ถูกสร้าง
SELECT
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd
FROM pg_policies
WHERE tablename = 'objects'
AND schemaname = 'storage'
ORDER BY policyname;

SELECT '✅ You can now upload and download files from the certificates bucket!' as final_message;
