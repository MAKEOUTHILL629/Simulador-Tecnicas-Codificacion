#!/usr/bin/env python3
"""
Advanced examples using the communication simulator with real sample data.

This script demonstrates:
1. Image transmission with quality metrics (PSNR, SSIM)
2. Audio transmission with different modulation schemes
3. Video transmission optimization
4. Comparison of different technologies (5G vs 5G-A vs 6G)
"""

import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.simulator import CommunicationSimulator
from src.visualization.plots import plot_constellation, plot_ber_vs_snr, plot_quality_vs_snr


def example_image_transmission_quality():
    """
    Example 4: Image transmission with quality analysis.
    
    Demonstrates how image quality degrades with SNR and compares
    different channel coding schemes.
    """
    print("\n" + "="*70)
    print("EJEMPLO 4: Transmisión de Imagen con Análisis de Calidad")
    print("="*70)
    
    # Load sample image
    image_path = 'data/image/sample_image.npy'
    if not os.path.exists(image_path):
        print(f"⚠️  Imagen no encontrada: {image_path}")
        print("   Ejecuta: python generate_sample_data.py")
        return
    
    image = np.load(image_path)
    print(f"\n📷 Imagen cargada: {image.shape} píxeles")
    
    # Convert image to bits
    image_bits = np.unpackbits(image.flatten())
    print(f"   Bits totales: {len(image_bits)}")
    
    # Test different SNR values
    snr_values = [5, 10, 15, 20, 25]
    channel_codes = ['LDPC', 'Polar']
    
    results = {code: {'snr': [], 'psnr': [], 'ssim': [], 'ber': []} 
               for code in channel_codes}
    
    print(f"\n🔬 Probando {len(channel_codes)} códigos de canal en {len(snr_values)} niveles de SNR...")
    
    for channel_code in channel_codes:
        print(f"\n  📡 Código de canal: {channel_code}")
        
        for snr_db in snr_values:
            config = {
                'technology': '5G_Advanced',
                'data_type': 'image',
                'channel_code': channel_code,
                'code_rate': 0.5,
                'modulation': '16QAM',
                'channel_model': 'AWGN',
                'snr_db': snr_db
            }
            
            sim = CommunicationSimulator(config)
            result = sim.run_simulation(image_bits)
            
            # Reconstruct image
            decoded_bits = result['decoded_bits'][:len(image_bits)]
            decoded_image = np.packbits(decoded_bits).reshape(image.shape)
            
            # Calculate metrics
            psnr = result['metrics']['psnr']
            ssim = result['metrics']['ssim']
            ber = result['metrics']['ber']
            
            results[channel_code]['snr'].append(snr_db)
            results[channel_code]['psnr'].append(psnr)
            results[channel_code]['ssim'].append(ssim)
            results[channel_code]['ber'].append(ber)
            
            print(f"     SNR={snr_db:2d}dB: PSNR={psnr:5.2f}dB, SSIM={ssim:.4f}, BER={ber:.6f}")
    
    # Plot quality vs SNR
    print(f"\n📊 Generando gráfica de calidad vs SNR...")
    plot_quality_vs_snr(results, 
                       title='Calidad de Imagen vs SNR (LDPC vs Polar)',
                       filename='plots/example4_image_quality.png')
    print(f"   ✓ Guardado: plots/example4_image_quality.png")
    
    print(f"\n✅ Ejemplo 4 completado")


