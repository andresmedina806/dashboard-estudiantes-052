import streamlit as st
import pandas as pd

# Título del dashboard
st.title("Dashboard Estudiantil – Grupo 052")

# Cargar archivo procesado
df = pd.read_excel(r"C:\Users\catac\Downloads\DashboardPA\DashboardPA\Estudiantes_ProcesadoLimpio.xlsx")

# Mostrar archivo
st.subheader("Archivo de Estudiantes")
st.dataframe(df)

# -------------------------------
# PUNTO 4: Filtros Multiselect
# -------------------------------

st.subheader("Filtros")

filtro_rh = st.multiselect("Tipo de Sangre (RH)", df["RH"].dropna().unique())
filtro_cabello = st.multiselect("Color de Cabello", df["Color_Cabello"].dropna().unique())
filtro_barrio = st.multiselect("Barrio de Residencia", df["Barrio_Residencia"].dropna().unique())

df_filtrado = df.copy()

if filtro_rh:
    df_filtrado = df_filtrado[df_filtrado["RH"].isin(filtro_rh)]

if filtro_cabello:
    df_filtrado = df_filtrado[df_filtrado["Color_Cabello"].isin(filtro_cabello)]

if filtro_barrio:
    df_filtrado = df_filtrado[df_filtrado["Barrio_Residencia"].isin(filtro_barrio)]

# -------------------------------
# PUNTO 5: Sliders
# -------------------------------

st.subheader("Rangos")

edad_min, edad_max = st.slider(
    "Rango de Edad",
    int(df["Edad"].min()),
    int(df["Edad"].max()),
    (int(df["Edad"].min()), int(df["Edad"].max()))
)

est_min, est_max = st.slider(
    "Rango de Estatura (m)",
    float(df["Estatura"].min()),
    float(df["Estatura"].max()),
    (float(df["Estatura"].min()), float(df["Estatura"].max()))
)

df_filtrado = df_filtrado[
    (df_filtrado["Edad"] >= edad_min) &
    (df_filtrado["Edad"] <= edad_max) &
    (df_filtrado["Estatura"] >= est_min) &
    (df_filtrado["Estatura"] <= est_max)
]

# Mostrar resultado filtrado
st.subheader("Datos Filtrados")
st.dataframe(df_filtrado)

# -------------------------------
# PUNTO 7: Métricas
# -------------------------------

st.subheader("Métricas del Grupo Filtrado")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Estudiantes", len(df_filtrado))

col2.metric("Edad Promedio", round(df_filtrado["Edad"].mean(), 1))

col3.metric("Estatura Promedio (m)", round(df_filtrado["Estatura"].mean(), 2))

col4.metric("Peso Promedio (kg)", round(df_filtrado["Peso"].mean(), 1))

col5.metric("IMC Promedio", round(df_filtrado["IMC"].mean(), 1))


# -------------------------------
# PUNTO 8: Primera fila de gráficos
# -------------------------------

st.subheader("Distribuciones del Grupo Filtrado")

col1, col2, col3 = st.columns(3)

# --- Gráfico 1: RH ---
with col1:
    st.write("Distribución por Tipo de Sangre (RH)")
    rh_counts = df_filtrado["RH"].value_counts()
    st.bar_chart(rh_counts)

# --- Gráfico 2: Color de Cabello ---
with col2:
    st.write("Distribución por Color de Cabello")
    cabello_counts = df_filtrado["Color_Cabello"].value_counts()
    st.bar_chart(cabello_counts)

# --- Gráfico 3: Barrio de Residencia ---
with col3:
    st.write("Distribución por Barrio")
    barrio_counts = df_filtrado["Barrio_Residencia"].value_counts()
    st.bar_chart(barrio_counts)



# -------------------------------
# PUNTO 9: 2da Fila de Gráficos (Scatter y Barras Cabello)
# -------------------------------

import plotly.express as px
import plotly.graph_objects as go

st.subheader("2. Relación Física y Color de Cabello")
col_g3, col_g4 = st.columns(2)

