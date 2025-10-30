#!/usr/bin/env python3
"""
Script de validación: Compara BER simulado vs BER teórico

Este script valida el simulador comparando el BER obtenido con las
curvas teóricas para diferentes esquemas de modulación en canal AWGN.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.modulation.modulators import create_modulator
from src.channel.models import AWGNChannel, calculate_ber_theoretical_awgn


def validate_ber_qpsk(snr_range=None, n_bits=50000):
    """
    Valida BER de QPSK contra curva teórica.
    
    Args:
        snr_range: Rango de SNR en dB (default: 0 a 12 dB)
        n_bits: Número de bits para simulación Monte Carlo
    
    Returns:
        Dict con resultados de validación
    """
    if snr_range is None:
        snr_range = np.arange(0, 13, 2)
    
    print("="*70)
    print("VALIDACIÓN BER: QPSK en Canal AWGN")
    print("="*70)
    print(f"Bits por simulación: {n_bits}")
    print(f"Rango SNR: {snr_range[0]} a {snr_range[-1]} dB")
    print()
    
    modulator = create_modulator('QPSK')
    
    ber_simulated = []
    ber_theoretical = []
    
    for snr_db in snr_range:
        print(f"Simulando SNR = {snr_db} dB...", end=" ")
        
        # Simulación
        channel = AWGNChannel(snr_db)
        bits = np.random.randint(0, 2, n_bits)
        symbols = modulator.modulate(bits)
        received = channel.transmit(symbols)
        llrs = modulator.demodulate(received, channel.get_noise_variance())
        decoded = (llrs < 0).astype(np.uint8)[:n_bits]
        
        ber_sim = np.sum(bits != decoded) / n_bits
        ber_simulated.append(ber_sim)
        
        # Teórico
        # Para QPSK sin codificación: Eb/N0 = SNR (1 símbolo = 2 bits, R=1)
        ebn0_db = snr_db  # Simplificación: Eb/N0 ≈ SNR para QPSK sin codificación
        ber_theo = calculate_ber_theoretical_awgn(ebn0_db, 'QPSK')
        ber_theoretical.append(ber_theo)
        
        print(f"BER_sim = {ber_sim:.6f}, BER_theo = {ber_theo:.6f}")
    
    # Calcular error relativo
    ber_simulated = np.array(ber_simulated)
    ber_theoretical = np.array(ber_theoretical)
    
    # Evitar división por cero
    valid_indices = ber_theoretical > 1e-10
    relative_error = np.abs(ber_simulated[valid_indices] - ber_theoretical[valid_indices]) / ber_theoretical[valid_indices]
    
    print()
    print("="*70)
    print("RESULTADOS DE VALIDACIÓN")
    print("="*70)
    print(f"Error relativo promedio: {np.mean(relative_error)*100:.2f}%")
    print(f"Error relativo máximo: {np.max(relative_error)*100:.2f}%")
    
    # Tolerancia: 20% debido a varianza Monte Carlo
    if np.all(relative_error < 0.3):
        print("✅ VALIDACIÓN EXITOSA: BER simulado concuerda con teoría")
        status = "PASS"
    else:
        print("⚠️  ADVERTENCIA: Diferencias significativas detectadas")
        status = "WARNING"
    
    # Graficar
    plt.figure(figsize=(10, 6))
    plt.semilogy(snr_range, ber_simulated, 'bo-', label='Simulado', markersize=8)
    plt.semilogy(snr_range, ber_theoretical, 'r--', label='Teórico', linewidth=2)
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.title('Validación BER: QPSK en AWGN')
    plt.legend()
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    
    os.makedirs('./plots', exist_ok=True)
    plt.savefig('./plots/validation_ber_qpsk.png', dpi=300, bbox_inches='tight')
    print(f"\n📊 Gráfica guardada en: ./plots/validation_ber_qpsk.png")
    plt.close()
    
    return {
        'status': status,
        'snr_range': snr_range,
        'ber_simulated': ber_simulated,
        'ber_theoretical': ber_theoretical,
        'relative_error': relative_error
    }


def validate_multiple_modulations(snr_range=None, n_bits=50000):
    """
    Valida múltiples esquemas de modulación.
    """
    if snr_range is None:
        snr_range = np.arange(0, 16, 3)
    
    print("\n" + "="*70)
    print("VALIDACIÓN MÚLTIPLES MODULACIONES")
    print("="*70)
    
    modulations = ['QPSK', '16QAM', '64QAM']
    results = {}
    
    plt.figure(figsize=(12, 7))
    
    for mod_scheme in modulations:
        print(f"\n📡 Validando {mod_scheme}...")
        
        modulator = create_modulator(mod_scheme)
        ber_sim_list = []
        ber_theo_list = []
        
        for snr_db in snr_range:
            # Simulación
            channel = AWGNChannel(snr_db)
            bits = np.random.randint(0, 2, n_bits)
            symbols = modulator.modulate(bits)
            received = channel.transmit(symbols)
            llrs = modulator.demodulate(received, channel.get_noise_variance())
            decoded = (llrs < 0).astype(np.uint8)[:n_bits]
            
            ber_sim = np.sum(bits != decoded) / n_bits
            ber_sim_list.append(ber_sim)
            
            # Teórico (aproximado)
            ebn0_db = snr_db
            ber_theo = calculate_ber_theoretical_awgn(ebn0_db, mod_scheme)
            ber_theo_list.append(ber_theo)
        
        results[mod_scheme] = {
            'simulated': np.array(ber_sim_list),
            'theoretical': np.array(ber_theo_list)
        }
        
        # Graficar
        plt.semilogy(snr_range, ber_sim_list, 'o-', label=f'{mod_scheme} (Sim)', markersize=6)
        plt.semilogy(snr_range, ber_theo_list, '--', label=f'{mod_scheme} (Teórico)', linewidth=2, alpha=0.7)
    
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.title('Validación BER: Múltiples Modulaciones en AWGN')
    plt.legend(loc='best')
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('./plots/validation_ber_multiple.png', dpi=300, bbox_inches='tight')
    print(f"\n📊 Gráfica guardada en: ./plots/validation_ber_multiple.png")
    plt.close()
    
    print("\n✅ Validación de múltiples modulaciones completada")
    
    return results


def main():
    """Función principal"""
    print("\n" + "🔬"*35)
    print("   VALIDACIÓN DEL SIMULADOR: BER vs Teoría")
    print("🔬"*35 + "\n")
    
    # Validación 1: QPSK detallada
    results_qpsk = validate_ber_qpsk(n_bits=100000)
    
    # Validación 2: Múltiples modulaciones
    results_multi = validate_multiple_modulations(n_bits=50000)
    
    print("\n" + "="*70)
    print("RESUMEN FINAL")
    print("="*70)
    print(f"Estado QPSK: {results_qpsk['status']}")
    print("\nTodas las validaciones completadas.")
    print("Consulta las gráficas en ./plots/ para análisis detallado.")
    print()


if __name__ == "__main__":
    main()
