import streamlit as st
import pandas as pd

# Título del dashboard
st.title("Dashboard Estudiantil – Grupo 052")

# Cargar archivo procesado
df = pd.read_excel(r"./Estudiantes_ProcesadoLimpio.xlsx")

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
# Filtro Integrantes de nuestro grupo
# -------------------------------

nombres_limpios = df_filtrado["Nombre_Estudiante"].astype(str).str.strip()
apellidos_limpios = df_filtrado["Apellido_Estudiante"].astype(str).str.strip()
df_filtrado["Nombre_Completo"] = nombres_limpios + " " + apellidos_limpios

nombres_grupo = [
        "ANDRES ELIAS MEDINA GAVIRIA", 
        "ISABELA RESTREPO MARIN", 
        "THOMAS DAVID BUENAÑOS ANGEL", 
        "CATALINA CORREA CARDONA"
    ] 
    
filtro_integrantes = st.multiselect("Integrantes del grupo a exponer", nombres_grupo, key="filtro_grupo_final")

if filtro_integrantes:
        df_filtrado = df_filtrado[df_filtrado["Nombre_Completo"].isin(filtro_integrantes)]


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
# -------------------------------
import plotly.express as px
import plotly.graph_objects as go

st.subheader("Distribuciones del Grupo Filtrado")