# --- Gráfico 3: Scatter Estatura vs Peso (Profesional) ---
with col_g3:
    st.write("*Relación Estatura vs Peso*")
    if not df_filtrado.empty:
        fig_scatter = px.scatter(
            df_filtrado,
            x="Peso",
            y="Estatura",
            color="Color_Cabello",
            size="IMC",
            hover_data=["Nombre_Estudiante", "Apellido_Estudiante", "Edad", "IMC"],
            labels={
                "Peso": "Peso (kg)",
                "Estatura": "Estatura (m)",
                "Color_Cabello": "Color de Cabello",
                "IMC": "IMC",
            },
            trendline="ols",               # Línea de tendencia estadística
            trendline_scope="overall",
        )
        fig_scatter.update_traces(
            marker=dict(
                opacity=0.82,
                line=dict(width=0.8, color="white"),
            ),
            selector=dict(mode="markers"),
        )
        fig_scatter.update_layout(
            plot_bgcolor="rgba(245,247,250,1)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(200,200,200,0.4)",
                zeroline=False,
                title_font=dict(size=12, color="#444"),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(200,200,200,0.4)",
                zeroline=False,
                title_font=dict(size=12, color="#444"),
            ),
            legend=dict(
                title_text="Cabello",
                orientation="v",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(200,200,200,0.5)",
                borderwidth=1,
            ),
            margin=dict(t=30, b=40, l=10, r=10),
            height=380,
        )
        # Personalizar línea de tendencia
        fig_scatter.update_traces(
            line=dict(color="#E63946", width=2, dash="dash"),
            selector=dict(mode="lines"),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("Sin datos para mostrar.")

# --- Gráfico 4: Barras Color de Cabello con color real de cada barra ---
with col_g4:
    st.write("*Distribución por Color de Cabello*")
    if not df_filtrado.empty:

        # Mapa de colores reales por nombre de cabello
        COLOR_CABELLO_MAP = {
            # Español
            "Negro":    "#1a1a1a",
            "Castaño":  "#6B3A2A",
            "Café":     "#7B4F2E",
            "Rubio":    "#E8C96D",
            "Rojo":     "#C0392B",
            "Rojizo":   "#C0392B",
            "Naranja":  "#E67E22",
            "Canoso":   "#9E9E9E",
            "Gris":     "#9E9E9E",
            "Blanco":   "#E0E0E0",
            "Azul":     "#2980B9",
            "Verde":    "#27AE60",
            "Rosa":     "#E91E8C",
            "Morado":   "#8E44AD",
            "Violeta":  "#8E44AD",
            # English fallbacks
            "Black":    "#1a1a1a",
            "Brown":    "#6B3A2A",
            "Blonde":   "#E8C96D",
            "Red":      "#C0392B",
            "Gray":     "#9E9E9E",
            "White":    "#E0E0E0",
        }

        cabello_counts = (
            df_filtrado["Color_Cabello"]
            .value_counts()
            .reset_index()
        )
        cabello_counts.columns = ["Color_Cabello", "Cantidad"]

        # Asignar color real a cada fila; fallback gris oscuro si no está en el mapa
        cabello_counts["color_hex"] = cabello_counts["Color_Cabello"].map(
            lambda c: COLOR_CABELLO_MAP.get(c, "#555555")
        )

        fig_cabello = go.Figure()

        for _, row in cabello_counts.iterrows():
            # Borde blanco para cabellos muy claros (rubio, blanco)
            border_color = "#999" if row["color_hex"] in ["#E8C96D", "#E0E0E0"] else "white"

            fig_cabello.add_trace(
                go.Bar(
                    x=[row["Color_Cabello"]],
                    y=[row["Cantidad"]],
                    name=row["Color_Cabello"],
                    marker=dict(
                        color=row["color_hex"],
                        line=dict(color=border_color, width=1.5),
                    ),
                    text=[row["Cantidad"]],
                    textposition="outside",
                    hovertemplate=(
                        f"<b>{row['Color_Cabello']}</b><br>"
                        f"Estudiantes: {row['Cantidad']}<extra></extra>"
                    ),
                )
            )

        fig_cabello.update_layout(
            showlegend=False,
            barmode="group",
            plot_bgcolor="rgba(245,247,250,1)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Color de Cabello",
                showgrid=False,
                tickfont=dict(size=12, color="#333"),
                title_font=dict(size=12, color="#444"),
            ),
            yaxis=dict(
                title="Nº Estudiantes",
                showgrid=True,
                gridcolor="rgba(200,200,200,0.4)",
                zeroline=False,
                title_font=dict(size=12, color="#444"),
            ),
            margin=dict(t=40, b=40, l=10, r=10),
            height=380,
            uniformtext_minsize=10,
            uniformtext_mode="hide",
        )

        st.plotly_chart(fig_cabello, use_container_width=True)
    else:
        st.warning("Sin datos para mostrar.")

















