"""
Interfaz Web Streamlit COMPLETA para el Simulador de Comunicaciones 5G/6G
Con TODAS las visualizaciones y gráficas integradas

Ejecutar con: streamlit run app_enhanced.py
"""

import streamlit as st
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
    
    st.title("📡 Simulador Completo de Sistemas de Comunicación 5G/6G")
    st.markdown("""
    **Simulador modular profesional** para análisis de sistemas de comunicación multi-generacionales
    con codificación de fuente, codificación de canal, modulación digital y análisis de rendimiento completo.
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
        ["SSCC", "JSCC"],
        help="SSCC: codificación separada, JSCC: codificación conjunta"
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
    
    # Opciones de visualización
    st.sidebar.markdown("---")
    st.sidebar.header("📈 Visualizaciones")
    
    show_constellation = st.sidebar.checkbox("Diagrama de Constelación", value=True)
    show_waveforms = st.sidebar.checkbox("Formas de Onda I/Q", value=True)
    show_llr_dist = st.sidebar.checkbox("Distribución de LLRs", value=True)
    show_intermediate = st.sidebar.checkbox("Estados Intermedios", value=False)
    
    # Botón de simulación
    if st.sidebar.button("▶️ Ejecutar Simulación", type="primary"):
        run_simulation(
            technology, data_type, channel_code, modulation,
            channel_model, snr_db, mode, num_bits,
            show_constellation, show_waveforms, show_llr_dist, show_intermediate
        )
    
    # Información adicional
    st.sidebar.markdown("---")
    st.sidebar.info("""
    💡 **Sugerencias:**
    - SNR bajo (<10 dB): usar QPSK
    - SNR alto (>15 dB): usar 64/256-QAM
    - Texto corto: usar Polar
    - Datos grandes: usar LDPC
    - JSCC para degradación gradual
    """)
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Información", "📈 Resultados", "📊 Visualizaciones", "❓ Ayuda"])
    
    with tab1:
        show_info_tab()
    
    with tab2:
        if 'results' not in st.session_state:
            st.info("👈 Configura los parámetros en el panel lateral y presiona 'Ejecutar Simulación'")
        else:
            show_results_tab()
    
    with tab3:
        if 'results' not in st.session_state:
            st.info("👈 Ejecuta una simulación primero para ver las visualizaciones")
        else:
            show_visualizations_tab()
    
    with tab4:
        show_help_tab()


def run_simulation(technology, data_type, channel_code, modulation,
                   channel_model, snr_db, mode, num_bits,
                   show_constellation, show_waveforms, show_llr_dist, show_intermediate):
    """Ejecuta la simulación con los parámetros dados"""
    
    # Mostrar spinner mientras se ejecuta
    with st.spinner('🔄 Ejecutando simulación... Por favor espera'):
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
            st.session_state['viz_options'] = {
                'constellation': show_constellation,
                'waveforms': show_waveforms,
                'llr_dist': show_llr_dist,
                'intermediate': show_intermediate
            }
            
            # Generar visualizaciones
            generate_visualizations(results, config)
            
            st.success("✅ Simulación completada exitosamente!")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error en la simulación: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


def generate_visualizations(results, config):
    """Genera todas las visualizaciones"""
    
    viz = SimulatorVisualizer(output_dir='/tmp/sim_plots')
    st.session_state['visualizations'] = {}
    
    try:
        # 1. Diagrama de constelación
        if 'modulated_symbols' in results['intermediate_states']:
            symbols = results['intermediate_states']['modulated_symbols']
            fig = create_constellation_plot(symbols, config['modulation'])
            st.session_state['visualizations']['constellation'] = fig
        
        # 2. Formas de onda I/Q
        if 'modulated_symbols' in results['intermediate_states']:
            symbols = results['intermediate_states']['modulated_symbols']
            fig = create_waveform_plot(symbols)
            st.session_state['visualizations']['waveforms'] = fig
        
        # 3. Distribución de LLRs
        if 'demodulated_llrs' in results['intermediate_states']:
            llrs = results['intermediate_states']['demodulated_llrs']
            fig = create_llr_distribution_plot(llrs)
            st.session_state['visualizations']['llr_dist'] = fig
        
        # 4. Gráfica de métricas
        fig = create_metrics_summary(results['metrics'], config)
        st.session_state['visualizations']['metrics'] = fig
        
    except Exception as e:
        st.warning(f"Advertencia al generar visualizaciones: {str(e)}")


def create_constellation_plot(symbols, modulation_name):
    """Crea diagrama de constelación"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Limitar número de puntos para visualización
    max_points = 2000
    if len(symbols) > max_points:
        indices = np.random.choice(len(symbols), max_points, replace=False)
        plot_symbols = symbols[indices]
    else:
        plot_symbols = symbols
    
    ax.scatter(plot_symbols.real, plot_symbols.imag, alpha=0.5, s=20, c='blue', edgecolors='navy', linewidth=0.5)
    ax.set_xlabel('In-Phase (I)', fontsize=12)
    ax.set_ylabel('Quadrature (Q)', fontsize=12)
    ax.set_title(f'Diagrama de Constelación - {modulation_name}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    
    # Añadir círculo de referencia
    max_amp = np.max(np.abs(symbols))
    circle = plt.Circle((0, 0), max_amp, fill=False, linestyle='--', color='red', alpha=0.3)
    ax.add_artist(circle)
    
    plt.tight_layout()
    return fig


def create_waveform_plot(symbols):
    """Crea gráfica de formas de onda I/Q"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    
    # Limitar a primeros 200 símbolos para claridad
    plot_length = min(200, len(symbols))
    time_axis = np.arange(plot_length)
    
    # Componente I
    ax1.plot(time_axis, symbols[:plot_length].real, 'b-', linewidth=1, label='In-Phase (I)')
    ax1.set_ylabel('Amplitud I', fontsize=11)
    ax1.set_title('Forma de Onda In-Phase', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Componente Q
    ax2.plot(time_axis, symbols[:plot_length].imag, 'r-', linewidth=1, label='Quadrature (Q)')
    ax2.set_xlabel('Índice de Símbolo', fontsize=11)
    ax2.set_ylabel('Amplitud Q', fontsize=11)
    ax2.set_title('Forma de Onda Quadrature', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    return fig


def create_llr_distribution_plot(llrs):
    """Crea histograma de distribución de LLRs"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Filtrar infinitos y NaN
    valid_llrs = llrs[np.isfinite(llrs)]
    
    if len(valid_llrs) > 0:
        ax.hist(valid_llrs, bins=50, alpha=0.7, color='green', edgecolor='darkgreen')
        ax.set_xlabel('Valor LLR', fontsize=12)
        ax.set_ylabel('Frecuencia', fontsize=12)
        ax.set_title('Distribución de Log-Likelihood Ratios (LLRs)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Añadir líneas verticales en 0
        ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='LLR=0 (decisión incierta)')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'No hay LLRs válidos para mostrar', 
                ha='center', va='center', transform=ax.transAxes)
    
    plt.tight_layout()
    return fig


def create_metrics_summary(metrics, config):
    """Crea resumen visual de métricas"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Resumen de Métricas - {config["technology"]} / {config["modulation"]} / SNR={config["snr_db"]}dB', 
                 fontsize=14, fontweight='bold')
    
    # BER
    ax = axes[0, 0]
    ber = metrics.get('ber', 0)
    colors = ['green' if ber < 1e-3 else 'orange' if ber < 0.1 else 'red']
    ax.bar(['BER'], [ber], color=colors, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Bit Error Rate')
    ax.set_title('BER (Bit Error Rate)', fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, axis='y')
    ax.text(0, ber, f'{ber:.2e}', ha='center', va='bottom', fontweight='bold')
    
    # Información Teorética
    ax = axes[0, 1]
    entropy = metrics.get('entropy', 0)
    mi = metrics.get('mutual_information', 0)
    ax.bar(['Entropía', 'Info. Mutua'], [entropy, mi], 
           color=['blue', 'purple'], alpha=0.7, edgecolor='black')
    ax.set_ylabel('Bits')
    ax.set_title('Teoría de la Información', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    for i, (label, val) in enumerate([('Entropía', entropy), ('Info. Mutua', mi)]):
        ax.text(i, val, f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Calidad de señal (si aplica)
    ax = axes[1, 0]
    if config['data_type'] in ['image', 'video']:
        psnr = metrics.get('psnr', 0)
        ssim = metrics.get('ssim', 0)
        ax.bar(['PSNR (dB)', 'SSIM'], [psnr, ssim*100], 
               color=['cyan', 'magenta'], alpha=0.7, edgecolor='black')
        ax.set_ylabel('Valor')
        ax.set_title('Métricas de Calidad', fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.text(0, psnr, f'{psnr:.1f}', ha='center', va='bottom', fontweight='bold')
        ax.text(1, ssim*100, f'{ssim:.3f}', ha='center', va='bottom', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Métricas de calidad\nno aplican para\neste tipo de datos', 
                ha='center', va='center', transform=ax.transAxes, fontsize=11)
        ax.axis('off')
    
    # MSE
    ax = axes[1, 1]
    mse = metrics.get('mse', 0)
    ax.bar(['MSE'], [mse], color='orange', alpha=0.7, edgecolor='black')
    ax.set_ylabel('Mean Squared Error')
    ax.set_title('Error Cuadrático Medio', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.text(0, mse, f'{mse:.4f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    return fig


def show_results_tab():
    """Muestra los resultados de la simulación"""
    
    results = st.session_state['results']
    config = st.session_state['config']
    
    st.header("📊 Resultados de la Simulación")
    
    # Configuración usada
    with st.expander("🔧 Configuración Utilizada", expanded=True):
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
        delta_color = "inverse" if ber < 1e-3 else "normal"
        st.metric(
            "BER",
            f"{ber:.2e}",
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
        st.markdown("---")
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
    st.markdown("---")
    st.subheader("💡 Interpretación Automática")
    
    ber_val = metrics.get('ber', 0)
    if ber_val < 1e-6:
        ber_status = "🟢 Excelente"
        ber_msg = "Calidad de transmisión óptima. El sistema funciona perfectamente."
        ber_recommendation = "✅ Configuración ideal para este SNR."
    elif ber_val < 1e-3:
        ber_status = "🟡 Bueno"
        ber_msg = "Calidad adecuada para la mayoría de comunicaciones."
        ber_recommendation = "ℹ️ Considera aumentar SNR para aplicaciones críticas."
    elif ber_val < 0.1:
        ber_status = "🟠 Aceptable"
        ber_msg = "Requiere corrección de errores adicional."
        ber_recommendation = "⚠️ Aumenta SNR o usa modulación más robusta (QPSK)."
    else:
        ber_status = "🔴 Malo"
        ber_msg = "Canal de mala calidad. Transmisión poco confiable."
        ber_recommendation = "❌ ACCIÓN REQUERIDA: Reduce modulación o aumenta SNR significativamente."
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(f"**Estado del Canal:** {ber_status}\n\n{ber_msg}")
    with col2:
        st.warning(ber_recommendation)
    
    # Comparación con umbral teórico
    st.markdown("---")
    st.subheader("📐 Análisis Comparativo")
    
    # Calcular capacidad de Shannon
    snr_linear = 10**(config['snr_db']/10)
    shannon_capacity = np.log2(1 + snr_linear)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Capacidad Shannon",
            f"{shannon_capacity:.2f} bits/símbolo",
            help="Límite teórico de información"
        )
    with col2:
        efficiency = mi / shannon_capacity if shannon_capacity > 0 else 0
        st.metric(
            "Eficiencia Espectral",
            f"{efficiency*100:.1f}%",
            help="Información mutua / Capacidad Shannon"
        )
    with col3:
        if config['data_type'] in ['image', 'video'] and psnr > 0:
            quality_status = "Excelente" if psnr > 40 else "Buena" if psnr > 30 else "Aceptable" if psnr > 20 else "Mala"
            st.metric(
                "Calidad Visual",
                quality_status,
                f"{psnr:.1f} dB",
                help="Basado en PSNR"
            )
    
    # Estados intermedios (opcional)
    if st.session_state.get('viz_options', {}).get('intermediate', False):
        with st.expander("🔍 Estados Intermedios del Pipeline"):
            intermediate = results['intermediate_states']
            
            for key, value in intermediate.items():
                if isinstance(value, np.ndarray) and len(value) > 0:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**{key}:**")
                    with col2:
                        st.code(f"Shape: {value.shape}")
                    with col3:
                        st.code(f"Dtype: {value.dtype}")


def show_visualizations_tab():
    """Muestra todas las visualizaciones generadas"""
    
    st.header("📊 Visualizaciones Completas")
    
    if 'visualizations' not in st.session_state or not st.session_state['visualizations']:
        st.warning("No hay visualizaciones disponibles. Ejecuta una simulación primero.")
        return
    
    viz = st.session_state['visualizations']
    viz_options = st.session_state.get('viz_options', {})
    
    # 1. Diagrama de Constelación
    if viz_options.get('constellation', True) and 'constellation' in viz:
        st.subheader("🎯 Diagrama de Constelación")
        st.pyplot(viz['constellation'])
        st.markdown("""
        **Interpretación:** 
        - Los puntos representan símbolos modulados transmitidos
        - La dispersión indica el efecto del ruido del canal
        - Menor dispersión = mejor SNR = menor BER
        """)
        st.markdown("---")
    
    # 2. Formas de Onda I/Q
    if viz_options.get('waveforms', True) and 'waveforms' in viz:
        st.subheader("📡 Formas de Onda I/Q")
        st.pyplot(viz['waveforms'])
        st.markdown("""
        **Interpretación:**
        - **Componente I (In-Phase):** Parte real de los símbolos complejos
        - **Componente Q (Quadrature):** Parte imaginaria de los símbolos complejos
        - Estas señales se transmiten simultáneamente en el canal
        """)
        st.markdown("---")
    
    # 3. Distribución de LLRs
    if viz_options.get('llr_dist', True) and 'llr_dist' in viz:
        st.subheader("📊 Distribución de Log-Likelihood Ratios")
        st.pyplot(viz['llr_dist'])
        st.markdown("""
        **Interpretación:**
        - LLR > 0: Mayor probabilidad de que el bit sea 1
        - LLR < 0: Mayor probabilidad de que el bit sea 0
        - LLR ≈ 0: Decisión incierta (mayor riesgo de error)
        - Mayor separación de picos = mejor calidad de canal
        """)
        st.markdown("---")
    
    # 4. Resumen de Métricas
    if 'metrics' in viz:
        st.subheader("📈 Resumen Visual de Métricas")
        st.pyplot(viz['metrics'])
        st.markdown("""
        **Interpretación:**
        - **BER:** Debe ser lo más bajo posible (objetivo: < 10⁻³)
        - **Entropía:** Mide la aleatoriedad de la fuente
        - **Información Mutua:** Información efectivamente transmitida
        - **MSE:** Error de reconstrucción (más bajo = mejor)
        """)


def show_info_tab():
    """Muestra información del simulador"""
    
    st.header("ℹ️ Acerca del Simulador")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Características Principales")
        st.markdown("""
        - **Tecnologías:** 5G, 5G Advanced, 6G
        - **Tipos de Datos:** Texto, Audio, Imagen, Video
        - **Codificación de Canal:** LDPC, Polar
        - **Modulación:** QPSK, 16/64/256/1024-QAM
        - **Modelos de Canal:** AWGN, Rayleigh, Rician
        - **Modos:** SSCC (Separado), JSCC (Conjunto)
        - **Métricas:** BER, PSNR, SSIM, Entropía, Info. Mutua
        """)
        
        st.subheader("🔬 Pipeline de Procesamiento")
        st.markdown("""
        1. **Codificación de Fuente** (Compresión)
        2. **Codificación de Canal** (Protección de errores)
        3. **Modulación Digital** (Mapeo a símbolos)
        4. **Transmisión por Canal** (Con ruido/desvanecimiento)
        5. **Demodulación** (Recuperación de bits con LLRs)
        6. **Decodificación de Canal** (Corrección de errores)
        7. **Decodificación de Fuente** (Reconstrucción)
        """)
    
    with col2:
        st.subheader("📊 Visualizaciones Disponibles")
        st.markdown("""
        - **Diagrama de Constelación:** Símbolos modulados I/Q
        - **Formas de Onda:** Componentes In-Phase y Quadrature
        - **Distribución LLR:** Log-Likelihood Ratios del demodulador
        - **Resumen de Métricas:** Análisis visual completo
        """)
        
        st.subheader("💡 Casos de Uso")
        st.markdown("""
        1. **Investigación:** Análisis de sistemas de comunicación
        2. **Educación:** Aprendizaje de conceptos 5G/6G
        3. **Validación:** Prueba de algoritmos y parámetros
        4. **Comparación:** Evaluación de tecnologías
        5. **Optimización:** Ajuste de configuraciones
        """)
        
        st.subheader("📚 Documentación")
        st.markdown("""
        - `manual-user.md`: Manual de usuario
        - `manual-dev.md`: Manual de desarrollador
        - `QUICKSTART.md`: Guía de inicio rápido
        - `README.md`: Especificaciones técnicas
        """)
    
    # Arquitectura del sistema
    st.markdown("---")
    st.subheader("🏗️ Arquitectura del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Capa de Fuente**
        - Huffman
        - Aritmético
        - HEVC/VVC
        - EVS/IVAS
        """)
    
    with col2:
        st.markdown("""
        **Capa Física**
        - LDPC/Polar
        - QPSK/QAM
        - AWGN/Fading
        - Ecualización
        """)
    
    with col3:
        st.markdown("""
        **Capa de Análisis**
        - Métricas físicas
        - Teoría información
        - Calidad perceptual
        - Visualizaciones
        """)