def example_audio_transmission():
    """
    Example 5: Audio transmission with different modulation schemes.
    
    Compares QPSK vs 64-QAM for audio transmission.
    """
    print("\n" + "="*70)
    print("EJEMPLO 5: Transmisión de Audio con Diferentes Modulaciones")
    print("="*70)
    
    # Load sample audio
    audio_path = 'data/audio/sample_audio.npy'
    if not os.path.exists(audio_path):
        print(f"⚠️  Audio no encontrado: {audio_path}")
        print("   Ejecuta: python generate_sample_data.py")
        return
    
    audio = np.load(audio_path)
    print(f"\n🎵 Audio cargado: {len(audio)} muestras")
    
    # Convert audio to bits (use first 1000 samples for speed)
    audio_subset = audio[:1000]
    audio_bytes = audio_subset.tobytes()
    audio_bits = np.unpackbits(np.frombuffer(audio_bytes, dtype=np.uint8))
    print(f"   Bits totales: {len(audio_bits)}")
    
    # Test different modulations
    modulations = ['QPSK', '16QAM', '64QAM']
    snr_db = 15
    
    print(f"\n🔬 Probando {len(modulations)} esquemas de modulación (SNR={snr_db}dB)...")
    
    results = []
    for modulation in modulations:
        config = {
            'technology': '5G',
            'data_type': 'audio',
            'channel_code': 'Polar',
            'code_rate': 0.667,
            'modulation': modulation,
            'channel_model': 'AWGN',
            'snr_db': snr_db
        }
        
        sim = CommunicationSimulator(config)
        result = sim.run_simulation(audio_bits)
        
        ber = result['metrics']['ber']
        snr = result['metrics']['snr']
        
        print(f"  📡 {modulation:6s}: BER={ber:.6f}, SNR={snr:.2f}dB")
        results.append({
            'modulation': modulation,
            'ber': ber,
            'snr': snr
        })
    
    print(f"\n✅ Ejemplo 5 completado")
    print(f"   Conclusión: QPSK ofrece mejor robustez, 64-QAM mayor eficiencia espectral")


def example_video_transmission():
    """
    Example 6: Video transmission with frame-by-frame analysis.
    
    Transmits video frames and analyzes quality per frame.
    """
    print("\n" + "="*70)
    print("EJEMPLO 6: Transmisión de Video Frame-by-Frame")
    print("="*70)
    
    # Load sample video
    video_path = 'data/video/sample_video.npy'
    if not os.path.exists(video_path):
        print(f"⚠️  Video no encontrado: {video_path}")
        print("   Ejecuta: python generate_sample_data.py")
        return
    
    video = np.load(video_path)
    num_frames, height, width = video.shape
    print(f"\n🎬 Video cargado: {num_frames} frames de {height}x{width} píxeles")
    
    # Transmit a subset of frames
    frames_to_transmit = min(5, num_frames)
    snr_db = 20
    
    print(f"\n🔬 Transmitiendo {frames_to_transmit} frames (SNR={snr_db}dB)...")
    
    config = {
        'technology': '6G',
        'data_type': 'video',
        'channel_code': 'Polar',
        'code_rate': 0.75,
        'modulation': '256QAM',
        'channel_model': 'AWGN',
        'snr_db': snr_db
    }
    
    frame_metrics = []
    
    for frame_idx in range(frames_to_transmit):
        frame = video[frame_idx]
        frame_bits = np.unpackbits(frame.flatten())
        
        sim = CommunicationSimulator(config)
        result = sim.run_simulation(frame_bits)
        
        # Reconstruct frame
        decoded_bits = result['decoded_bits'][:len(frame_bits)]
        decoded_frame = np.packbits(decoded_bits).reshape(frame.shape)
        
        psnr = result['metrics']['psnr']
        ssim = result['metrics']['ssim']
        ber = result['metrics']['ber']
        
        frame_metrics.append({
            'frame': frame_idx + 1,
            'psnr': psnr,
            'ssim': ssim,
            'ber': ber
        })
        
        print(f"  Frame {frame_idx+1}/{frames_to_transmit}: "
              f"PSNR={psnr:5.2f}dB, SSIM={ssim:.4f}, BER={ber:.6f}")
    
    # Calculate average metrics
    avg_psnr = np.mean([m['psnr'] for m in frame_metrics])
    avg_ssim = np.mean([m['ssim'] for m in frame_metrics])
    avg_ber = np.mean([m['ber'] for m in frame_metrics])
    
    print(f"\n📊 Métricas promedio:")
    print(f"   PSNR: {avg_psnr:.2f}dB")
    print(f"   SSIM: {avg_ssim:.4f}")
    print(f"   BER:  {avg_ber:.6f}")
    
    print(f"\n✅ Ejemplo 6 completado")


