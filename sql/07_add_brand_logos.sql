-- ==========================================
-- LOGOS DE MARCA EN SUPABASE STORAGE
-- ==========================================
-- Bucket público: brand-logos
-- URL: https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/{archivo}
--
-- Los archivos se suben con scripts/upload_brand_logos.py.
-- Este script crea el bucket, sube assets/logos/ y aplica el UPDATE de abajo.
-- Ejecutar este SQL a mano antes de subir los archivos deja los logos rotos.
-- ==========================================

INSERT INTO storage.buckets (id, name, public)
VALUES ('brand-logos', 'brand-logos', true)
ON CONFLICT (id) DO UPDATE SET public = EXCLUDED.public;

DROP POLICY IF EXISTS "Lectura publica logos" ON storage.objects;
CREATE POLICY "Lectura publica logos"
ON storage.objects
FOR SELECT
TO public
USING (bucket_id = 'brand-logos');

UPDATE dim_marca SET url_logo = CASE marca
    WHEN 'BMW'        THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/bmw.png'
    WHEN 'BYD'        THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/byd.png'
    WHEN 'Chevrolet'  THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/chevrolet.png'
    WHEN 'Citroën'    THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/citroen.png'
    WHEN 'Cupra'      THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/cupra.png'
    WHEN 'Ford'       THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/ford.png'
    WHEN 'Honda'      THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/honda.png'
    WHEN 'Hyundai'    THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/hyundai.png'
    WHEN 'Jeep'       THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/jeep.png'
    WHEN 'Kia'        THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/kia.png'
    WHEN 'Mazda'      THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/mazda.png'
    WHEN 'MG'         THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/mg.png'
    WHEN 'Nissan'     THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/Nissan.png'
    WHEN 'Peugeot'    THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/peugeot.png'
    WHEN 'RAM'        THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/ram.png'
    WHEN 'Renault'    THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/renault.png'
    WHEN 'Subaru'     THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/subaru.png'
    WHEN 'Suzuki'     THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/suzuki.png'
    WHEN 'Tesla'      THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/tesla.png'
    WHEN 'Toyota'     THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/toyota.png'
    WHEN 'Volkswagen' THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/volkswagen.png'
    WHEN 'Chery'      THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/chery.png'
    WHEN 'Deepal'     THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/deepal.png'
    WHEN 'Dongfeng'   THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/dongfeng.png'
    WHEN 'GAC'        THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/gac.png'
    WHEN 'Geely'      THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/geely.png'
    WHEN 'GWM'        THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/gwm.png'
    WHEN 'Foton'      THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/foton.png'
    WHEN 'JAC'        THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/jac.png'
    WHEN 'JMC'        THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/jmc.png'
    WHEN 'Kenworth'   THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/kenworth.png'
    WHEN 'Daewoo'     THEN 'https://mhmyufztulogrljlyyuy.supabase.co/storage/v1/object/public/brand-logos/daewoo.png'
    WHEN 'FRR'        THEN NULL
    ELSE NULL
END;
