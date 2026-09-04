import pandas as pd
import psycopg2
import streamlit as st

MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

QUERY = """
SELECT
    fm.id_periodo,
    df.año,
    df.mes_numero,
    df.mes_nombre,
    df.trimestre,
    df.semestre,
    df.año_mes,
    da.id_marca,
    da.marca,
    da.url_logo,
    dm.id_modelo,
    dm.modelo,
    fm.unidades_vendidas
FROM fact_ventas_mensuales fm
JOIN dim_fecha df ON df.id_periodo = fm.id_periodo
JOIN dim_modelo dm ON dm.id_modelo = fm.id_modelo
JOIN dim_marca da ON da.id_marca = dm.id_marca
ORDER BY fm.id_periodo, da.marca, dm.modelo;
"""


def _get_connection():
    s = st.secrets["connections"]["supabase"]
    return psycopg2.connect(
        host=s["host"],
        port=s["port"],
        dbname=s["database"],
        user=s["username"],
        password=s["password"],
        sslmode="require",
    )


@st.cache_data(ttl=300)
def cargar_datos() -> pd.DataFrame:
    """Consulta las tablas del modelo dimensional en Supabase y devuelve un DataFrame consolidado."""

    conn = _get_connection()
    df = pd.read_sql(QUERY, conn)
    conn.close()

    df["marca_modelo"] = df["marca"] + " " + df["modelo"]

    column_order = [
        "id_periodo", "año", "mes_numero", "mes_nombre", "año_mes",
        "trimestre", "semestre",
        "id_marca", "marca", "url_logo", "id_modelo", "modelo", "marca_modelo",
        "unidades_vendidas",
    ]

    return df[column_order]