def example_technology_comparison():
    """
    Example 7: Compare 5G, 5G-Advanced, and 6G performance.
    
    Shows how different technologies perform under same conditions.
    """
    print("\n" + "="*70)
    print("EJEMPLO 7: Comparación de Tecnologías (5G vs 5G-A vs 6G)")
    print("="*70)
    
    # Generate test data
    test_bits = np.random.randint(0, 2, 1000)
    print(f"\n📡 Datos de prueba: {len(test_bits)} bits")
    
    technologies = {
        '5G': {
            'modulation': 'QPSK',
            'code_rate': 0.5
        },
        '5G_Advanced': {
            'modulation': '64QAM',
            'code_rate': 0.667
        },
        '6G': {
            'modulation': '1024QAM',
            'code_rate': 0.833
        }
    }
    
    snr_db = 20
    
    print(f"\n🔬 Comparando tecnologías (SNR={snr_db}dB)...")
    
    results = []
    for tech_name, tech_params in technologies.items():
        config = {
            'technology': tech_name,
            'data_type': 'text',
            'channel_code': 'Polar',
            'code_rate': tech_params['code_rate'],
            'modulation': tech_params['modulation'],
            'channel_model': 'AWGN',
            'snr_db': snr_db
        }
        
        sim = CommunicationSimulator(config)
        result = sim.run_simulation(test_bits)
        
        ber = result['metrics']['ber']
        spectral_efficiency = np.log2(int(tech_params['modulation'].replace('QPSK', '4').replace('QAM', '')))
        
        # Calculate approximate throughput
        code_rate = tech_params['code_rate']
        throughput = spectral_efficiency * code_rate
        
        print(f"\n  📡 {tech_name:15s}:")
        print(f"     Modulación: {tech_params['modulation']:8s}")
        print(f"     Tasa código: {code_rate:.3f}")
        print(f"     BER: {ber:.6f}")
        print(f"     Eficiencia espectral: {spectral_efficiency:.2f} bits/símbolo")
        print(f"     Throughput relativo: {throughput:.2f}")
        
        results.append({
            'technology': tech_name,
            'ber': ber,
            'throughput': throughput
        })
    
    print(f"\n📊 Resumen:")
    print(f"   5G:          Más robusto, menor throughput")
    print(f"   5G-Advanced: Balance robustez/throughput")
    print(f"   6G:          Mayor throughput, requiere mejor SNR")
    
    print(f"\n✅ Ejemplo 7 completado")


def main():
    """Run all advanced examples."""
    print("\n" + "🚀"*35)
    print("   EJEMPLOS AVANZADOS - Simulador de Comunicaciones 5G/6G")
    print("🚀"*35)
    
    # Check if sample data exists
    if not os.path.exists('data/image/sample_image.npy'):
        print("\n⚠️  ADVERTENCIA: Datos de ejemplo no encontrados")
        print("   Ejecutando script de generación de datos...")
        os.system('python generate_sample_data.py')
        print()
    
    # Create plots directory
    os.makedirs('plots', exist_ok=True)
    
    # Run examples
    try:
        example_image_transmission_quality()
        example_audio_transmission()
        example_video_transmission()
        example_technology_comparison()
        
        print("\n" + "="*70)
        print("✅ TODOS LOS EJEMPLOS AVANZADOS COMPLETADOS")
        print("="*70)
        print("\nGráficas generadas en: ./plots/")
        print("Para más información, consulta:")
        print("  - manual-user.md  (Guía de uso)")
        print("  - manual-dev.md   (Documentación técnica)")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Ejecución interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
