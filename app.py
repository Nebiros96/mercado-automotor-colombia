import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import cargar_datos

st.set_page_config(
    page_title="Mercado Automotor Colombia",
    page_icon="🚗",
    layout="wide",
)

st.title("Mercado Automotor de Colombia")
st.caption("Ventas mensuales de vehículos — 2026")

df = cargar_datos()

# --- KPIs ---
periodos = df["id_periodo"].nunique()
marcas = df["marca"].nunique()
modelos = df["modelo"].nunique()
total_unidades = df["unidades_vendidas"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Unidades vendidas", f"{total_unidades:,.0f}")
col2.metric("Marcas", marcas)
col3.metric("Modelos", modelos)
col4.metric("Períodos cargados", periodos)

st.divider()

# --- Evolución mensual del mercado ---
st.subheader("Evolución mensual del mercado")

evolucion = (
    df.groupby(["id_periodo", "año_mes"], as_index=False)["unidades_vendidas"]
    .sum()
    .sort_values("id_periodo")
)

fig_evol = px.line(
    evolucion,
    x="año_mes",
    y="unidades_vendidas",
    markers=True,
    labels={"año_mes": "Mes", "unidades_vendidas": "Unidades"},
    text="unidades_vendidas",
)
fig_evol.update_traces(textposition="top center", texttemplate="%{text:,.0f}")
fig_evol.update_layout(yaxis_title="Unidades vendidas", xaxis_title="")
st.plotly_chart(fig_evol, width="stretch")

st.divider()

# --- Top 10 marcas ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 marcas por unidades totales")

    top_marcas = (
        df.groupby("marca", as_index=False)["unidades_vendidas"]
        .sum()
        .nlargest(10, "unidades_vendidas")
        .sort_values("unidades_vendidas", ascending=True)
    )

    fig_marcas = px.bar(
        top_marcas,
        x="unidades_vendidas",
        y="marca",
        orientation="h",
        text="unidades_vendidas",
        labels={"unidades_vendidas": "Unidades", "marca": ""},
        color="unidades_vendidas",
        color_continuous_scale="Blues",
    )
    fig_marcas.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_marcas.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_marcas, width="stretch")

with col_right:
    st.subheader("Top 10 modelos por unidades totales")

    top_modelos = (
        df.groupby("marca_modelo", as_index=False)["unidades_vendidas"]
        .sum()
        .nlargest(10, "unidades_vendidas")
        .sort_values("unidades_vendidas", ascending=True)
    )

    fig_modelos = px.bar(
        top_modelos,
        x="unidades_vendidas",
        y="marca_modelo",
        orientation="h",
        text="unidades_vendidas",
        labels={"unidades_vendidas": "Unidades", "marca_modelo": ""},
        color="unidades_vendidas",
        color_continuous_scale="Greens",
    )
    fig_modelos.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_modelos.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_modelos, width="stretch")

st.divider()

# --- Participación de mercado por marca ---
st.subheader("Participación de mercado por marca")

participacion = (
    df.groupby("marca", as_index=False)["unidades_vendidas"]
    .sum()
    .sort_values("unidades_vendidas", ascending=False)
)
participacion["participacion"] = (
    participacion["unidades_vendidas"] / participacion["unidades_vendidas"].sum() * 100
)

top_n = 10
otras = participacion.iloc[top_n:]
top_part = participacion.iloc[:top_n].copy()
if len(otras) > 0:
    otras_row = pd.DataFrame({
        "marca": ["Otras"],
        "unidades_vendidas": [otras["unidades_vendidas"].sum()],
        "participacion": [otras["participacion"].sum()],
    })
    top_part = pd.concat([top_part, otras_row], ignore_index=True)

fig_pie = px.pie(
    top_part,
    values="unidades_vendidas",
    names="marca",
    hole=0.4,
)
fig_pie.update_traces(textinfo="label+percent", textposition="outside")
fig_pie.update_layout(showlegend=False)
st.plotly_chart(fig_pie, width="stretch")
