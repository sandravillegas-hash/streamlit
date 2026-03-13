import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import os
from PIL import Image

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Sandra Villegas - Talento Tech",
    page_icon="🎓",
    layout="wide"
)

# --- SOLUCIÓN AL ERROR: CSS PROFESIONAL ---
# Se cambió 'unsafe_allow_stdio' por 'unsafe_allow_html'
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        background-color: #1f77b4; 
        color: white; 
        font-weight: bold;
        height: 3.5em;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #155a8a; border: 1px solid #ffffff; }
    .help-icon { color: #1f77b4; font-size: 1.3rem; font-weight: bold; }
    .doc-box {
        padding: 20px;
        background-color: #ffffff;
        border-left: 5px solid #1f77b4;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS (Kaggle) ---
@st.cache_data
def load_data():
    try:
        # Descarga automática desde Kaggle
        path = kagglehub.dataset_download("sehaj1104/student-productivity-and-digital-distraction-dataset")
        files = [f for f in os.listdir(path) if f.endswith('.csv')]
        if not files: return None
        full_path = os.path.join(path, files[0])
        df = pd.read_csv(full_path)
        # Limpieza de nombres de columnas
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error en la conexión con Kaggle: {e}")
        return None

# --- SISTEMA DE NAVEGACIÓN ---
if 'view' not in st.session_state:
    st.session_state.view = 'landing'

# --- 1. LANDING PAGE ---
if st.session_state.view == 'landing':
    st.title("🚀 Impacto de la Distracción Digital")
    st.markdown("### Proyecto Integrador de Análisis de Datos | Talento Tech")
    st.markdown("---")
    
    col_info, col_img = st.columns([1, 1], gap="large")
    
    with col_info:
        st.subheader("Entendiendo el Dataset")
        st.write("""
            Este análisis aborda uno de los desafíos más grandes de la educación moderna: 
            **¿Cómo influyen nuestros dispositivos en nuestra capacidad de producir resultados?**
            
            A través de este panel, Sandra Villegas explora la relación entre:
            - **Nivel de Distracción Digital:** El ruido tecnológico constante.
            - **Puntaje de Productividad:** La eficiencia percibida del estudiante.
            - **Hábitos de Estudio:** La inversión de tiempo vs. resultados.
            
            Utilizamos técnicas avanzadas de visualización para identificar si la tecnología 
            es un catalizador o un obstáculo.
        """)
        if st.button("INGRESAR AL PANEL DE TRABAJO ➡️"):
            st.session_state.view = 'dashboard'
            st.rerun()

    with col_img:
        try:
            # Se usa la imagen proporcionada por el usuario
            image = Image.open("digitalDistraction.jpg")
            st.image(image, caption="Analista: Sandra Villegas", use_container_width=True)
        except:
            st.info("💡 Coloque el archivo 'digitalDistraction.jpg' en la raíz para visualizar la imagen temática.")

    st.markdown("---")
    st.write("**Desarrollado por:** Sandra Villegas")

# --- 2. PANEL DE TRABAJO (DASHBOARD) ---
elif st.session_state.view == 'dashboard':
    st.sidebar.title("⚙️ Configuración")
    st.sidebar.markdown(f"**Usuario:** Sandra Villegas")
    if st.sidebar.button("🏠 Regresar al Inicio"):
        st.session_state.view = 'landing'
        st.rerun()
    
    df = load_data()
    
    if df is not None:
        st.title("📊 Panel de Análisis Experto")
        st.markdown("Visualización de variables críticas de productividad.")
        
        # --- KPIs ---
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Estudiantes", len(df))
        kpi2.metric("Media Productividad", f"{df['Productivity_Score'].mean():.2f}")
        kpi3.metric("Promedio Distracción", f"{df['Digital_Distraction_Score'].mean():.2f}")

        st.markdown("---")

        # --- GRÁFICO 1: MAPA DE CALOR (CORRELACIÓN) ---
        st.header("1. Sinergia y Correlación de Variables")
        tab1, tab2, tab3 = st.tabs(["📊 Gráfico de Calor", "❓ Explicación", "📖 Documentación"])
        
        with tab1:
            fig, ax = plt.subplots(figsize=(10, 6))
            # Filtrar solo columnas numéricas
            numeric_cols = df.select_dtypes(include=['float64', 'int64'])
            sns.heatmap(numeric_cols.corr(), annot=True, cmap="YlGnBu", ax=ax)
            st.pyplot(fig)
        
        with tab2:
            st.markdown("### <span class='help-icon'>❓</span> Interpretación del Experto")
            st.markdown("""
                <div class='doc-box'>
                Este mapa utiliza el coeficiente de Pearson. Los valores cercanos a <b>-1</b> 
                indican una relación inversa fuerte. Si observamos colores oscuros entre la 
                distracción y la productividad, confirmamos que el uso de dispositivos 
                perjudica directamente el rendimiento académico.
                </div>
            """, unsafe_allow_html=True)
            
        with tab3:
            st.markdown("#### Detalles Técnicos")
            st.code("sns.heatmap(df.corr(), annot=True, cmap='YlGnBu')")
            st.write("Librería: Seaborn. Permite identificar patrones de dependencia lineal entre variables cuantitativas.")

        st.markdown("---")

        # --- GRÁFICO 2: REGRESIÓN LINEAL (IMPACTO) ---
        st.header("2. Tendencia: Distracción vs Productividad")
        tab1, tab2, tab3 = st.tabs(["📊 Gráfico Regresión", "❓ Explicación", "📖 Documentación"])
        
        with tab1:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.regplot(data=df, x='Digital_Distraction_Score', y='Productivity_Score', 
                        scatter_kws={'alpha':0.4}, line_kws={'color':'#d62728'}, ax=ax)
            st.pyplot(fig)
            
        with tab2:
            st.markdown("### <span class='help-icon'>❓</span> ¿Qué nos dice la tendencia?")
            st.markdown("""
                <div class='doc-box'>
                La línea roja representa la tendencia promedio. Una pendiente descendente es la 
                prueba estadística de que a mayor distracción digital, los niveles de productividad 
                tienden a caer de forma sistemática en la población estudiantil.
                </div>
            """, unsafe_allow_html=True)

        with tab3:
            st.markdown("#### Implementación")
            st.write("Utilizamos `sns.regplot` para combinar un diagrama de dispersión con un ajuste de modelo lineal.")

        st.markdown("---")

        # --- GRÁFICO 3: DISTRIBUCIÓN POR GÉNERO ---
        if 'Gender' in df.columns:
            st.header("3. Distribución de Productividad por Género")
            tab1, tab2, tab3 = st.tabs(["📊 Gráfico de Violín", "❓ Explicación", "📖 Documentación"])
            
            with tab1:
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.violinplot(data=df, x='Gender', y='Productivity_Score', palette="Set2", ax=ax)
                st.pyplot(fig)
                
            with tab2:
                st.markdown("### <span class='help-icon'>❓</span> Análisis de Densidad")
                st.markdown("""
                    <div class='doc-box'>
                    El gráfico de violín nos muestra dónde se concentra la mayor cantidad de estudiantes. 
                    Si el 'cuerpo' del violín está más arriba en un género, ese grupo muestra una 
                    mayor resiliencia a las distracciones digitales.
                    </div>
                """, unsafe_allow_html=True)

            with tab3:
                st.markdown("#### Documentación")
                st.write("`sns.violinplot` es superior al boxplot porque muestra la distribución de probabilidad de los datos.")

        # Tabla de datos crudos
        with st.expander("📂 Explorar registros originales (Dataset de Kaggle)"):
            st.dataframe(df, use_container_width=True)
    else:
        st.error("Error crítico: No se pudo cargar el dataset desde Kagglehub.")
