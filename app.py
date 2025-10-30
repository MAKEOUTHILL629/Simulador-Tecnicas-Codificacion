"""
Interfaz Web Streamlit para el Simulador de Comunicaciones 5G/6G

Ejecutar con: streamlit run app.py
"""

import streamlit as st
import numpy as np
import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.simulator import CommunicationSimulator
from src.visualization.plots import SimulatorVisualizer
from src.metrics.performance import MetricsCalculator


def main():
    st.set_page_config(
        page_title="Simulador 5G/6G",
        page_icon="📡",
        layout="wide"
    )
    
    st.title("📡 Simulador de Sistemas de Comunicación 5G/6G")
    st.markdown("""
    Simulador modular para análisis de sistemas de comunicación multi-generacionales
    con codificación de fuente, codificación de canal, modulación digital y análisis de rendimiento.
    """)
    
    # Sidebar para configuración
    st.sidebar.header("⚙️ Configuración del Sistema")
    
    # Tecnología
    technology = st.sidebar.selectbox(
        "Tecnología",
        ["5G", "5G_Advanced", "6G"],
        help="Selecciona la generación tecnológica"
    )
    
    # Tipo de datos
    data_type = st.sidebar.selectbox(
        "Tipo de Datos",
        ["text", "audio", "image", "video"],
        help="Tipo de información a transmitir"
    )
    
    # Código de canal
    channel_code = st.sidebar.selectbox(
        "Código de Canal",
        ["LDPC", "Polar"],
        help="LDPC para datos, Polar para control"
    )
    
    # Modulación (filtrada por tecnología)
    if technology == "6G":
        modulation_options = ["QPSK", "16QAM", "64QAM", "256QAM", "1024QAM"]
    else:
        modulation_options = ["QPSK", "16QAM", "64QAM", "256QAM"]
    
    modulation = st.sidebar.selectbox(
        "Modulación",
        modulation_options,
        index=1,  # Default 16QAM
        help="Esquema de modulación digital"
    )
    
    # Modelo de canal
    channel_model = st.sidebar.selectbox(
        "Modelo de Canal",
        ["AWGN", "Rayleigh", "Rician"],
        help="AWGN: ideal, Rayleigh: NLOS, Rician: LOS"
    )
    
    # SNR
    snr_db = st.sidebar.slider(
        "SNR (dB)",
        min_value=0,
        max_value=30,
        value=10,
        step=1,
        help="Relación señal a ruido del canal"
    )
    
    # Modo
    mode = st.sidebar.selectbox(
        "Modo de Operación",
        ["SSCC"],  # JSCC pendiente
        help="SSCC: codificación separada fuente-canal"
    )
    
    st.sidebar.markdown("---")
    
    # Parámetros de simulación
    st.sidebar.header("📊 Parámetros de Simulación")
    
    num_bits = st.sidebar.number_input(
        "Número de Bits",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100,
        help="Cantidad de bits a transmitir"
    )
    
    # Botón de simulación
    if st.sidebar.button("▶️ Ejecutar Simulación", type="primary"):
        run_simulation(
            technology, data_type, channel_code, modulation,
            channel_model, snr_db, mode, num_bits
        )
    
    # Información adicional
    st.sidebar.markdown("---")
    st.sidebar.info("""
    💡 **Sugerencias:**
    - SNR bajo (<10 dB): usar QPSK
    - SNR alto (>15 dB): usar 64/256-QAM
    - Texto corto: usar Polar
    - Datos grandes: usar LDPC
    """)
    
    # Tabs principales
    tab1, tab2, tab3 = st.tabs(["📖 Información", "📈 Resultados", "❓ Ayuda"])
    
    with tab1:
        show_info_tab()
    
    with tab2:
        if 'results' not in st.session_state:
            st.info("👈 Configura los parámetros en el panel lateral y presiona 'Ejecutar Simulación'")
        else:
            show_results_tab()
    
    with tab3:
        show_help_tab()


