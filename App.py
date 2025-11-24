import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Ruta Estadística", page_icon="📊", layout="centered")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #f0f2f6;
        color: #31333F;
        border: 1px solid #d6d6d8;
    }
    .stButton>button:hover {
        background-color: #ff4b4b;
        color: white;
        border: 1px solid #ff4b4b;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .result-box {
        padding: 20px;
        background-color: #e8f5e9;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE NAVEGACIÓN ---

def ir_a(paso):
    st.session_state.paso = paso

def reiniciar():
    st.session_state.paso = 'inicio'

# Inicializar estado si no existe
if 'paso' not in st.session_state:
    st.session_state.paso = 'inicio'

# --- ENCABEZADO ---
st.title("🧭 Ruta de Decisión Estadística")
st.markdown("Responde las preguntas para encontrar la prueba estadística ideal para tu investigación.")
st.divider()

# --- LÓGICA DE PREGUNTAS (UNA A LA VEZ) ---

# PASO 1: OBJETIVO
if st.session_state.paso == 'inicio':
    st.markdown('<p class="big-font">1. ¿Cuál es el objetivo principal de tu análisis?</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🅰️ Comparar\n(Grupos o mediciones)"):
            ir_a('comparar_grupos_cantidad')
    with col2:
        if st.button("🅱️ Relacionar\n(Asociación entre variables)"):
            ir_a('relacionar_tipo_vars')
    with col3:
        if st.button("©️ Predecir\n(Valores futuros)"):
            ir_a('res_regresion')

# --- RAMA: COMPARAR ---

# PASO 2: CANTIDAD DE GRUPOS
elif st.session_state.paso == 'comparar_grupos_cantidad':
    st.markdown('<p class="big-font">2. ¿Cuántos grupos o momentos estás comparando?</p>', unsafe_allow_html=True)
    
    if st.button("A. Solo dos grupos (ej. Hombres vs Mujeres, Antes vs Después)"):
        ir_a('comparar_dependencia')
    if st.button("B. Tres o más grupos (ej. Tratamiento A vs B vs C)"):
        ir_a('comparar_3_normalidad')
    
    st.markdown("---")
    if st.button("⬅️ Volver al inicio"): reiniciar()

# PASO 3: DEPENDENCIA (Para 2 grupos)
elif st.session_state.paso == 'comparar_dependencia':
    st.markdown('<p class="big-font">3. ¿Existe dependencia entre las muestras?</p>', unsafe_allow_html=True)
    
    if st.button("A. Independientes (Personas distintas en cada grupo)"):
        ir_a('comparar_2_indep_normalidad')
    if st.button("B. Relacionadas/Pareadas (Mismas personas medidas dos veces)"):
        ir_a('comparar_2_pareada_normalidad')

    st.markdown("---")
    if st.button("⬅️ Reiniciar"): reiniciar()

# PASO 4A: NORMALIDAD (Para 2 grupos independientes)
elif st.session_state.paso == 'comparar_2_indep_normalidad':
    st.markdown('<p class="big-font">4. ¿Tus datos tienen distribución NORMAL y varianzas iguales?</p>', unsafe_allow_html=True)
    st.info("💡 Tip: Usa Shapiro-Wilk para normalidad y Levene para varianzas.")
    
    if st.button("SÍ (Cumple supuestos paramétricos)"):
        ir_a('res_t_student_indep')
    if st.button("NO (Datos ordinales, pocos datos o no normales)"):
        ir_a('res_mann_whitney')

    st.markdown("---")
    if st.button("⬅️ Reiniciar"): reiniciar()

# PASO 4B: NORMALIDAD (Para 2 grupos relacionados)
elif st.session_state.paso == 'comparar_2_pareada_normalidad':
    st.markdown('<p class="big-font">4. ¿Las diferencias entre mediciones tienen distribución NORMAL?</p>', unsafe_allow_html=True)
    
    if st.button("SÍ (Cumple supuestos)"):
        ir_a('res_t_student_pareada')
    if st.button("NO (No normal o muestra pequeña)"):
        ir_a('res_wilcoxon')

    st.markdown("---")
    if st.button("⬅️ Reiniciar"): reiniciar()

# PASO 6: NORMALIDAD (Para 3+ grupos)
elif st.session_state.paso == 'comparar_3_normalidad':
    st.markdown('<p class="big-font">¿Tus datos cumplen con NORMALIDAD y homocedasticidad en todos los grupos?</p>', unsafe_allow_html=True)
    
    if st.button("SÍ (Cumple supuestos paramétricos)"):
        ir_a('res_anova')
    if st.button("NO (Datos ordinales o no normales)"):
        ir_a('res_kruskal')

    st.markdown("---")
    if st.button("⬅️ Reiniciar"): reiniciar()

# --- RAMA: RELACIONAR ---

# PASO 5: TIPO DE VARIABLES
elif st.session_state.paso == 'relacionar_tipo_vars':
    st.markdown('<p class="big-font">2. ¿Qué tipo de variables estás relacionando?</p>', unsafe_allow_html=True)
    
    if st.button("A. Exclusivamente Categóricas (Nominales/Ordinales)"):
        ir_a('res_chi')
    if st.button("B. Cuantitativas (Numéricas)"):
        ir_a('relacionar_linealidad')

    st.markdown("---")
    if st.button("⬅️ Volver al inicio"): reiniciar()

# PASO 7: LINEALIDAD Y NORMALIDAD
elif st.session_state.paso == 'relacionar_linealidad':
    st.markdown('<p class="big-font">3. ¿La relación es LINEAL y los datos son NORMALES?</p>', unsafe_allow_html=True)
    
    if st.button("SÍ (Lineal y Normal)"):
        ir_a('res_pearson')
    if st.button("NO (No lineal/monótona u Ordinal)"):
        ir_a('res_spearman')

    st.markdown("---")
    if st.button("⬅️ Reiniciar"): reiniciar()

# --- PANTALLAS DE RESULTADOS ---

def mostrar_resultado(nombre, tipo, objetivo, requisitos):
    st.markdown(f"""
        <div class="result-box">
            <h2>🏆 Resultado: {nombre}</h2>
            <p><strong>Tipo:</strong> {tipo}</p>
            <p><strong>Objetivo:</strong> {objetivo}</p>
            <p><strong>Requisitos clave:</strong> {requisitos}</p>
        </div>
    """, unsafe_allow_html=True)
    st.balloons()
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Realizar nueva consulta"):
        reiniciar()

# Resultados Finales
if st.session_state.paso == 'res_regresion':
    mostrar_resultado(
        "Regresión Lineal Simple", 
        "Paramétrica", 
        "Predecir una variable dependiente a partir de una independiente.", 
        "Relación lineal, normalidad de residuos, homocedasticidad."
    )

elif st.session_state.paso == 'res_t_student_indep':
    mostrar_resultado(
        "T de Student (Muestras Independientes)", 
        "Paramétrica", 
        "Comparar si las medias de dos grupos distintos son iguales.", 
        "Muestreo aleatorio, Distribución normal, Varianzas iguales."
    )

elif st.session_state.paso == 'res_mann_whitney':
    mostrar_resultado(
        "U de Mann-Whitney", 
        "No Paramétrica", 
        "Comparar dos grupos independientes (medianas/rangos) sin normalidad.", 
        "Datos ordinales o cuantitativos, grupos pequeños, muestras independientes."
    )

elif st.session_state.paso == 'res_t_student_pareada':
    mostrar_resultado(
        "T de Student (Muestras Relacionadas)", 
        "Paramétrica", 
        "Comparar dos mediciones en la misma muestra (antes/después).", 
        "Nivel de intervalo/razón, Distribución normal de las diferencias."
    )

elif st.session_state.paso == 'res_wilcoxon':
    mostrar_resultado(
        "Prueba de Wilcoxon", 
        "No Paramétrica", 
        "Comparar dos mediciones en los mismos sujetos (medianas/rangos).", 
        "Datos ordinales o cuantitativos, distribución libre (no normal)."
    )

elif st.session_state.paso == 'res_anova':
    mostrar_resultado(
        "ANOVA de un factor", 
        "Paramétrica", 
        "Comparar medias de 3 o más grupos independientes.", 
        "Normalidad en grupos, Varianzas iguales, Independencia."
    )

elif st.session_state.paso == 'res_kruskal':
    mostrar_resultado(
        "Kruskal-Wallis", 
        "No Paramétrica", 
        "Comparar 3 o más grupos (medianas/rangos) sin suponer normalidad.", 
        "Variable ordinal o cuantitativa, distribuciones similares."
    )

elif st.session_state.paso == 'res_chi':
    mostrar_resultado(
        "Chi-Cuadrada", 
        "No Paramétrica", 
        "Determinar relación entre dos variables categóricas.", 
        "Variables nominales u ordinales, frecuencias esperadas suficientes."
    )

elif st.session_state.paso == 'res_pearson':
    mostrar_resultado(
        "Correlación de Pearson", 
        "Paramétrica", 
        "Medir fuerza y dirección de relación lineal entre variables.", 
        "Normalidad, Linealidad, Variables de intervalo/razón."
    )

elif st.session_state.paso == 'res_spearman':
    mostrar_resultado(
        "Correlación de Spearman", 
        "No Paramétrica", 
        "Evaluar relación monótona (ranking) entre variables.", 
        "Datos ordinales o cuantitativos, no requiere normalidad ni linealidad estricta."
    )