def show_help_tab():
    """Muestra ayuda y guías"""
    
    st.header("❓ Ayuda y Guías")
    
    # Guía rápida
    st.subheader("🚀 Guía Rápida de Uso")
    
    with st.expander("1️⃣ Configurar Simulación", expanded=True):
        st.markdown("""
        **Pasos:**
        1. Selecciona la **Tecnología** (5G, 5G-Advanced, 6G)
        2. Elige el **Tipo de Datos** a transmitir
        3. Configura **Código de Canal** y **Modulación**
        4. Selecciona el **Modelo de Canal**
        5. Ajusta el **SNR** deseado
        6. Presiona **"Ejecutar Simulación"**
        
        **Tips:**
        - Comienza con configuraciones simples (QPSK, AWGN)
        - Aumenta complejidad gradualmente
        - Observa el efecto de cada parámetro
        """)
    
    with st.expander("2️⃣ Interpretar Resultados"):
        st.markdown("""
        **Métricas Clave:**
        
        - **BER (Bit Error Rate)**
          - < 10⁻⁶: Excelente 🟢
          - 10⁻⁶ a 10⁻³: Bueno 🟡
          - 10⁻³ a 10⁻¹: Aceptable 🟠
          - > 10⁻¹: Malo 🔴
        
        - **PSNR (dB)** - Para imagen/video
          - > 40: Excelente
          - 30-40: Bueno
          - 20-30: Aceptable
          - < 20: Malo
        
        - **Información Mutua**
          - Cercano a Entropía: Transmisión eficiente
          - Mucho menor: Pérdida de información
        """)
    
    with st.expander("3️⃣ Optimizar Rendimiento"):
        st.markdown("""
        **Para mejorar BER:**
        - Aumentar SNR
        - Usar modulación más robusta (QPSK vs QAM)
        - Usar código de canal más fuerte
        - Cambiar a canal AWGN si es posible
        
        **Para aumentar throughput:**
        - Usar QAM de orden superior (256-QAM, 1024-QAM)
        - Aumentar tasa de código
        - Operar con SNR alto
        
        **Trade-offs:**
        - Robustez ↔ Eficiencia Espectral
        - Latencia ↔ Corrección de Errores
        - Complejidad ↔ Rendimiento
        """)
    
    with st.expander("4️⃣ Troubleshooting"):
        st.markdown("""
        **Problemas Comunes:**
        
        **BER muy alto:**
        - SNR demasiado bajo
        - Modulación muy compleja para el SNR
        - Canal con desvanecimiento severo
        
        **Sin visualizaciones:**
        - Marca las opciones en el panel lateral
        - Ejecuta la simulación nuevamente
        
        **Error de simulación:**
        - Verifica configuración de parámetros
        - Revisa el traceback en la pestaña Results
        - Consulta la documentación
        """)
    
    # Glosario
    st.markdown("---")
    st.subheader("📖 Glosario de Términos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **BER:** Bit Error Rate (Tasa de error de bits)
        
        **SNR:** Signal-to-Noise Ratio (Relación señal-ruido)
        
        **LDPC:** Low-Density Parity-Check (código de canal)
        
        **Polar:** Código de canal óptimo teóricamente
        
        **QPSK:** Quadrature Phase-Shift Keying
        
        **QAM:** Quadrature Amplitude Modulation
        
        **AWGN:** Additive White Gaussian Noise
        """)
    
    with col2:
        st.markdown("""
        **LLR:** Log-Likelihood Ratio (razón de verosimilitud)
        
        **PSNR:** Peak Signal-to-Noise Ratio
        
        **SSIM:** Structural Similarity Index
        
        **SSCC:** Separate Source-Channel Coding
        
        **JSCC:** Joint Source-Channel Coding
        
        **HEVC:** High Efficiency Video Coding (H.265)
        
        **EVS:** Enhanced Voice Services
        """)
    
    # Contacto y recursos
    st.markdown("---")
    st.subheader("📚 Recursos Adicionales")
    
    st.info("""
    **Documentación Completa:**
    - `README.md`: Especificaciones técnicas detalladas
    - `manual-user.md`: Manual de usuario completo
    - `manual-dev.md`: Guía para desarrolladores
    - `job.md`: Estado del proyecto y roadmap
    
    **Ejemplos de Código:**
    - `main.py`: Ejemplos básicos
    - `examples_advanced.py`: Ejemplos avanzados
    - `example_jscc.py`: Comparación JSCC vs SSCC
    - `example_performance.py`: Optimización de rendimiento
    """)


if __name__ == "__main__":
    main()
