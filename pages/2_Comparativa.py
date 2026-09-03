import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import cargar_datos

st.set_page_config(page_title="Comparativa de Modelos", page_icon="🔄", layout="wide")

st.title("Comparativa de Modelos")

df = cargar_datos()

# --- Sidebar: selectores ---
marcas_modelo = sorted(df["marca_modelo"].unique())

seleccionados = st.sidebar.multiselect(
    "Seleccioná modelos a comparar (máx. 5)",
    marcas_modelo,
    default=marcas_modelo[:2],
    max_selections=5,
)

if len(seleccionados) < 2:
    st.info("Seleccioná al menos 2 modelos en el panel lateral para comparar.")
    st.stop()

df_comp = df[df["marca_modelo"].isin(seleccionados)]

# --- KPIs comparativos ---
st.subheader("Resumen comparativo")

resumen = (
    df_comp.groupby("marca_modelo", as_index=False)
    .agg(
        unidades_totales=("unidades_vendidas", "sum"),
        meses_activos=("id_periodo", "nunique"),
        mejor_mes=("unidades_vendidas", "max"),
    )
)
resumen["promedio_mensual"] = (resumen["unidades_totales"] / resumen["meses_activos"]).round(0).astype(int)
resumen["participacion"] = (resumen["unidades_totales"] / df["unidades_vendidas"].sum() * 100).round(2)
resumen = resumen.sort_values("unidades_totales", ascending=False)

st.dataframe(
    resumen.rename(columns={
        "marca_modelo": "Modelo",
        "unidades_totales": "Unidades totales",
        "meses_activos": "Meses activos",
        "mejor_mes": "Mejor mes",
        "promedio_mensual": "Promedio mensual",
        "participacion": "Participación (%)",
    }).set_index("Modelo"),
    width="stretch",
)

st.divider()

# --- Evolución mensual comparativa ---
st.subheader("Evolución mensual")

evol = (
    df_comp.groupby(["id_periodo", "año_mes", "marca_modelo"], as_index=False)["unidades_vendidas"]
    .sum()
    .sort_values("id_periodo")
)

fig_lineas = px.line(
    evol,
    x="año_mes",
    y="unidades_vendidas",
    color="marca_modelo",
    markers=True,
    labels={"año_mes": "Mes", "unidades_vendidas": "Unidades", "marca_modelo": "Modelo"},
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
    color="marca_modelo",
    barmode="group",
    text="unidades_vendidas",
    labels={"año_mes": "Mes", "unidades_vendidas": "Unidades", "marca_modelo": "Modelo"},
)
fig_barras.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
fig_barras.update_layout(yaxis_title="Unidades", xaxis_title="")
st.plotly_chart(fig_barras, width="stretch")

st.divider()

# --- Acumulado total comparado ---
st.subheader("Total acumulado")

total_comp = (
    df_comp.groupby("marca_modelo", as_index=False)["unidades_vendidas"]
    .sum()
    .sort_values("unidades_vendidas", ascending=True)
)

fig_total = px.bar(
    total_comp,
    x="unidades_vendidas",
    y="marca_modelo",
    orientation="h",
    text="unidades_vendidas",
    labels={"unidades_vendidas": "Unidades", "marca_modelo": ""},
    color="marca_modelo",
)
fig_total.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
fig_total.update_layout(showlegend=False)
st.plotly_chart(fig_total, width="stretch")
