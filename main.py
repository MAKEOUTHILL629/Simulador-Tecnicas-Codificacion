#!/usr/bin/env python3
"""
Script principal para ejecutar el simulador.
Ejemplo de uso con diferentes configuraciones.
"""

import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.simulator import CommunicationSimulator, create_default_config
from src.source_coding.encoders import create_source_encoder
from src.channel_coding.codes import create_channel_encoder, LDPCDecoder, PolarDecoder
from src.modulation.modulators import create_modulator
from src.channel.models import create_channel
from src.metrics.performance import MetricsCalculator
from src.visualization.plots import SimulatorVisualizer


def example_text_simulation():
    """
    Ejemplo 1: Simulación con datos de texto.
    """
    print("\n" + "="*70)
    print("EJEMPLO 1: SIMULACIÓN DE TRANSMISIÓN DE TEXTO")
    print("="*70)
    
    # Configuración
    config = {
        'technology': '5G',
        'data_type': 'text',
        'channel_code': 'Polar',
        'modulation': 'QPSK',
        'channel_model': 'AWGN',
        'snr_db': 10.0,
        'mode': 'SSCC'
    }
    
    # Datos de prueba: mensaje de texto convertido a bits
    message = "HELLO WORLD"
    text_bits = np.unpackbits(np.array([ord(c) for c in message], dtype=np.uint8))
    
    print(f"\nMensaje original: {message}")
    print(f"Longitud en bits: {len(text_bits)}")
    print(f"Configuración: {config}")
    
    # Crear componentes del sistema
    source_encoder = create_source_encoder(config['data_type'], config['technology'])
    channel_encoder = create_channel_encoder(config['channel_code'], code_rate=0.5)
    modulator = create_modulator(config['modulation'])
    channel = create_channel(config['channel_model'], config['snr_db'])
    
    # Pipeline de transmisión
    print("\n--- Pipeline de Transmisión ---")
    
    # 1. Codificación de fuente (compresión)
    print("1. Codificando fuente...")
    compressed, metadata = source_encoder.encode(text_bits)
    print(f"   Tasa de compresión: {source_encoder.get_compression_ratio():.3f}")
    
    # 2. Codificación de canal
    print("2. Codificando canal...")
    encoded = channel_encoder.encode(compressed)
    print(f"   Tasa de código: {channel_encoder.get_code_rate():.3f}")
    print(f"   Bits codificados: {len(encoded)}")
    
    # 3. Modulación
    print("3. Modulando...")
    symbols = modulator.modulate(encoded)
    print(f"   Número de símbolos: {len(symbols)}")
    
    # 4. Transmisión por canal
    print("4. Transmitiendo por canal...")
    received = channel.transmit(symbols)
    
    # 5. Demodulación
    print("5. Demodulando...")
    llrs = modulator.demodulate(received, noise_var=channel.get_noise_variance())
    
    # 6. Decodificación de canal
    print("6. Decodificando canal...")
    if config['channel_code'] == 'Polar':
        decoder = PolarDecoder(channel_encoder)
    else:
        decoder = LDPCDecoder(channel_encoder)
    
    decoded = decoder.decode(llrs)
    
    # Recortar al tamaño original
    decoded = decoded[:len(compressed)]
    
    # 7. Calcular métricas
    print("\n--- Métricas de Rendimiento ---")
    calc = MetricsCalculator()
    metrics = calc.calculate_all_metrics(
        compressed, decoded,
        original_bits=compressed,
        received_bits=decoded,
        data_type='text'
    )
    
    print(f"BER: {metrics.get('ber', 0):.6f}")
    print(f"Entropía: {metrics.get('entropy', 0):.4f} bits/símbolo")
    
    # 8. Visualización
    print("\n--- Generando visualizaciones ---")
    viz = SimulatorVisualizer(output_dir='./plots')
    viz.plot_constellation(received, "Constelación Recibida - QPSK", "example1_constellation.png")
    viz.plot_waveform(symbols[:100], title="Forma de Onda Modulada", filename="example1_waveform.png")
    print("Gráficas guardadas en ./plots/")
    
    print("\n✓ Simulación completada exitosamente\n")


