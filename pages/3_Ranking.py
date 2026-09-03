import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import cargar_datos

st.set_page_config(page_title="Ranking", page_icon="🏆", layout="wide")

st.title("Ranking de Ventas")

df = cargar_datos()

# --- Sidebar: filtros ---
st.sidebar.header("Filtros")

periodos_disponibles = sorted(df["año_mes"].unique())
rango = st.sidebar.select_slider(
    "Rango de períodos",
    options=periodos_disponibles,
    value=(periodos_disponibles[0], periodos_disponibles[-1]),
)

marcas_disponibles = ["Todas"] + sorted(df["marca"].unique())
marca_filtro = st.sidebar.selectbox("Marca", marcas_disponibles)

top_n = st.sidebar.slider("Cantidad de posiciones", min_value=5, max_value=50, value=20, step=5)

nivel = st.sidebar.radio("Agrupar por", ["Marca-Modelo", "Marca", "Modelo"])

# --- Aplicar filtros ---
mask = (df["año_mes"] >= rango[0]) & (df["año_mes"] <= rango[1])
if marca_filtro != "Todas":
    mask &= df["marca"] == marca_filtro

df_filtrado = df[mask]

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# --- Calcular ranking ---
if nivel == "Marca-Modelo":
    col_group = "marca_modelo"
elif nivel == "Marca":
    col_group = "marca"
else:
    col_group = "modelo"

ranking = (
    df_filtrado.groupby(col_group, as_index=False)
    .agg(
        unidades_totales=("unidades_vendidas", "sum"),
        meses_activos=("id_periodo", "nunique"),
        mejor_mes=("unidades_vendidas", "max"),
    )
)
ranking["promedio_mensual"] = (ranking["unidades_totales"] / ranking["meses_activos"]).round(0).astype(int)
ranking = ranking.nlargest(top_n, "unidades_totales").reset_index(drop=True)
ranking.index = ranking.index + 1
ranking.index.name = "Posición"

# --- KPIs del filtro ---
total_filtrado = df_filtrado["unidades_vendidas"].sum()
periodos_filtrados = df_filtrado["id_periodo"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Unidades en el rango", f"{total_filtrado:,.0f}")
col2.metric("Períodos seleccionados", periodos_filtrados)
col3.metric(f"Top {nivel}s mostrados", len(ranking))

st.divider()

# --- Gráfico de barras horizontal ---
st.subheader(f"Top {len(ranking)} — {nivel}")

ranking_chart = ranking.sort_values("unidades_totales", ascending=True)

fig = px.bar(
    ranking_chart,
    x="unidades_totales",
    y=col_group,
    orientation="h",
    text="unidades_totales",
    labels={"unidades_totales": "Unidades", col_group: ""},
    color="unidades_totales",
    color_continuous_scale="Viridis",
)
fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
fig.update_layout(
    showlegend=False,
    coloraxis_showscale=False,
    height=max(400, len(ranking) * 28),
)
st.plotly_chart(fig, width="stretch")

st.divider()

# --- Tabla del ranking ---
st.subheader("Tabla de ranking")

st.dataframe(
    ranking.rename(columns={
        col_group: nivel,
        "unidades_totales": "Unidades totales",
        "meses_activos": "Meses activos",
        "mejor_mes": "Mejor mes (und.)",
        "promedio_mensual": "Promedio mensual",
    }),
    width="stretch",
)
