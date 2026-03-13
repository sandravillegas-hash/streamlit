import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import os
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Sandra Villegas - Talento Tech",
    page_icon="🎓",
    layout="wide"
)

# --- ESTILOS CSS (CORREGIDO unsafe_allow_html) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 12px; background-color: #1f77b4; 
        color: white; font-weight: bold; height: 3.5em; border: none;
    }
    .help-icon { color: #1f77b4; font-size: 1.2rem; font-weight: bold; }
    .doc-box {
        padding: 20px; background-color: #ffffff;
        border-left: 5px solid #1f77b4; border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA Y LIMPIEZA DE DATOS (SOLUCIÓN AL KEYERROR) ---
@st.cache_data
def load_data():
    try:
        path = kagglehub.dataset_download("sehaj1104/student-productivity-and-digital-distraction-dataset")
        files = [f for f in os.listdir(path) if f.endswith('.csv')]
        if not files: return None
        
        full_path = os.path.join(path, files[0])
        df = pd.read_csv(full_path)
        
        # NORMALIZACIÓN DE COLUMNAS:
        # 1. Quitamos espacios al inicio/final
        # 2. Reemplazamos espacios internos por guiones bajos
        df.columns = df.columns.str.strip().str.replace(' ', '_')
        
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None

# --- NAVEGACIÓN ---
if 'view' not in st.session_state:
    st.session_state.view = 'landing'

# --- LANDING PAGE ---
if st.session_state.view == 'landing':
    st.title("🚀 Análisis de Productividad Digital")
    st.write("### Proyecto Integrador | Sandra Villegas")
    st.markdown("---")
    
    col_l, col_r = st.columns([1, 1], gap="large")
    
    with col_l:
        st.subheader("Sobre el Proyecto")
        st.write("""
            Bienvenidos al panel de análisis de Talento Tech. Este estudio investiga 
            cómo las distracciones tecnológicas afectan el rendimiento académico.
            
            **Variables Clave:**
            - **Productividad:** Nivel de eficiencia en tareas.
            - **Distracción Digital:** Interrupciones por dispositivos.
            - **Estudio:** Horas dedicadas al aprendizaje.
        """)
        if st.button("INGRESAR AL PANEL DE TRABAJO 📈"):
            st.session_state.view = 'dashboard'
            st.rerun()

    with col_r:
        try:
            image = Image.open("digitalDistraction.jpg")
            st.image(image, caption="Analista: Sandra Villegas", use_container_width=True)
        except:
            st.info("💡 Coloca 'digitalDistraction.jpg' en la carpeta para ver la imagen.")

# --- DASHBOARD (SOLUCIÓN A LOS ERRORES DE COLUMNA) ---
elif st.session_state.view == 'dashboard':
    st.sidebar.title("⚙️ Controles")
    if st.sidebar.button("🏠 Regresar al Inicio"):
        st.session_state.view = 'landing'
        st.rerun()

    df = load_data()

    if df is not None:
        st.title("📊 Panel de Análisis Experto")
        
        # Validación de columnas antes de calcular métricas
        target_cols = ['Productivity_Score', 'Digital_Distraction_Score', 'Study_Hours']
        
        # Verificamos cuáles columnas del dataset coinciden con lo que buscamos
        missing_cols = [c for c in target_cols if c not in df.columns]
        
        if missing_cols:
            st.warning(f"Atención: No se encontraron las columnas: {missing_cols}")
            st.write("Columnas detectadas en el archivo:", list(df.columns))
            # Intento de mapeo automático si los nombres son parecidos
            st.stop() # Detenemos la ejecución para evitar el error de KPI

        # --- KPIs ---
        k1, k2, k3 = st.columns(3)
        k1.metric("Estudiantes", len(df))
        k2.metric("Media Productividad", f"{df['Productivity_Score'].mean():.2f}")
        k3.metric("Media Distracción", f"{df['Digital_Distraction_Score'].mean():.2f}")

        st.markdown("---")

        # --- GRÁFICO 1: CORRELACIÓN ---
        st.header("1. Mapa de Calor (Seaborn)")
        t1, t2, t3 = st.tabs(["📊 Gráfico", "❓ Ayuda", "📖 Documentación"])
        
        with t1:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df.select_dtypes(include=['number']).corr(), annot=True, cmap="mako", ax=ax)
            st.pyplot(fig)
        with t2:
            st.markdown("<div class='doc-box'>Este gráfico muestra la relación entre variables. Un valor negativo fuerte entre distracción y productividad confirma el impacto negativo del celular.</div>", unsafe_allow_html=True)
        with t3:
            st.code("sns.heatmap(df.corr(), annot=True, cmap='mako')")

        st.markdown("---")

        # --- GRÁFICO 2: REGRESIÓN ---
        st.header("2. Impacto: Distracción vs Productividad")
        t1, t2, t3 = st.tabs(["📊 Gráfico", "❓ Ayuda", "📖 Documentación"])
        
        with t1:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.regplot(data=df, x='Digital_Distraction_Score', y='Productivity_Score', 
                        scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax)
            st.pyplot(fig)
        with t2:
            st.markdown("<div class='doc-box'>La línea roja muestra la tendencia: si baja, significa que a más distracción, menos productividad hay.</div>", unsafe_allow_html=True)
        with t3:
            st.write("Gráfico de regresión lineal para identificar tendencias de comportamiento.")

        with st.expander("📂 Explorar Datos Crudos"):
            st.dataframe(df)
    else:
        st.error("No se pudo cargar el dataset.")

