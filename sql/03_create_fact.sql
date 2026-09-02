-- ============================================================
-- FACT: VENTAS MENSUALES DE VEHÍCULOS
-- ============================================================

CREATE TABLE fact_ventas_mensuales (
    id_periodo INTEGER NOT NULL,
    id_modelo INTEGER NOT NULL,
    unidades_vendidas INTEGER NOT NULL,

    -- Llave primaria compuesta:
    -- un modelo solo puede tener un registro por período
    CONSTRAINT pk_fact_ventas_mensuales
        PRIMARY KEY (id_periodo, id_modelo),

    -- Relación con la dimensión de fechas
    CONSTRAINT fk_fact_periodo
        FOREIGN KEY (id_periodo)
        REFERENCES dim_fecha(id_periodo),

    -- Relación con la dimensión de modelos
    CONSTRAINT fk_fact_modelo
        FOREIGN KEY (id_modelo)
        REFERENCES dim_modelo(id_modelo),

    -- Validación de unidades
    CONSTRAINT chk_unidades_vendidas
        CHECK (unidades_vendidas >= 0)
);