import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import cargar_datos

st.set_page_config(page_title="Análisis por Marca", page_icon="🏷️", layout="wide")

st.title("Análisis por Marca")

df = cargar_datos()

# --- Sidebar: selector de marca ---
marcas_ordenadas = sorted(df["marca"].unique())
marca_sel = st.sidebar.selectbox("Seleccioná una marca", marcas_ordenadas)

df_marca = df[df["marca"] == marca_sel]

# --- KPIs de la marca ---
total_marca = df_marca["unidades_vendidas"].sum()
total_mercado = df["unidades_vendidas"].sum()
participacion = total_marca / total_mercado * 100
modelos_marca = df_marca["modelo"].nunique()
periodos_marca = df_marca["id_periodo"].nunique()
promedio_mensual = total_marca / periodos_marca if periodos_marca > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Unidades totales", f"{total_marca:,.0f}")
col2.metric("Participación", f"{participacion:.1f}%")
col3.metric("Modelos", modelos_marca)
col4.metric("Promedio mensual", f"{promedio_mensual:,.0f}")

st.divider()

# --- Evolución mensual de la marca vs mercado ---
st.subheader(f"Evolución mensual — {marca_sel} vs. mercado")

evol_marca = (
    df_marca.groupby(["id_periodo", "año_mes"], as_index=False)["unidades_vendidas"]
    .sum()
    .rename(columns={"unidades_vendidas": "marca"})
)

evol_mercado = (
    df.groupby(["id_periodo", "año_mes"], as_index=False)["unidades_vendidas"]
    .sum()
    .rename(columns={"unidades_vendidas": "mercado"})
)

evol = evol_marca.merge(evol_mercado, on=["id_periodo", "año_mes"])
evol = evol.sort_values("id_periodo")

fig_evol = px.line(
    evol.melt(
        id_vars=["id_periodo", "año_mes"],
        value_vars=["marca", "mercado"],
        var_name="serie",
        value_name="unidades",
    ),
    x="año_mes",
    y="unidades",
    color="serie",
    markers=True,
    labels={"año_mes": "Mes", "unidades": "Unidades", "serie": ""},
    color_discrete_map={"marca": "#1f77b4", "mercado": "#d3d3d3"},
)
fig_evol.update_layout(yaxis_title="Unidades vendidas", xaxis_title="")
st.plotly_chart(fig_evol, width="stretch")

st.divider()

# --- Ranking de modelos de la marca ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader(f"Modelos de {marca_sel} — Total acumulado")

    modelos_total = (
        df_marca.groupby("modelo", as_index=False)["unidades_vendidas"]
        .sum()
        .sort_values("unidades_vendidas", ascending=True)
    )

    fig_mod = px.bar(
        modelos_total,
        x="unidades_vendidas",
        y="modelo",
        orientation="h",
        text="unidades_vendidas",
        labels={"unidades_vendidas": "Unidades", "modelo": ""},
        color="unidades_vendidas",
        color_continuous_scale="Blues",
    )
    fig_mod.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_mod.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_mod, width="stretch")

with col_right:
    st.subheader(f"Evolución mensual por modelo — {marca_sel}")

    evol_modelos = (
        df_marca.groupby(["id_periodo", "año_mes", "modelo"], as_index=False)["unidades_vendidas"]
        .sum()
        .sort_values("id_periodo")
    )

    fig_evol_mod = px.line(
        evol_modelos,
        x="año_mes",
        y="unidades_vendidas",
        color="modelo",
        markers=True,
        labels={"año_mes": "Mes", "unidades_vendidas": "Unidades", "modelo": "Modelo"},
    )
    fig_evol_mod.update_layout(yaxis_title="Unidades", xaxis_title="")
    st.plotly_chart(fig_evol_mod, width="stretch")

st.divider()

# --- Tabla detallada ---
st.subheader(f"Detalle mensual — {marca_sel}")

tabla = (
    df_marca.pivot_table(
        index="modelo",
        columns="año_mes",
        values="unidades_vendidas",
        aggfunc="sum",
        fill_value=0,
    )
    .assign(Total=lambda x: x.sum(axis=1))
    .sort_values("Total", ascending=False)
)

st.dataframe(tabla, width="stretch")
