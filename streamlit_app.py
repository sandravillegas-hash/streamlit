import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import os
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Talento Tech - Análisis de Productividad",
    page_icon="🎓",
    layout="wide"
)

# --- ESTILOS PROFESIONALES (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #1f77b4; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        white-space: pre-wrap; 
        background-color: #f1f3f5; 
        border-radius: 10px 10px 0 0; 
        gap: 1px; 
        padding-top: 10px; 
        padding-bottom: 10px; 
    }
    .help-icon { color: #1f77b4; font-size: 1.2rem; cursor: help; }
    </style>
    """, unsafe_allow_stdio=True)

# --- LÓGICA DE DATOS ---
@st.cache_data
def load_data():
    try:
        path = kagglehub.dataset_download("sehaj1104/student-productivity-and-digital-distraction-dataset")
        csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
        full_path = os.path.join(path, csv_files[0])
        df = pd.read_csv(full_path)
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error al descargar los datos: {e}")
        return None

# --- ESTADO DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def change_page(page_name):
    st.session_state.page = page_name

# --- LANDING PAGE ---
if st.session_state.page == 'landing':
    st.title("🚀 Bienvenidos al Análisis de Productividad Digital")
    st.markdown("---")
    
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.subheader("Sobre el Proyecto Integrador")
        st.write("""
            Este proyecto analiza el impacto de las distracciones digitales en la productividad académica. 
            Utilizamos el dataset de Kaggle **'Student Productivity and Digital Distraction'** para identificar 
            patrones de comportamiento en estudiantes modernos.
            
            **Objetivos:**
            - Cuantificar la relación entre horas de pantalla y notas.
            - Identificar las aplicaciones más disruptivas.
            - Proponer estrategias basadas en datos para la mejora del enfoque.
        """)
        if st.button("Ingresar al Panel de Trabajo ➡️"):
            change_page('dashboard')
            st.rerun()

    with col_r:
        try:
            img = Image.open("digitalDistraction.jpg")
            st.image(img, caption="El desafío de la atención en la era digital", use_container_width=True)
        except:
            st.info("Imagen principal del tema.")

    st.info("Desarrollado por: **Sandra Villegas** | Talento Tech Nivel Integrador")

# --- DASHBOARD PRINCIPAL ---
elif st.session_state.page == 'dashboard':
    df = load_data()
    
    # Sidebar
    st.sidebar.title("🛠️ Panel de Control")
    st.sidebar.write("Sandra Villegas - Analista")
    if st.sidebar.button("🏠 Volver al Inicio"):
        change_page('landing')
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtros")
    if df is not None:
        gender_filter = st.sidebar.multiselect("Género", options=df['Gender'].unique(), default=df['Gender'].unique())
        df_view = df[df['Gender'].isin(gender_filter)]
    
    st.title("📊 Panel de Análisis de Datos")
    
    if df is not None:
        # Gráfico 1: Correlación
        st.header("1. Mapa de Calor: Sinergia de Variables")
        tab1, tab2, tab3 = st.tabs(["📈 Gráfico", "❓ Explicación", "📖 Documentación"])
        
        with tab1:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df_view.select_dtypes(include=['number']).corr(), annot=True, cmap="Blues", ax=ax)
            st.pyplot(fig)
        
        with tab2:
            st.markdown("### <span class='help-icon'>❓</span> ¿Qué estamos viendo?", unsafe_allow_stdio=True)
            st.write("Este mapa de calor muestra la fuerza de relación entre variables. Un valor cercano a 1 indica que cuando una variable sube, la otra también.")
            
        with tab3:
            st.markdown("#### Detalles Técnicos")
            st.code("sns.heatmap(data.corr(), annot=True, cmap='Blues')")
            st.write("Se utiliza el coeficiente de Pearson para evaluar dependencias lineales.")

        st.markdown("---")

        # Gráfico 2: Regresión
        st.header("2. Impacto de la Distracción en la Productividad")
        tab1, tab2, tab3 = st.tabs(["📈 Gráfico", "❓ Explicación", "📖 Documentación"])
        
        with tab1:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.regplot(data=df_view, x='Digital_Distraction_Score', y='Productivity_Score', 
                        scatter_kws={'alpha':0.5}, line_kws={'color':'red'}, ax=ax)
            ax.set_title("Relación Inversa: Distracción vs Productividad")
            st.pyplot(fig)
            
        with tab2:
            st.markdown("### <span class='help-icon'>❓</span> Análisis del Experto", unsafe_allow_stdio=True)
            st.write("Observamos una tendencia descendente. A mayor puntaje de distracción digital, los niveles de productividad tienden a disminuir sistemáticamente.")

        with tab3:
            st.markdown("#### Librerías")
            st.write("- **Seaborn regplot**: Combina un scatter plot con un ajuste de regresión lineal.")

        st.markdown("---")

        # Gráfico 3: Distribución
        st.header("3. Distribución de Horas de Estudio")
        tab1, tab2, tab3 = st.tabs(["📈 Gráfico", "❓ Explicación", "📖 Documentación"])
        
        with tab1:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(df_view['Study_Hours'], kde=True, color="#1f77b4", ax=ax)
            st.pyplot(fig)
            
        with tab2:
            st.markdown("### <span class='help-icon'>❓</span> Insights", unsafe_allow_stdio=True)
            st.write("La curva KDE nos muestra la densidad de estudiantes. Es vital identificar si la mayoría dedica pocas horas debido a las distracciones mencionadas.")

        with tab3:
            st.markdown("#### Parámetros")
            st.write("- **KDE**: Kernel Density Estimate, suaviza el histograma para ver la forma de la distribución.")

        # Tabla de datos al final
        with st.expander("Ver tabla de datos completa"):
            st.dataframe(df_view)

    else:
        st.warning("Cargando dataset...")
