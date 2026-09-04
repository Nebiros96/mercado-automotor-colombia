-- ==========================================
-- ACTUALIZAR LOGOS POR MARCA
-- ==========================================
-- Fuente: Tomba Logo API (gratis, sin API key)
-- Formato: https://logo.tomba.io/{dominio}
-- ==========================================

UPDATE dim_marca SET url_logo = CASE marca
    -- Marcas globales
    WHEN 'BMW'        THEN 'https://logo.tomba.io/bmw.com'
    WHEN 'BYD'        THEN 'https://logo.tomba.io/byd.com'
    WHEN 'Chevrolet'  THEN 'https://logo.tomba.io/chevrolet.com'
    WHEN 'Citroën'    THEN 'https://logo.tomba.io/citroen.com'
    WHEN 'Cupra'      THEN 'https://logo.tomba.io/cupraofficial.com'
    WHEN 'Ford'       THEN 'https://logo.tomba.io/ford.com'  -- No aparece
    WHEN 'Honda'      THEN 'https://logo.tomba.io/honda.com'
    WHEN 'Hyundai'    THEN 'https://logo.tomba.io/hyundai.com'
    WHEN 'Jeep'       THEN 'https://logo.tomba.io/jeep.com'
    WHEN 'Kia'        THEN 'https://logo.tomba.io/kia.com'
    WHEN 'Mazda'      THEN 'https://logo.tomba.io/mazda.com'
    WHEN 'MG'         THEN 'https://logo.tomba.io/mgmotor.com'  -- Cambiar
    WHEN 'Nissan'     THEN 'https://logo.tomba.io/nissan.com'  -- Cambiar
    WHEN 'Peugeot'    THEN 'https://logo.tomba.io/peugeot.com'
    WHEN 'RAM'        THEN 'https://logo.tomba.io/ramtrucks.com'
    WHEN 'Renault'    THEN 'https://logo.tomba.io/renault.com'  -- Cambiar
    WHEN 'Subaru'     THEN 'https://logo.tomba.io/subaru.com'
    WHEN 'Suzuki'     THEN 'https://logo.tomba.io/suzuki.com'
    WHEN 'Tesla'      THEN 'https://logo.tomba.io/tesla.com'
    WHEN 'Toyota'     THEN 'https://logo.tomba.io/toyota.com'
    WHEN 'Volkswagen' THEN 'https://logo.tomba.io/volkswagen.com'

    -- Marcas chinas / asiáticas
    WHEN 'Chery'      THEN 'https://logo.tomba.io/cheryinternational.com'
    WHEN 'Deepal'     THEN 'https://logo.tomba.io/deepal.com'  -- Cambiar
    WHEN 'Dongfeng'   THEN 'https://logo.tomba.io/dongfeng-global.com'
    WHEN 'GAC'        THEN 'https://logo.tomba.io/gac-motor.com'
    WHEN 'Geely'      THEN 'https://logo.tomba.io/geely.com'  -- Cambiar
    WHEN 'GWM'        THEN 'https://logo.tomba.io/gwm-global.com'

    -- Vehículos comerciales / camiones
    WHEN 'Foton'      THEN 'https://logo.tomba.io/foton-global.com'
    WHEN 'JAC'        THEN 'https://logo.tomba.io/jacmotors.com'
    WHEN 'JMC'        THEN 'https://logo.tomba.io/jmc.com.cn'
    WHEN 'Kenworth'   THEN 'https://logo.tomba.io/kenworth.com'

    -- Marcas sin logo disponible (revisar manualmente)
    WHEN 'Daewoo'     THEN NULL
    WHEN 'FRR'        THEN NULL

    ELSE NULL
END;