def example_comparison_snr():
    """
    Ejemplo 2: Comparación de BER vs SNR para diferentes modulaciones.
    """
    print("\n" + "="*70)
    print("EJEMPLO 2: COMPARACIÓN BER vs SNR")
    print("="*70)
    
    # Parámetros
    snr_range = np.arange(0, 15, 2)  # SNR de 0 a 14 dB
    modulations = ['QPSK', '16QAM', '64QAM']
    
    # Generar datos de prueba
    n_bits = 10000
    test_bits = np.random.randint(0, 2, n_bits)
    
    # Almacenar resultados
    results = {}
    
    for mod_scheme in modulations:
        print(f"\nProbando {mod_scheme}...")
        ber_values = []
        
        for snr in snr_range:
            # Configurar sistema
            modulator = create_modulator(mod_scheme)
            channel = create_channel('AWGN', snr)
            
            # Transmitir
            symbols = modulator.modulate(test_bits)
            received = channel.transmit(symbols)
            llrs = modulator.demodulate(received, noise_var=channel.get_noise_variance())
            
            # Decisión hard
            decoded_bits = (llrs < 0).astype(np.uint8)
            decoded_bits = decoded_bits[:len(test_bits)]
            
            # Calcular BER
            errors = np.sum(test_bits != decoded_bits)
            ber = errors / len(test_bits)
            ber_values.append(ber)
            
            print(f"  SNR={snr} dB: BER={ber:.6f}")
        
        results[mod_scheme] = (snr_range, np.array(ber_values))
    
    # Visualizar resultados
    print("\n--- Generando gráfica comparativa ---")
    viz = SimulatorVisualizer(output_dir='./plots')
    viz.plot_ber_vs_ebn0(results, filename="example2_ber_comparison.png")
    print("Gráfica guardada en ./plots/example2_ber_comparison.png")
    
    print("\n✓ Simulación completada exitosamente\n")


def example_image_transmission():
    """
    Ejemplo 3: Simulación de transmisión de imagen.
    """
    print("\n" + "="*70)
    print("EJEMPLO 3: SIMULACIÓN DE TRANSMISIÓN DE IMAGEN")
    print("="*70)
    
    # Generar imagen de prueba (patrón simple)
    image_size = (64, 64)
    test_image = np.random.randint(0, 256, image_size, dtype=np.uint8)
    
    print(f"\nTamaño de imagen: {image_size}")
    print(f"Total de píxeles: {test_image.size}")
    
    # Configuración para video/imagen
    config = {
        'technology': '5G_Advanced',
        'data_type': 'image',
        'channel_code': 'LDPC',
        'modulation': '64QAM',
        'channel_model': 'AWGN',
        'snr_db': 15.0,
        'mode': 'SSCC'
    }
    
    print(f"Configuración: {config}")
    
    # Crear componentes
    source_encoder = create_source_encoder(config['data_type'], config['technology'])
    
    # Codificar imagen
    print("\n--- Procesando imagen ---")
    print("1. Codificando fuente (compresión)...")
    compressed, metadata = source_encoder.encode(test_image.flatten())
    print(f"   Códec: {metadata.get('codec', 'N/A')}")
    print(f"   Tasa de compresión: {source_encoder.get_compression_ratio():.3f}")
    
    # Simular transmisión (simplificado)
    print("2. Simulando transmisión...")
    # En una versión completa, pasaría por todo el pipeline
    
    # Reconstrucción (simulada)
    reconstructed = np.resize(compressed, test_image.size).reshape(image_size)
    
    # Calcular métricas de calidad
    print("\n--- Métricas de Calidad ---")
    calc = MetricsCalculator()
    metrics = calc.calculate_all_metrics(
        test_image,
        reconstructed,
        data_type='image'
    )
    
    print(f"PSNR: {metrics.get('psnr', 0):.2f} dB")
    print(f"SSIM: {metrics.get('ssim', 0):.4f}")
    print(f"MSE: {metrics.get('mse', 0):.2f}")
    
    print("\n✓ Simulación completada exitosamente\n")


def main():
    """
    Función principal que ejecuta los ejemplos.
    """
    print("\n" + "="*70)
    print("SIMULADOR DE SISTEMAS DE COMUNICACIÓN 5G/6G")
    print("="*70)
    print("\nEste simulador implementa:")
    print("  • Codificación de fuente (HEVC, VVC, EVS, IVAS, Huffman)")
    print("  • Codificación de canal (LDPC, Polar)")
    print("  • Modulación digital (QPSK, 16/64/256/1024-QAM)")
    print("  • Modelos de canal (AWGN, Rayleigh, Rician)")
    print("  • Métricas de rendimiento (BER, PSNR, SSIM, entropía, etc.)")
    print("  • Visualizaciones comparativas")
    
    # Crear directorio de salida
    os.makedirs('./plots', exist_ok=True)
    
    # Ejecutar ejemplos
    try:
        example_text_simulation()
        example_comparison_snr()
        example_image_transmission()
        
        print("\n" + "="*70)
        print("TODOS LOS EJEMPLOS COMPLETADOS")
        print("="*70)
        print("\nRevisa el directorio './plots' para ver las visualizaciones generadas.")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error durante la simulación: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
