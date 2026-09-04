import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import cargar_datos

st.set_page_config(page_title="Comparativa de Marcas", page_icon="⚖️", layout="wide")

st.title("Comparativa de Marcas")

df = cargar_datos()

# --- Sidebar: selector de marcas ---
marcas_disponibles = sorted(df["marca"].unique())

seleccionadas = st.sidebar.multiselect(
    "Seleccioná marcas a comparar (máx. 5)",
    marcas_disponibles,
    default=marcas_disponibles[:2] if len(marcas_disponibles) >= 2 else marcas_disponibles,
    max_selections=5,
)

if len(seleccionadas) < 2:
    st.info("Seleccioná al menos 2 marcas en el panel lateral para comparar.")
    st.stop()

# --- Agrupar por marca ---
df_comp = df[df["marca"].isin(seleccionadas)]

marcas_agg = (
    df_comp.groupby("marca", as_index=False)
    .agg(
        unidades_totales=("unidades_vendidas", "sum"),
        modelos_activos=("modelo", "nunique"),
        meses_activos=("id_periodo", "nunique"),
        mejor_mes=("unidades_vendidas", "max"),
    )
)
marcas_agg["promedio_mensual"] = (marcas_agg["unidades_totales"] / marcas_agg["meses_activos"]).round(0).astype(int)
marcas_agg["participacion"] = (marcas_agg["unidades_totales"] / df["unidades_vendidas"].sum() * 100).round(2)
marcas_agg = marcas_agg.sort_values("unidades_totales", ascending=False)

# --- Tabla resumen ---
st.subheader("Resumen comparativo")

st.dataframe(
    marcas_agg.rename(columns={
        "marca": "Marca",
        "unidades_totales": "Unidades totales",
        "modelos_activos": "Modelos activos",
        "meses_activos": "Meses activos",
        "mejor_mes": "Mejor mes (und.)",
        "promedio_mensual": "Promedio mensual",
        "participacion": "Participación (%)",
    }).set_index("Marca"),
    width="stretch",
)

st.divider()

# --- Evolución mensual comparativa ---
st.subheader("Evolución mensual")

evol = (
    df_comp.groupby(["id_periodo", "año_mes", "marca"], as_index=False)["unidades_vendidas"]
    .sum()
    .sort_values("id_periodo")
)

fig_lineas = px.line(
    evol,
    x="año_mes",
    y="unidades_vendidas",
    color="marca",
    markers=True,
    labels={"año_mes": "Mes", "unidades_vendidas": "Unidades", "marca": "Marca"},
)
fig_lineas.update_layout(yaxis_title="Unidades vendidas", xaxis_title="")
st.plotly_chart(fig_lineas, width="stretch")

st.divider()

# --- Barras agrupadas por período ---
st.subheader("Unidades por período")

fig_barras = px.bar(
    evol,
    x="año_mes",
    y="unidades_vendidas",
    color="marca",
    barmode="group",
    text="unidades_vendidas",
    labels={"año_mes": "Mes", "unidades_vendidas": "Unidades", "marca": "Marca"},
)
fig_barras.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
fig_barras.update_layout(yaxis_title="Unidades", xaxis_title="")
st.plotly_chart(fig_barras, width="stretch")

st.divider()

# --- Total acumulado ---
st.subheader("Total acumulado")

total_comp = (
    df_comp.groupby("marca", as_index=False)["unidades_vendidas"]
    .sum()
    .sort_values("unidades_vendidas", ascending=True)
)

fig_total = px.bar(
    total_comp,
    x="unidades_vendidas",
    y="marca",
    orientation="h",
    text="unidades_vendidas",
    labels={"unidades_vendidas": "Unidades", "marca": ""},
    color="marca",
)
fig_total.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
fig_total.update_layout(showlegend=False)
st.plotly_chart(fig_total, width="stretch")