# --- Diseño profesional con CSS para los marcos azulados ---
st.markdown("""
<style>
    div[data-testid="stVVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        border: 2px solid RoyalBlue;
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(240,248,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

# --- Gráfico 1: Distribución por Edad (Barras profesional) ---
with col1:
    with st.container(border=True):
        st.write("*Distribución por Edad*")
        if not df_filtrado.empty:
            edad_counts = df_filtrado["Edad"].value_counts().sort_index().reset_index()
            edad_counts.columns = ["Edad", "Cantidad"]

            fig_edad = px.bar(
                edad_counts,
                x="Edad",
                y="Cantidad",
                text="Cantidad",
                color="Cantidad",
                color_continuous_scale="Blues",
                labels={"Edad": "Edad (años)", "Cantidad": "Nº Estudiantes"},
            )
            fig_edad.update_traces(
                textposition="outside",
                textfont_size=16,
                textfont_color="black",
                cliponaxis=False,
                marker_line_color="rgb(8,48,107)",
                marker_line_width=1.5,
            )
            fig_edad.update_layout(
                bargap=0.1,
                coloraxis_showscale=False,
                font=dict(size=14),
                xaxis=dict(tickmode="linear", dtick=1, tickfont=dict(size=13, color="black")),
                yaxis=dict(tickfont=dict(size=13, color="black")),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)", 
                margin=dict(t=50, b=20, l=10, r=10),
                height=400,
            )
            st.plotly_chart(fig_edad, use_container_width=True)
        else:
            st.warning("Sin datos para mostrar.")

# --- Gráfico 2: Distribución por Tipo de Sangre (Torta/Pie profesional) ---
with col2:
    with st.container(border=True):
        st.write("*Distribución por Tipo de Sangre (RH)*")
        if not df_filtrado.empty:
            rh_counts = df_filtrado["RH"].value_counts().reset_index()
            rh_counts.columns = ["RH", "Cantidad"]

            fig_rh = go.Figure(
                go.Pie(
                    labels=rh_counts["RH"],
                    values=rh_counts["Cantidad"],
                    hole=0.38,
                    textinfo="label+percent",
                    textfont=dict(size=15),
                    hovertemplate="<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>",
                    marker=dict(
                        colors=px.colors.qualitative.Set2,
                        line=dict(color="white", width=2),
                    ),
                    pull=[0.05] * len(rh_counts),
                )
            )
            fig_rh.update_layout(
                showlegend=True,
                font=dict(size=14),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=13)),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=20, b=20, l=10, r=10),
                height=400,
            )
            st.plotly_chart(fig_rh, use_container_width=True)
        else:
            st.warning("Sin datos para mostrar.")


# -------------------------------
# PUNTO 9: 2da Fila de Gráficos (Scatter y Barras Cabello)
# -------------------------------

st.subheader("2. Relación Física y Color de Cabello")
col_g3, col_g4 = st.columns(2)

# --- Gráfico: Scatter Estatura vs Peso ---
with col_g3:
    st.write("*Relación Estatura vs Peso*")
    if not df_filtrado.empty:

        # ✅ FIX: eliminar filas con NaN en columnas críticas
        df_scatter = df_filtrado.dropna(subset=["Peso", "Estatura", "IMC", "Color_Cabello"]).copy()

        # Normalizar IMC para el tamaño de los puntos
        imc_min = df_scatter["IMC"].min()
        imc_max = df_scatter["IMC"].max()
        if imc_max > imc_min:
            df_scatter["IMC_size"] = 8 + ((df_scatter["IMC"] - imc_min) / (imc_max - imc_min)) * 22
        else:
            df_scatter["IMC_size"] = 15

        fig_scatter = px.scatter(
            df_scatter,
            x="Peso",
            y="Estatura",
            color="Color_Cabello",
            size="IMC_size",
            size_max=30,
            hover_data=["Nombre_Estudiante", "Apellido_Estudiante", "Edad", "IMC"],
            labels={
                "Peso": "Peso (kg)",
                "Estatura": "Estatura (m)",
                "Color_Cabello": "Color de Cabello",
                "IMC_size": "IMC (escalado)",
            },
            trendline="ols",
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
        fig_scatter.update_traces(
            line=dict(color="#E63946", width=2, dash="dash"),
            selector=dict(mode="lines"),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("Sin datos para mostrar.")

# --- Gráfico: Barras Color de Cabello con color real ---
with col_g4:
    st.write("*Distribución por Color de Cabello*")
    if not df_filtrado.empty:

        COLOR_CABELLO_MAP = {
            "Negro":   "#1a1a1a",
            "Castaño": "#6B3A2A",
            "Café":    "#7B4F2E",
            "Rubio":   "#E8C96D",
            "Rojo":    "#C0392B",
            "Rojizo":  "#C0392B",
            "Naranja": "#E67E22",
            "Canoso":  "#9E9E9E",
            "Gris":    "#9E9E9E",
            "Blanco":  "#E0E0E0",
            "Azul":    "#2980B9",
            "Verde":   "#27AE60",
            "Rosa":    "#E91E8C",
            "Morado":  "#8E44AD",
            "Violeta": "#8E44AD",
            "Black":   "#1a1a1a",
            "Brown":   "#6B3A2A",
            "Blonde":  "#E8C96D",
            "Red":     "#C0392B",
            "Gray":    "#9E9E9E",
            "White":   "#E0E0E0",
        }

        cabello_counts = df_filtrado["Color_Cabello"].value_counts().reset_index()
        cabello_counts.columns = ["Color_Cabello", "Cantidad"]
        cabello_counts["color_hex"] = cabello_counts["Color_Cabello"].map(
            lambda c: COLOR_CABELLO_MAP.get(c, "#555555")
        )

        fig_cabello = go.Figure()

        for _, row in cabello_counts.iterrows():
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
# PUNTO 10: 3era Fila de Gráficos — Tallas de Zapatos y Top 10 Barrios
# -------------------------------

st.subheader("3. Tallas de Zapatos y Barrios de Residencia")
col_g5, col_g6 = st.columns(2)

# --- Gráfico 5: Línea — Distribución de Tallas de Zapatos ---
with col_g5:
    st.write("*Distribución de Tallas de Zapatos*")
    if "Talla_Zapato" in df_filtrado.columns and not df_filtrado.empty:

        zapatos_counts = (
            df_filtrado["Talla_Zapato"]
            .dropna()
            .value_counts()
            .sort_index()
            .reset_index()
        )
        zapatos_counts.columns = ["Talla", "Cantidad"]

        fig_zapatos = go.Figure()

        # Área rellena debajo de la línea
        fig_zapatos.add_trace(go.Scatter(
            x=zapatos_counts["Talla"],
            y=zapatos_counts["Cantidad"],
            mode="lines+markers+text",
            text=zapatos_counts["Cantidad"],
            textposition="top center",
            textfont=dict(size=11, color="#1a5276"),
            line=dict(color="#2980B9", width=2.5, shape="spline"),
            marker=dict(
                size=9,
                color="#2980B9",
                line=dict(color="white", width=1.5),
            ),
            fill="tozeroy",
            fillcolor="rgba(41,128,185,0.12)",
            hovertemplate="Talla %{x}<br>Estudiantes: %{y}<extra></extra>",
            name="Talla de Zapato",
        ))

        fig_zapatos.update_layout(
            plot_bgcolor="rgba(245,247,250,1)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Talla de Zapato",
                showgrid=True,
                gridcolor="rgba(200,200,200,0.4)",
                tickmode="linear",
                dtick=1,
                title_font=dict(size=12, color="#444"),
            ),
            yaxis=dict(
                title="Nº Estudiantes",
                showgrid=True,
                gridcolor="rgba(200,200,200,0.4)",
                zeroline=True,
                zerolinecolor="rgba(150,150,150,0.3)",
                title_font=dict(size=12, color="#444"),
            ),
            showlegend=False,
            margin=dict(t=30, b=40, l=10, r=10),
            height=380,
        )
        st.plotly_chart(fig_zapatos, use_container_width=True)
    else:
        st.warning("No se encontró la columna Talla_Zapato.")

# --- Gráfico 6: Barras Horizontales — Top 10 Barrios de Residencia ---
with col_g6:
    st.write("*Top 10 Barrios de Residencia*")
    if not df_filtrado.empty:

        top_barrios = (
            df_filtrado["Barrio_Residencia"]
            .dropna()
            .value_counts()
            .head(10)
            .reset_index()
        )
        top_barrios.columns = ["Barrio", "Cantidad"]
        top_barrios = top_barrios.sort_values("Cantidad", ascending=True)  # orden ascendente para barras horizontales

        fig_barrios = go.Figure(go.Bar(
            x=top_barrios["Cantidad"],
            y=top_barrios["Barrio"],
            orientation="h",
            text=top_barrios["Cantidad"],
            textposition="outside",
            marker=dict(
                color=top_barrios["Cantidad"],
                colorscale="Teal",
                line=dict(color="rgba(0,77,77,0.6)", width=1),
                colorbar=dict(title="Cantidad"),
            ),
            hovertemplate="<b>%{y}</b><br>Estudiantes: %{x}<extra></extra>",
        ))

        fig_barrios.update_layout(
            plot_bgcolor="rgba(245,247,250,1)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Nº Estudiantes",
                showgrid=True,
                gridcolor="rgba(200,200,200,0.4)",
                zeroline=False,
                title_font=dict(size=12, color="#444"),
            ),
            yaxis=dict(
                title="",
                tickfont=dict(size=11, color="#333"),
            ),
            margin=dict(t=30, b=40, l=10, r=20),
            height=380,
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_barrios, use_container_width=True)
    else:
        st.warning("Sin datos para mostrar.")
  
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
# PUNTO 11: Top 5 Mayor Estatura y Mayor Peso
# -------------------------------
st.subheader("🏆 Modo gráfico Mayores Medidas Físicas")
col_t1, col_t2 = st.columns(2)

# --- Top 5 Mayor Estatura ---
with col_t1:
    st.write("*Top 5: Mayor Estatura*")
    if not df_filtrado.empty:
        top_estatura = df_filtrado.nlargest(5, "Estatura")[
            ["Nombre_Estudiante", "Apellido_Estudiante", "Estatura", "Peso", "Edad"]
        ].reset_index(drop=True)
        top_estatura.index += 1  # ranking desde 1

        fig_top_est = go.Figure()

        fig_top_est.add_trace(go.Bar(
            x=top_estatura["Estatura"],
            y=top_estatura["Nombre_Estudiante"] + " " + top_estatura["Apellido_Estudiante"],
            orientation="h",
            text=[f"{v:.2f} m" for v in top_estatura["Estatura"]],
            textposition="outside",
            marker=dict(
                color=top_estatura["Estatura"],
                colorscale=[
                    [0.0,  "#A8D8EA"],
                    [0.5,  "#3A86C8"],
                    [1.0,  "#1A3A5C"],
                ],
                line=dict(color="white", width=1.2),
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Estatura: %{x:.2f} m<extra></extra>"
            ),
        ))

        fig_top_est.update_layout(
            plot_bgcolor="rgba(245,247,250,1)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Estatura (m)",
                showgrid=True,
                gridcolor="rgba(200,200,200,0.4)",
                zeroline=False,
                range=[
                    top_estatura["Estatura"].min() - 0.05,
                    top_estatura["Estatura"].max() + 0.08,
                ],
                title_font=dict(size=12, color="#444"),
            ),
            yaxis=dict(
                autorange="reversed",
                tickfont=dict(size=11, color="#333"),
            ),
            margin=dict(t=20, b=30, l=10, r=60),
            height=280,
            showlegend=False,
        )
        st.plotly_chart(fig_top_est, use_container_width=True)

    else:
        st.warning("Sin datos para mostrar.")

# --- Top 5 Mayor Peso ---
with col_t2:
    st.write("*Top 5: Mayor Peso*")
    if not df_filtrado.empty:
        top_peso = df_filtrado.nlargest(5, "Peso")[
            ["Nombre_Estudiante", "Apellido_Estudiante", "Estatura", "Peso", "Edad"]
        ].reset_index(drop=True)
        top_peso.index += 1

        fig_top_peso = go.Figure()

        fig_top_peso.add_trace(go.Bar(
            x=top_peso["Peso"],
            y=top_peso["Nombre_Estudiante"] + " " + top_peso["Apellido_Estudiante"],
            orientation="h",
            text=[f"{v:.1f} kg" for v in top_peso["Peso"]],
            textposition="outside",
            marker=dict(
                color=top_peso["Peso"],
                colorscale=[
                    [0.0,  "#F9C6C6"],
                    [0.5,  "#E05C5C"],
                    [1.0,  "#7B1A1A"],
                ],
                line=dict(color="white", width=1.2),
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Peso: %{x:.1f} kg<extra></extra>"
            ),
        ))

        fig_top_peso.update_layout(
            plot_bgcolor="rgba(245,247,250,1)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Peso (kg)",
                showgrid=True,
                gridcolor="rgba(200,200,200,0.4)",
                zeroline=False,
                range=[
                    top_peso["Peso"].min() - 3,
                    top_peso["Peso"].max() + 8,
                ],
                title_font=dict(size=12, color="#444"),
            ),
            yaxis=dict(
                autorange="reversed",
                tickfont=dict(size=11, color="#333"),
            ),
            margin=dict(t=20, b=30, l=10, r=60),
            height=280,
            showlegend=False,
        )
        st.plotly_chart(fig_top_peso, use_container_width=True)

    else:
        st.warning("Sin datos para mostrar.")
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

# -------------------------------
# PUNTO 12: Resumen Estadístico en 3 columnas
# -------------------------------
st.subheader("📊 Resumen Estadístico Físico modo gráfico")
col_s1, col_s2, col_s3 = st.columns(3)

STAT_LABELS = {
    "count": "Conteo",
    "mean":  "Promedio",
    "std":   "Desv. Estándar",
    "min":   "Mínimo",
    "25%":   "Percentil 25%",
    "50%":   "Mediana",
    "75%":   "Percentil 75%",
    "max":   "Máximo",
}

def render_stat_chart(col, variable: str, titulo: str, color_scale: list, unidad: str):
    with col:
        st.write(f"*{titulo}*")
        if not df_filtrado.empty and variable in df_filtrado.columns:
            stats = df_filtrado[variable].dropna().describe()
            stat_df = pd.DataFrame({
                "Estadístico": [STAT_LABELS.get(k, k) for k in stats.index],
                "Valor": stats.values,
            })

            fig_stat = go.Figure()

            fig_stat.add_trace(go.Bar(
                x=stat_df["Valor"],
                y=stat_df["Estadístico"],
                orientation="h",
                text=[f"{v:.2f} {unidad}" for v in stat_df["Valor"]],
                textposition="outside",
                marker=dict(
                    color=stat_df["Valor"],
                    colorscale=color_scale,
                    line=dict(color="white", width=1),
                ),
                hovertemplate="<b>%{y}</b>: %{x:.2f}<extra></extra>",
            ))

            fig_stat.update_layout(
                plot_bgcolor="rgba(245,247,250,1)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(200,200,200,0.4)",
                    zeroline=False,
                    title_font=dict(size=11, color="#444"),
                    tickfont=dict(size=10),
                ),
                yaxis=dict(
                    autorange="reversed",
                    tickfont=dict(size=11, color="#333"),
                ),
                margin=dict(t=10, b=20, l=10, r=70),
                height=310,
                showlegend=False,
            )
            st.plotly_chart(fig_stat, use_container_width=True)

        else:
            st.warning(f"Sin datos para {titulo}.")

# Renderizar las 3 columnas estadísticas
render_stat_chart(
    col_s1, "Estatura", "Estadísticas de Estatura",
    [[0.0, "#A8D8EA"], [0.5, "#3A86C8"], [1.0, "#1A3A5C"]], "m"
)
render_stat_chart(
    col_s2, "Peso", "Estadísticas de Peso",
    [[0.0, "#F9C6C6"], [0.5, "#E05C5C"], [1.0, "#7B1A1A"]], "kg"
)
render_stat_chart(
    col_s3, "IMC", "Estadísticas de IMC",
    [[0.0, "#C8F7C5"], [0.5, "#27AE60"], [1.0, "#0B5E2F"]], ""
)