def run_simulation(technology, data_type, channel_code, modulation,
                   channel_model, snr_db, mode, num_bits):
    """Ejecuta la simulación con los parámetros dados"""
    
    # Mostrar spinner mientras se ejecuta
    with st.spinner('Ejecutando simulación...'):
        try:
            # Crear configuración
            config = {
                'technology': technology,
                'data_type': data_type,
                'channel_code': channel_code,
                'modulation': modulation,
                'channel_model': channel_model,
                'snr_db': float(snr_db),
                'mode': mode
            }
            
            # Crear simulador
            sim = CommunicationSimulator(config)
            
            # Generar datos aleatorios
            data = np.random.randint(0, 2, num_bits)
            
            # Ejecutar simulación
            results = sim.run_simulation(data)
            
            # Guardar en session state
            st.session_state['results'] = results
            st.session_state['config'] = config
            st.session_state['data'] = data
            
            st.success("✅ Simulación completada exitosamente!")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error en la simulación: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


def show_results_tab():
    """Muestra los resultados de la simulación"""
    
    results = st.session_state['results']
    config = st.session_state['config']
    
    st.header("📊 Resultados de la Simulación")
    
    # Configuración usada
    with st.expander("🔧 Configuración Utilizada", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tecnología", config['technology'])
            st.metric("Tipo de Datos", config['data_type'])
        with col2:
            st.metric("Código de Canal", config['channel_code'])
            st.metric("Modulación", config['modulation'])
        with col3:
            st.metric("Canal", config['channel_model'])
            st.metric("SNR", f"{config['snr_db']} dB")
    
    # Métricas principales
    st.subheader("📈 Métricas de Rendimiento")
    
    metrics = results['metrics']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ber = metrics.get('ber', 0)
        st.metric(
            "BER",
            f"{ber:.6f}",
            delta=None,
            help="Bit Error Rate: proporción de bits erróneos"
        )
    
    with col2:
        entropy = metrics.get('entropy', 0)
        st.metric(
            "Entropía",
            f"{entropy:.2f} bits",
            help="Contenido promedio de información"
        )
    
    with col3:
        mi = metrics.get('mutual_information', 0)
        st.metric(
            "Info. Mutua",
            f"{mi:.2f} bits",
            help="Información transferida con éxito"
        )
    
    with col4:
        mse = metrics.get('mse', 0)
        st.metric(
            "MSE",
            f"{mse:.4f}",
            help="Error cuadrático medio"
        )
    
    # Métricas adicionales según tipo de datos
    if config['data_type'] in ['image', 'video']:
        col1, col2 = st.columns(2)
        with col1:
            psnr = metrics.get('psnr', 0)
            st.metric(
                "PSNR",
                f"{psnr:.2f} dB",
                help="Peak Signal-to-Noise Ratio"
            )
        with col2:
            ssim = metrics.get('ssim', 0)
            st.metric(
                "SSIM",
                f"{ssim:.4f}",
                help="Structural Similarity Index"
            )
    
    # Interpretación de resultados
    st.subheader("💡 Interpretación")
    
    ber_val = metrics.get('ber', 0)
    if ber_val < 1e-6:
        ber_status = "🟢 Excelente"
        ber_msg = "Calidad de transmisión óptima"
    elif ber_val < 1e-3:
        ber_status = "🟡 Bueno"
        ber_msg = "Calidad adecuada para comunicaciones"
    elif ber_val < 0.1:
        ber_status = "🟠 Aceptable"
        ber_msg = "Requiere corrección de errores adicional"
    else:
        ber_status = "🔴 Malo"
        ber_msg = "Canal de mala calidad, considere reducir la tasa o aumentar SNR"
    
    st.info(f"**Estado del Canal:** {ber_status} - {ber_msg}")
    
    # Estados intermedios
    with st.expander("🔍 Estados Intermedios del Pipeline"):
        intermediate = results['intermediate_states']
        
        for key, value in intermediate.items():
            if isinstance(value, np.ndarray) and len(value) > 0:
                st.write(f"**{key}:** Shape = {value.shape}, Dtype = {value.dtype}")


def show_info_tab():
    """Muestra información del simulador"""
    
    st.header("ℹ️ Acerca del Simulador")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Características")
        st.markdown("""
        - **Tecnologías:** 5G, 5G Advanced, 6G
        - **Tipos de Datos:** Texto, Audio, Imagen, Video
        - **Códigos de Canal:** LDPC, Polar
        - **Modulación:** QPSK, 16/64/256/1024-QAM
        - **Canales:** AWGN, Rayleigh, Rician
        - **Métricas:** BER, PSNR, SSIM, Entropía, etc.
        """)
    
    with col2:
        st.subheader("📚 Pipeline de Simulación")
        st.markdown("""
        1. 📥 Generación de Fuente
        2. 🗜️ Codificación de Fuente (compresión)
        3. 🛡️ Codificación de Canal (FEC)
        4. 📡 Modulación Digital
        5. 🌊 Transmisión por Canal
        6. 📻 Demodulación
        7. 🔓 Decodificación de Canal
        8. 📤 Decodificación de Fuente
        """)
    
    st.subheader("🔬 Fundamentos Teóricos")
    
    st.markdown("""
    El simulador implementa los principios fundamentales de la teoría de la información de Shannon:
    
    - **Codificación de Fuente:** Elimina redundancia (compresión)
    - **Codificación de Canal:** Añade redundancia controlada (protección)
    - **Modulación:** Mapea bits a símbolos complejos
    - **Canal:** Simula degradaciones reales (ruido, desvanecimiento)
    - **Decodificación:** Recupera información con soft decisions (LLRs)
    """)


def show_help_tab():
    """Muestra ayuda y guía de uso"""
    
    st.header("❓ Ayuda y Guía de Uso")
    
    st.subheader("🚀 Inicio Rápido")
    st.markdown("""
    1. **Selecciona la tecnología** (5G, 5G-A o 6G)
    2. **Elige el tipo de datos** a transmitir
    3. **Configura los parámetros** de codificación y modulación
    4. **Ajusta el SNR** según las condiciones del canal
    5. **Ejecuta la simulación** y analiza los resultados
    """)
    
    st.subheader("💡 Recomendaciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Para SNR Bajo (<10 dB):**
        - Usar QPSK (más robusto)
        - Preferir Polar para latencia baja
        - Tasa de código baja (más redundancia)
        """)
    
    with col2:
        st.markdown("""
        **Para SNR Alto (>15 dB):**
        - Usar 64-QAM o superior
        - LDPC para datos grandes
        - Tasa de código alta (menos redundancia)
        """)
    
    st.subheader("📊 Interpretación de Métricas")
    
    with st.expander("BER (Bit Error Rate)"):
        st.markdown("""
        - **< 10⁻⁶:** Excelente (calidad broadcast)
        - **< 10⁻³:** Bueno (comunicaciones de voz)
        - **< 10⁻²:** Aceptable (requiere FEC adicional)
        - **> 10⁻¹:** Inaceptable
        """)
    
    with st.expander("PSNR (Peak Signal-to-Noise Ratio)"):
        st.markdown("""
        - **> 40 dB:** Excelente calidad
        - **30-40 dB:** Buena calidad
        - **20-30 dB:** Calidad aceptable
        - **< 20 dB:** Mala calidad
        """)
    
    with st.expander("Entropía"):
        st.markdown("""
        Mide el contenido promedio de información:
        - **Alta:** Muchos datos, difícil de comprimir
        - **Baja:** Redundante, fácil de comprimir
        """)
    
    st.subheader("📖 Documentación")
    st.markdown("""
    Para más información, consulta:
    - `manual-user.md` - Guía de usuario completa
    - `manual-dev.md` - Guía para desarrolladores
    - `README.md` - Especificación técnica
    """)


if __name__ == "__main__":
    main()