# -------------------------------
# PUNTO 9: 2da Fila de Gráficos (Scatter y Barras Cabello)
# -------------------------------
st.subheader("2. Relación Física y Color de Cabello")
col_g3, col_g4 = st.columns(2)

with col_g3:
    st.write("Relación Estatura vs Peso (Scatter)")
    st.scatter_chart(df_filtrado, x="Peso", y="Estatura")

with col_g4:
    st.write("Distribución por Color de Cabello (Barras)")
    cabello_counts = df_filtrado["Color_Cabello"].value_counts()
    st.bar_chart(cabello_counts)
    
# -------------------------------
# PUNTO 10: 3era Fila de Gráficos (Lineas Talla Zapatos y Barras Barrios)
# -------------------------------
st.subheader("3. Tallas de Zapatos y Barrios de Residencia")
col_g5, col_g6 = st.columns(2)

with col_g5:
    st.write("Distribución Tallas de Zapatos (Línea)")
    if "Talla_Zapato" in df_filtrado.columns:
        zapatos_counts = df_filtrado["Talla_Zapato"].value_counts().sort_index()
        st.line_chart(zapatos_counts)
    else:
        st.warning("No se encontró la columna de Talla_Zapato.")

with col_g6:
    st.write("Top 10 Barrios de Residencia (Barras)")
    top_barrios = df_filtrado["Barrio_Residencia"].value_counts().head(10)
    st.bar_chart(top_barrios)
    
    
# -------------------------------
# PUNTO 11: 2 archivos con el Top 5
# -------------------------------
st.subheader("Top 5: Mayores Medidas Físicas")
col_t1, col_t2 = st.columns(2)

with col_t1:
    st.write("**Top 5: Mayor Estatura**")
    # Usamos los nombres exactos de las columnas de tu Excel
    top_estatura = df_filtrado.nlargest(5, "Estatura")[["Nombre_Estudiante", "Apellido_Estudiante", "Estatura", "Peso", "Edad"]] 
    st.dataframe(top_estatura, hide_index=True)

with col_t2:
    st.write("**Top 5: Mayor Peso**")
    # Usamos los nombres exactos de las columnas de tu Excel
    top_peso = df_filtrado.nlargest(5, "Peso")[["Nombre_Estudiante", "Apellido_Estudiante", "Estatura", "Peso", "Edad"]]
    st.dataframe(top_peso, hide_index=True)

# -------------------------------
# PUNTO 12: Resumen Estadístico en 3 columnas
# -------------------------------
st.subheader("Resumen Estadístico Físico")
col_s1, col_s2, col_s3 = st.columns(3)

# La función .describe() nos entrega el conteo, media, desviación estándar, min, max, etc. [cite: 17]
with col_s1:
    st.write("**Estadísticas de Estatura**")
    st.dataframe(df_filtrado["Estatura"].describe())

with col_s2:
    st.write("**Estadísticas de Peso**")
    st.dataframe(df_filtrado["Peso"].describe())

with col_s3:
    st.write("**Estadísticas de IMC**")
    st.dataframe(df_filtrado["IMC"].describe())