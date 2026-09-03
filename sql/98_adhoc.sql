-- Tablas dimensionales y de hechos
SELECT * FROM fact_ventas_mensuales;
SELECT * FROM dim_fecha;
SELECT * FROM dim_marca -- WHERE marca LIKE 'BYD';
SELECT * FROM dim_modelo ORDER BY modelo ASC;
SELECT * FROM dim_marca ORDER BY marca ASC;


-- Inserción de marcas nuevas (si existe)
INSERT INTO dim_marca(marca)
VALUES 
	('Cupra')
;


-- truncado de tabla stage
TRUNCATE TABLE stg_ventas_mensuales;


-- Llamado de SP
CALL cargar_ventas_mensuales(202608);


-- Consulta ad hoc
SELECT 
	da.marca,
	dm.modelo,
	SUM(fm.unidades_vendidas) AS unidades_totales,
	SUM(fm.unidades_vendidas) / COUNT(DISTINCT(id_periodo)) AS uni_mes_prom,
	COUNT(DISTINCT(id_periodo)) AS meses_totales
FROM fact_ventas_mensuales AS fm
LEFT JOIN dim_modelo AS dm
	ON dm.id_modelo=fm.id_modelo
LEFT JOIN dim_marca AS da
	ON da.id_marca=dm.id_marca
GROUP BY 
	dm.modelo,
	da.marca
ORDER BY
	unidades_totales DESC
;