-- Validación final
SELECT
    f.id_periodo,
    m.marca,
    mo.modelo,
    CONCAT_WS(' ', m.marca, mo.modelo) AS vehiculo,
    f.unidades_vendidas
FROM fact_ventas_mensuales f
JOIN dim_modelo mo
    ON f.id_modelo = mo.id_modelo
JOIN dim_marca m
    ON mo.id_marca = m.id_marca
ORDER BY mo.modelo ASC;