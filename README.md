# Mercado Automotor de Colombia

Proyecto de integración y análisis de información mensual del mercado automotor colombiano. El proyecto utiliza PostgreSQL para estructurar los datos mediante un modelo dimensional y un proceso ETL desarrollado en SQL/PLpgSQL.

El objetivo es consolidar las ventas mensuales por marca y modelo para posteriormente realizar análisis y visualizaciones mediante herramientas de Business Intelligence como Power BI.

## Arquitectura del proyecto

El flujo de datos está diseñado de la siguiente manera:

```text
Archivo CSV mensual
        │
        ▼
stg_ventas_mensuales
        │
        ▼
Validaciones ETL
        │
        ├──────────────► dim_marca
        │
        ├──────────────► dim_modelo
        │
        └──────────────► dim_fecha
                         │
                         ▼
                fact_ventas_mensuales
                         │
                         ▼
                    Power BI
```

La tabla de staging funciona como punto de entrada de los archivos mensuales, mientras que las dimensiones y la tabla de hechos conforman el modelo analítico.

## Modelo de datos

El proyecto utiliza un modelo dimensional con tres dimensiones y una tabla de hechos.

### `dim_fecha`

Dimensión temporal con granularidad mensual.

Contiene:

* Período en formato `YYYYMM`
* Fecha
* Año
* Número de mes
* Nombre del mes
* Trimestre
* Semestre
* Año-mes

### `dim_marca`

Catálogo de marcas de vehículos.

Cada marca posee un identificador único utilizado como clave sustituta dentro del modelo.

### `dim_modelo`

Catálogo de modelos asociados a cada marca.

La combinación de marca y modelo es única, permitiendo identificar correctamente cada vehículo dentro del modelo dimensional.

### `fact_ventas_mensuales`

Tabla de hechos que almacena las unidades vendidas por modelo y período.

La granularidad es:

> Una fila por modelo y período mensual.

Principales campos:

| Campo               | Descripción                          |
| ------------------- | ------------------------------------ |
| `id_periodo`        | Período de venta en formato `YYYYMM` |
| `id_modelo`         | Identificador del modelo             |
| `unidades_vendidas` | Unidades vendidas durante el período |

La tabla utiliza una clave primaria compuesta por `id_periodo` e `id_modelo`.

## Proceso ETL

La carga de nuevos períodos sigue un proceso controlado:

1. Preparación del archivo CSV correspondiente al mes.
2. Limpieza y normalización de los datos de origen.
3. Vaciamiento de la tabla de staging.
4. Importación del CSV en `stg_ventas_mensuales`.
5. Validación de marcas y modelos.
6. Incorporación de nuevos modelos cuando corresponda.
7. Eliminación de los registros existentes del período que se está cargando.
8. Inserción de los datos del período en `fact_ventas_mensuales`.
9. Validación final de la cantidad de registros cargados.

El procedimiento almacenado utilizado para realizar este proceso es:

```sql
CALL cargar_ventas_mensuales(202605);
```

El parámetro corresponde al período en formato `YYYYMM`.

Por ejemplo:

```sql
CALL cargar_ventas_mensuales(202606);
CALL cargar_ventas_mensuales(202607);
CALL cargar_ventas_mensuales(202608);
```

## Control de calidad de los datos

El proceso ETL incorpora diferentes validaciones para evitar que errores presentes en los archivos de origen lleguen al modelo analítico.

Entre ellas:

* Validación de existencia del período en `dim_fecha`.
* Validación de marcas no registradas.
* Validación de asociación entre marca y modelo.
* Control de unidades vendidas no negativas.
* Integridad referencial mediante claves foráneas.
* Control de duplicidad mediante claves primarias y restricciones `UNIQUE`.

Las marcas nuevas no se crean automáticamente durante el proceso ETL. Si aparece una marca que no existe en `dim_marca`, la carga se detiene y muestra los vehículos afectados para que puedan ser revisados.

Los modelos nuevos asociados a marcas válidas sí pueden incorporarse automáticamente a `dim_modelo`.

Este enfoque permite diferenciar entre la aparición legítima de una nueva marca y errores de digitación en los archivos de origen.

## Recarga de períodos

El procedimiento considera el archivo CSV como fuente de verdad para el período cargado.

Al ejecutar nuevamente un período:

```sql
CALL cargar_ventas_mensuales(202605);
```

los registros existentes de mayo de 2026 son eliminados y posteriormente reemplazados por la información actualmente disponible en staging.

Esto permite corregir un archivo y volver a cargar el período sin generar duplicados.

## Estructura del repositorio

```text
mercado-automotor-colombia/
│
├── README.md
│
├── data/
│   └── fact_ventas_mensuales.csv
│
└── sql/
    ├── 01_create_db.sql
    ├── 02_create_dimensions.sql
    ├── 03_create_fact.sql
    ├── 04_create_fact_staging.sql
    ├── 05_etl_ventas_mensuales.sql
    └── 99_query_validacion.sql
```

### Archivos SQL

**`01_create_db.sql`**

Creación de la base de datos del proyecto:

```text
mercado_automotor_colombia
```

**`02_create_dimensions.sql`**

Creación y configuración de las dimensiones:

* `dim_fecha`
* `dim_marca`
* `dim_modelo`

**`03_create_fact.sql`**

Creación de la tabla de hechos `fact_ventas_mensuales`, incluyendo claves primarias, claves foráneas y restricciones.

**`04_create_fact_staging.sql`**

Creación de la tabla de staging utilizada para recibir los archivos CSV mensuales.

**`05_etl_ventas_mensuales.sql`**

Contiene el procedimiento almacenado `cargar_ventas_mensuales()`, responsable de validar y cargar la información desde staging hacia el modelo dimensional.

**`99_query_validacion.sql`**

Consultas utilizadas para verificar la información cargada y validar las relaciones entre hechos, modelos y marcas.

## Datos

El directorio `data/` contiene los datos utilizados para alimentar la tabla de hechos.

Actualmente se incluye:

```text
data/fact_ventas_mensuales.csv
```

El archivo contiene información consolidada de ventas mensuales por vehículo.

## Tecnologías

* PostgreSQL
* PL/pgSQL
* pgAdmin 4
* SQL
* Git
* GitHub
* Power BI

## Posibles análisis

La estructura permite desarrollar posteriormente diferentes análisis del mercado automotor, entre ellos:

* Evolución mensual de ventas.
* Ranking de marcas.
* Ranking de modelos.
* Participación de mercado.
* Crecimiento mensual e interanual.
* Evolución de modelos nuevos.
* Análisis por segmento o fabricante.
* Evolución de vehículos eléctricos e híbridos.
* Construcción de dashboards interactivos en Power BI.

## Estado del proyecto

**En desarrollo.**

La estructura de la base de datos, las dimensiones, la tabla de hechos y el proceso ETL mensual se encuentran implementados.

El proyecto continuará incorporando nuevos períodos y análisis sobre la evolución del mercado automotor colombiano.

## Fuente de información

Los datos corresponden a información de matriculaciones de vehículos en Colombia.

La documentación de las fuentes y metodología de cada conjunto de datos será ampliada a medida que avance el proyecto.
