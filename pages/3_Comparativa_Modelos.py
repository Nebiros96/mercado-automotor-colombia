import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import cargar_datos

st.set_page_config(page_title="Comparativa de Modelos", page_icon="🔄", layout="wide")

st.title("Comparativa de Modelos")

df = cargar_datos()

# --- Sidebar: selectores de 2 modelos ---
marcas_modelo = sorted(df["marca_modelo"].unique())

modelo_a = st.sidebar.selectbox("Modelo A", marcas_modelo, index=0)
modelo_b = st.sidebar.selectbox("Modelo B", marcas_modelo, index=min(1, len(marcas_modelo) - 1))

if modelo_a == modelo_b:
    st.warning("Seleccioná dos modelos diferentes para comparar.")
    st.stop()

seleccionados = [modelo_a, modelo_b]
df_comp = df[df["marca_modelo"].isin(seleccionados)]

# --- Header con logos de marcas ---
info_a = df_comp[df_comp["marca_modelo"] == modelo_a].iloc[0]
info_b = df_comp[df_comp["marca_modelo"] == modelo_b].iloc[0]

col_a, col_sep, col_b = st.columns([5, 1, 5])

with col_a:
    sub_logo_a, sub_name_a = st.columns([1, 4])
    with sub_logo_a:
        if pd.notna(info_a["url_logo"]):
            st.image(info_a["url_logo"], width=60)
    with sub_name_a:
        st.subheader(modelo_a)

with col_sep:
    st.markdown("<h2 style='text-align: center; color: gray;'>vs</h2>", unsafe_allow_html=True)

with col_b:
    sub_logo_b, sub_name_b = st.columns([1, 4])
    with sub_logo_b:
        if pd.notna(info_b["url_logo"]):
            st.image(info_b["url_logo"], width=60)
    with sub_name_b:
        st.subheader(modelo_b)

st.divider()

# --- Tabla resumen comparativa ---
st.subheader("Resumen comparativo")

resumen = (
    df_comp.groupby("marca_modelo", as_index=False)
    .agg(
        unidades_totales=("unidades_vendidas", "sum"),
        meses_activos=("id_periodo", "nunique"),
        mejor_mes=("unidades_vendidas", "max"),
        peor_mes=("unidades_vendidas", "min"),
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
        "peor_mes": "Peor mes",
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
    text="unidades_vendidas",
    labels={"año_mes": "Mes", "unidades_vendidas": "Unidades", "marca_modelo": "Modelo"},
)
fig_lineas.update_traces(textposition="top center", texttemplate="%{text:,.0f}")
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
