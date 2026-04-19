import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from datetime import datetime
df = pd.read_excel(r"C:\Users\thoma\OneDrive\Escritorio\Plantilla_Estudiantes_Grupo_052_DashBoard.xlsx")
print(df)


# 2. Convertir fechas con formato mixto
df["Fecha_Nacimiento"] = pd.to_datetime(df["Fecha_Nacimiento"], format="mixed", dayfirst=True)

# 3. Limpiar columna Peso 
df["Peso"] = df["Peso"].astype(str).str.replace("kg", "", case=False).str.strip()
df["Peso"] = pd.to_numeric(df["Peso"], errors="coerce")

# Calcular Edad
df["Edad"] = (datetime.now() - df["Fecha_Nacimiento"]).dt.days // 365

# Calcular IMC 
df["IMC"] = df["Peso"] / (df["Estatura"] ** 2)

#  Clasificación IMC 
def clasificar_imc(imc):
    if pd.isna(imc):
        return None
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25:
        return "Adecuado"
    elif imc < 30:
        return "Sobrepeso"
    elif imc < 35:
        return "Obesidad grado 1"
    elif imc < 40:
        return "Obesidad grado 2"
    else:
        return "Obesidad grado 3"

df["Clasificación_IMC"] = df["IMC"].apply(clasificar_imc)



# Mostrar el archivo completo
print(df)

df.to_excel(r"C:\Users\thoma\OneDrive\Escritorio\DashboardPA\Estudiantes_ProcesadoLimpio.xlsx", index=False)