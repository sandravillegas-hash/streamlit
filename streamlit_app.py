import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import os
from PIL import Image

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sandra Villegas - Talento Tech", layout="wide")

# --- ESTILOS CSS (CORREGIDO) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 10px; background-color: #1f77b4; 
        color: white; font-weight: bold; height: 3.5em; border: none;
    }
    .expert-card {
        padding: 20px; background-color: white; border-radius: 12px;
        border-left: 5px solid #1f77b4; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .help-icon { color: #1f77b4; font-weight: bold; cursor: help; }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    try:
        # Descarga el dataset
        path = kagglehub.dataset_download("sehaj1104/student-productivity-and-digital-distraction-dataset")
        files = [f for f in os.listdir(path) if f.endswith('.csv')]
        full_path = os.path.join(path, files[0])
        df = pd.read_csv(full_path)
        # Limpieza básica de espacios en nombres
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None

# --- NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- 1. LANDING PAGE ---
if st.session_state.page == 'landing':
    st.title("🚀 Impacto de la Distracción Digital en Estudiantes")
    st.write("### Proyecto Integrador | Sandra Villegas - Talento Tech")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.subheader("Contexto del Análisis")
        st.write("""
            En la actualidad, el uso de dispositivos digitales es omnipresente. Pero, 
            ¿cómo afecta realmente esto a nuestra productividad y enfoque académico?
            
            Este dashboard analiza 20,000 registros de estudiantes para encontrar:
            - La correlación entre **uso de teléfono** y **productividad**.
            - Patrones de **horas de estudio** efectivas.
            - Impacto del estilo de vida en el rendimiento final.
        """)
        if st.button("INGRESAR AL PANEL DE TRABAJO ➡️"):
            st.session_state.page = 'dashboard'
            st.rerun()
    with col2:
        try:
            img = Image.open("digitalDistraction.jpg")
            st.image(img, caption="Concentración vs. Tecnología", use_container_width=True)
        except:
            st.info("💡 Asegúrese de incluir 'digitalDistraction.jpg' en su carpeta.")

# --- 2. DASHBOARD ---
else:
    st.sidebar.title("🛠️ Configuración")
    st.sidebar.write("Analista: **Sandra Villegas**")
    if st.sidebar.button("🏠 Volver al Inicio"):
        st.session_state.page = 'landing'
        st.rerun()

    df = load_data()

    if df is not None:
        st.title("📊 Panel de Análisis de Productividad")
        
        # Mapeo de columnas para que el código sea legible
        # Nombres reales en el dataset: 'productivity_score', 'phone_usage_hours', 'study_hours_per_day'
        col_prod = 'productivity_score'
        col_dist = 'phone_usage_hours'
        col_study = 'study_hours_per_day'

        # Verificación de seguridad
        if all(c in df.columns for c in [col_prod, col_dist, col_study]):
            
            # KPIs
            k1, k2, k3 = st.columns(3)
            k1.metric("Estudiantes", f"{len(df):,}")
            k2.metric("Promedio Productividad", f"{df[col_prod].mean():.2f}%")
            k3.metric("Uso Teléfono Avg", f"{df[col_dist].mean():.1f}h")

            st.markdown("---")

            # Gráfico 1: Correlación
            st.header("1. Mapa de Calor Estadístico")
            t1, t2, t3 = st.tabs(["📉 Gráfico", "❓ Ayuda", "📖 Documentación"])
            with t1:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(df.select_dtypes(include=['number']).corr(), annot=True, cmap="mako", ax=ax)
                st.pyplot(fig)
            with t2:
                st.markdown("<div class='expert-card'><span class='help-icon'>❓</span> Un valor cercano a -1 entre el uso del teléfono y la productividad confirmaría que la tecnología distrae significativamente al estudiante.</div>", unsafe_allow_html=True)
            with t3:
                st.write("Generado con `sns.heatmap`. Muestra la matriz de correlación de Pearson.")

            st.markdown("---")

            # Gráfico 2: Regresión
            st.header("2. Regresión: Teléfono vs Productividad")
            t1, t2, t3 = st.tabs(["📉 Gráfico", "❓ Ayuda", "📖 Documentación"])
            with t1:
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.regplot(data=df.sample(2000), x=col_dist, y=col_prod, scatter_kws={'alpha':0.2}, line_kws={'color':'red'}, ax=ax)
                st.pyplot(fig)
            with t2:
                st.markdown("<div class='expert-card'><span class='help-icon'>❓</span> La pendiente descendente de la línea roja indica que a mayor uso del teléfono, menor es el puntaje de productividad.</div>", unsafe_allow_html=True)
            with t3:
                st.write("`sns.regplot`: Realiza una regresión lineal sobre una muestra de los datos.")

            # Tabla de datos
            with st.expander("📂 Explorar Datos Crudos"):
                st.dataframe(df.head(100), use_container_width=True)
        else:
            st.error("Error: Las columnas esperadas no coinciden con el dataset descargado.")
            st.write("Columnas encontradas:", list(df.columns))


