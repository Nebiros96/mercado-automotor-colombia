# Mercado Automotor de Colombia

Proyecto de análisis de ventas mensuales de vehículos nuevos en Colombia, construido a partir de información de matriculaciones y estructurado bajo un modelo dimensional para facilitar su análisis posterior en herramientas de Business Intelligence.

## Descripción

Este proyecto tiene como objetivo consolidar y analizar la evolución mensual del mercado automotor colombiano, incluyendo las unidades vendidas por marca y modelo.

La información se almacena en una base de datos PostgreSQL y se organiza mediante un modelo dimensional compuesto por tablas de dimensiones y una tabla de hechos.

El proceso de carga está diseñado para incorporar nuevos períodos mensuales mediante archivos CSV, utilizando una tabla de staging y un procedimiento almacenado encargado de realizar las validaciones y transformaciones necesarias.

## Arquitectura

El flujo de datos sigue la siguiente estructura:

CSV mensual
   ↓
stg_ventas_mensuales
   ↓
dim_marca
   ↓
dim_modelo
   ↓
fact_ventas_mensuales
   ↓
Análisis / Power BI

## Modelo de datos

### Dimensiones

**dim_fecha**

Contiene la información temporal a nivel mensual:

- Período (`YYYYMM`)
- Fecha
- Año
- Mes
- Trimestre
- Semestre
- Año-mes

**dim_marca**

Catálogo de marcas presentes en el mercado automotor.

**dim_modelo**

Catálogo de modelos asociados a cada marca.

### Tabla de hechos

**fact_ventas_mensuales**

Contiene las unidades vendidas por modelo y período.

La granularidad de la tabla es:

> Un registro por modelo y mes.

Campos principales:

- `id_periodo`
- `id_modelo`
- `unidades_vendidas`

## Proceso ETL

La carga de información mensual se realiza mediante el siguiente proceso:

1. Cargar el archivo CSV correspondiente al mes en `stg_ventas_mensuales`.
2. Validar la cantidad y estructura de registros.
3. Ejecutar el procedimiento almacenado `cargar_ventas_mensuales()`.
4. Validar que las marcas existentes en el archivo estén registradas en `dim_marca`.
5. Crear automáticamente nuevos modelos en `dim_modelo` cuando corresponda.
6. Asociar cada registro con su período, marca y modelo.
7. Cargar la información en `fact_ventas_mensuales`.

Ejemplo:

```sql
CALL cargar_ventas_mensuales(202605);