CREATE OR REPLACE PROCEDURE cargar_ventas_mensuales(
    p_id_periodo INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_sin_marca INTEGER;
    v_sin_modelo INTEGER;
    v_registros INTEGER;
	v_marcas_faltantes TEXT;
BEGIN

    -- ========================================================
    -- 1. VALIDAR QUE EL PERÍODO EXISTA
    -- ========================================================

    IF NOT EXISTS (
        SELECT 1
        FROM dim_fecha
        WHERE id_periodo = p_id_periodo
    ) THEN

        RAISE EXCEPTION
            'El período % no existe en dim_fecha.',
            p_id_periodo;

    END IF;


    -- ========================================================
    -- 2. VALIDAR QUE TODAS LAS MARCAS EXISTAN
    -- ========================================================
    -- No creamos marcas automáticamente.
    --
    -- Si aparece:
    --     Nueva Nissan Kicks
    --
    -- "Nueva" no existe en dim_marca y la carga se detiene.
    --
    -- Esto evita contaminar la dimensión por errores del CSV.
    -- ========================================================

	SELECT COUNT(*)
	INTO v_sin_marca
	FROM stg_ventas_mensuales s
	LEFT JOIN dim_marca m
	    ON SPLIT_PART(TRIM(s.vehiculo), ' ', 1) = m.marca
	WHERE TRIM(s.vehiculo) <> ''
	  AND m.id_marca IS NULL;
	
	IF v_sin_marca > 0 THEN
	
	    SELECT STRING_AGG(
	        marca_faltante || ' → ' || vehiculos,
	        E'\n'
	        ORDER BY marca_faltante
	    )
	    INTO v_marcas_faltantes
	    FROM (
	        SELECT
	            SPLIT_PART(TRIM(s.vehiculo), ' ', 1) AS marca_faltante,
	            STRING_AGG(
	                TRIM(s.vehiculo),
	                ', '
	                ORDER BY TRIM(s.vehiculo)
	            ) AS vehiculos
	        FROM stg_ventas_mensuales s
	        LEFT JOIN dim_marca m
	            ON SPLIT_PART(TRIM(s.vehiculo), ' ', 1) = m.marca
	        WHERE TRIM(s.vehiculo) <> ''
	          AND m.id_marca IS NULL
	        GROUP BY SPLIT_PART(TRIM(s.vehiculo), ' ', 1)
	    ) AS faltantes;
	
	    RAISE EXCEPTION
	        E'La carga fue detenida: % vehículos contienen marcas no existentes en dim_marca.\n\nMarcas y vehículos afectados:\n%',
	        v_sin_marca,
	        v_marcas_faltantes;
	
	END IF;


    -- ========================================================
    -- 3. INSERTAR MODELOS NUEVOS
    -- ========================================================
    -- La marca ya fue validada.
    --
    -- Ejemplo:
    -- Tesla Model Y
    --
    -- marca  = Tesla
    -- modelo = Model Y
    -- ========================================================

    INSERT INTO dim_modelo (
        id_marca,
        modelo
    )
    SELECT DISTINCT
        m.id_marca,
        TRIM(
            SUBSTRING(
                s.vehiculo
                FROM LENGTH(m.marca) + 1
            )
        ) AS modelo
    FROM stg_ventas_mensuales s
    JOIN dim_marca m
        ON SPLIT_PART(TRIM(s.vehiculo), ' ', 1) = m.marca
    WHERE TRIM(
        SUBSTRING(
            s.vehiculo
            FROM LENGTH(m.marca) + 1
        )
    ) <> ''
    ON CONFLICT (id_marca, modelo) DO NOTHING;


    -- ========================================================
    -- 4. VALIDAR QUE TODOS LOS MODELOS EXISTAN
    -- ========================================================

    SELECT COUNT(*)
    INTO v_sin_modelo
    FROM stg_ventas_mensuales s
    JOIN dim_marca m
        ON SPLIT_PART(TRIM(s.vehiculo), ' ', 1) = m.marca
    LEFT JOIN dim_modelo mo
        ON mo.id_marca = m.id_marca
        AND mo.modelo = TRIM(
            SUBSTRING(
                s.vehiculo
                FROM LENGTH(m.marca) + 1
            )
        )
    WHERE mo.id_modelo IS NULL;


    IF v_sin_modelo > 0 THEN

        RAISE EXCEPTION
            'La carga fue detenida: % vehículos no pudieron asociarse a un modelo.',
            v_sin_modelo;

    END IF;


    -- ========================================================
    -- 5. ELIMINAR EL PERÍODO SI YA EXISTE
    -- ========================================================
    -- Esto permite corregir y volver a cargar un CSV.
    --
    -- Ejemplo:
    --
    -- Junio incorrecto
    --       ↓
    -- corregimos CSV
    --       ↓
    -- CALL cargar_ventas_mensuales(202606)
    --       ↓
    -- se elimina junio anterior
    --       ↓
    -- se carga junio corregido
    -- ========================================================

    DELETE FROM fact_ventas_mensuales
    WHERE id_periodo = p_id_periodo;


    -- ========================================================
    -- 6. INSERTAR EL PERÍODO COMPLETO
    -- ========================================================

    INSERT INTO fact_ventas_mensuales (
        id_periodo,
        id_modelo,
        unidades_vendidas
    )
    SELECT
        p_id_periodo,
        mo.id_modelo,
        s.unidades_vendidas::INTEGER
    FROM stg_ventas_mensuales s
    JOIN dim_marca m
        ON SPLIT_PART(TRIM(s.vehiculo), ' ', 1) = m.marca
    JOIN dim_modelo mo
        ON mo.id_marca = m.id_marca
        AND mo.modelo = TRIM(
            SUBSTRING(
                s.vehiculo
                FROM LENGTH(m.marca) + 1
            )
        );


    -- ========================================================
    -- 7. VALIDACIÓN FINAL
    -- ========================================================

    SELECT COUNT(*)
    INTO v_registros
    FROM fact_ventas_mensuales
    WHERE id_periodo = p_id_periodo;


    RAISE NOTICE '============================================';
    RAISE NOTICE 'Carga completada correctamente.';
    RAISE NOTICE 'Período: %', p_id_periodo;
    RAISE NOTICE 'Registros cargados: %', v_registros;
    RAISE NOTICE '============================================';

END;
$$;