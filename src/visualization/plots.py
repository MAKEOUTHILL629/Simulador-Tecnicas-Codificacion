"""
Módulo de visualización.
Genera gráficas comparativas y diagramas.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple, Any
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para servidores


class SimulatorVisualizer:
    """
    Clase para generar visualizaciones del simulador.
    """
    
    def __init__(self, output_dir: str = './plots'):
        """
        Args:
            output_dir: Directorio para guardar las gráficas
        """
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_constellation(
        self,
        symbols: np.ndarray,
        title: str = "Diagrama de Constelación",
        filename: Optional[str] = None
    ):
        """
        Dibuja diagrama de constelación.
        
        Args:
            symbols: Símbolos complejos
            title: Título del gráfico
            filename: Nombre del archivo (opcional)
        """
        plt.figure(figsize=(8, 8))
        plt.scatter(symbols.real, symbols.imag, alpha=0.5, s=10)
        plt.xlabel('In-Phase (I)')
        plt.ylabel('Quadrature (Q)')
        plt.title(title)
        plt.grid(True)
        plt.axis('equal')
        
        if filename:
            plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        else:
            plt.savefig(f"{self.output_dir}/constellation.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_ber_vs_ebn0(
        self,
        results: Dict[str, Tuple[np.ndarray, np.ndarray]],
        filename: str = "ber_vs_ebn0.png"
    ):
        """
        Dibuja curvas BER vs Eb/N0 para diferentes esquemas.
        
        Args:
            results: Dict con {nombre: (ebn0_values, ber_values)}
            filename: Nombre del archivo
        """
        plt.figure(figsize=(10, 6))
        
        for label, (ebn0, ber) in results.items():
            plt.semilogy(ebn0, ber, marker='o', label=label)
        
        plt.xlabel('Eb/N0 (dB)')
        plt.ylabel('Bit Error Rate (BER)')
        plt.title('BER vs Eb/N0')
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.6)
        
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_quality_vs_snr(
        self,
        results: Dict[str, Tuple[np.ndarray, np.ndarray]],
        metric: str = 'PSNR',
        filename: str = "quality_vs_snr.png"
    ):
        """
        Dibuja curvas de calidad (PSNR/SSIM) vs SNR.
        Muestra el efecto acantilado de SSCC vs degradación gradual de JSCC.
        
        Args:
            results: Dict con {nombre: (snr_values, quality_values)}
            metric: Métrica de calidad ('PSNR', 'SSIM', 'PESQ')
            filename: Nombre del archivo
        """
        plt.figure(figsize=(10, 6))
        
        for label, (snr, quality) in results.items():
            linestyle = '--' if 'SSCC' in label else '-'
            plt.plot(snr, quality, marker='o', linestyle=linestyle, label=label)
        
        plt.xlabel('Channel SNR (dB)')
        plt.ylabel(f'{metric}')
        plt.title(f'{metric} vs Channel SNR: SSCC Cliff Effect vs JSCC Graceful Degradation')
        plt.legend()
        plt.grid(True, alpha=0.6)
        
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_rate_distortion(
        self,
        results: Dict[str, Tuple[np.ndarray, np.ndarray]],
        filename: str = "rate_distortion.png"
    ):
        """
        Dibuja curvas tasa-distorsión para diferentes códecs.
        
        Args:
            results: Dict con {codec_name: (bitrate, distortion)}
            filename: Nombre del archivo
        """
        plt.figure(figsize=(10, 6))
        
        for codec, (rate, distortion) in results.items():
            plt.plot(rate, distortion, marker='s', label=codec)
        
        plt.xlabel('Bitrate (kbps)')
        plt.ylabel('Distortion (MSE or -PSNR)')
        plt.title('Rate-Distortion Curves')
        plt.legend()
        plt.grid(True, alpha=0.6)
        
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_mutual_information_vs_snr(
        self,
        results: Dict[str, Tuple[np.ndarray, np.ndarray]],
        filename: str = "mutual_info_vs_snr.png"
    ):
        """
        Dibuja información mutua vs SNR del canal.
        
        Args:
            results: Dict con {nombre: (snr_values, mi_values)}
            filename: Nombre del archivo
        """
        plt.figure(figsize=(10, 6))
        
        for label, (snr, mi) in results.items():
            plt.plot(snr, mi, marker='o', label=label)
        
        plt.xlabel('Channel SNR (dB)')
        plt.ylabel('Mutual Information (bits)')
        plt.title('Mutual Information vs Channel SNR')
        plt.legend()
        plt.grid(True, alpha=0.6)
        
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_llr_distribution(
        self,
        llrs: np.ndarray,
        title: str = "Distribución de LLRs",
        filename: str = "llr_distribution.png"
    ):
        """
        Dibuja distribución de LLRs.
        
        Args:
            llrs: Valores de LLR
            title: Título del gráfico
            filename: Nombre del archivo
        """
        plt.figure(figsize=(10, 6))
        plt.hist(llrs, bins=50, density=True, alpha=0.7, edgecolor='black')
        plt.xlabel('LLR Value')
        plt.ylabel('Probability Density')
        plt.title(title)
        plt.grid(True, alpha=0.6)
        
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_waveform(
        self,
        signal: np.ndarray,
        sample_rate: int = 1,
        title: str = "Forma de Onda",
        filename: str = "waveform.png"
    ):
        """
        Dibuja forma de onda en el dominio del tiempo.
        
        Args:
            signal: Señal (puede ser compleja)
            sample_rate: Tasa de muestreo
            title: Título del gráfico
            filename: Nombre del archivo
        """
        t = np.arange(len(signal)) / sample_rate
        
        plt.figure(figsize=(12, 6))
        
        if np.iscomplexobj(signal):
            plt.subplot(2, 1, 1)
            plt.plot(t, signal.real)
            plt.ylabel('I (In-Phase)')
            plt.title(f'{title} - Componente I')
            plt.grid(True, alpha=0.6)
            
            plt.subplot(2, 1, 2)
            plt.plot(t, signal.imag)
            plt.xlabel('Time')
            plt.ylabel('Q (Quadrature)')
            plt.title(f'{title} - Componente Q')
            plt.grid(True, alpha=0.6)
        else:
            plt.plot(t, signal)
            plt.xlabel('Time')
            plt.ylabel('Amplitude')
            plt.title(title)
            plt.grid(True, alpha=0.6)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_spectrogram(
        self,
        signal: np.ndarray,
        sample_rate: int = 16000,
        title: str = "Espectrograma",
        filename: str = "spectrogram.png"
    ):
        """
        Dibuja espectrograma de una señal de audio.
        
        Args:
            signal: Señal de audio
            sample_rate: Tasa de muestreo
            title: Título del gráfico
            filename: Nombre del archivo
        """
        plt.figure(figsize=(12, 6))
        plt.specgram(signal, Fs=sample_rate, cmap='viridis')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title(title)
        plt.colorbar(label='Intensity (dB)')
        
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_comparison_bars(
        self,
        metrics: Dict[str, Dict[str, float]],
        metric_name: str = 'BER',
        filename: str = "comparison_bars.png"
    ):
        """
        Dibuja gráfico de barras comparativo.
        
        Args:
            metrics: Dict con {scheme_name: {metric: value}}
            metric_name: Nombre de la métrica a comparar
            filename: Nombre del archivo
        """
        schemes = list(metrics.keys())
        values = [metrics[s].get(metric_name, 0) for s in schemes]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(schemes, values, color='steelblue', edgecolor='black')
        
        # Colorear barras según el valor
        for i, bar in enumerate(bars):
            if values[i] < np.mean(values):
                bar.set_color('green')
            else:
                bar.set_color('red')
        
        plt.xlabel('Scheme')
        plt.ylabel(metric_name)
        plt.title(f'Comparison of {metric_name} across Different Schemes')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, axis='y', alpha=0.6)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_summary_figure(
        self,
        results: Dict[str, Any],
        filename: str = "summary.png"
    ):
        """
        Crea figura con múltiples subplots mostrando resumen completo.
        
        Args:
            results: Diccionario con todos los resultados
            filename: Nombre del archivo
        """
        fig = plt.figure(figsize=(16, 12))
        
        # Subplot 1: Constelación
        if 'constellation' in results:
            ax1 = plt.subplot(2, 3, 1)
            symbols = results['constellation']
            ax1.scatter(symbols.real, symbols.imag, alpha=0.5, s=5)
            ax1.set_xlabel('I')
            ax1.set_ylabel('Q')
            ax1.set_title('Constellation Diagram')
            ax1.grid(True)
            ax1.axis('equal')
        
        # Subplot 2: BER vs Eb/N0
        if 'ber_curves' in results:
            ax2 = plt.subplot(2, 3, 2)
            for label, (ebn0, ber) in results['ber_curves'].items():
                ax2.semilogy(ebn0, ber, marker='o', label=label)
            ax2.set_xlabel('Eb/N0 (dB)')
            ax2.set_ylabel('BER')
            ax2.set_title('BER Performance')
            ax2.legend()
            ax2.grid(True)
        
        # Subplot 3: Métricas de calidad
        if 'quality_metrics' in results:
            ax3 = plt.subplot(2, 3, 3)
            metrics = results['quality_metrics']
            metric_names = list(metrics.keys())
            metric_values = list(metrics.values())
            ax3.bar(metric_names, metric_values, color='steelblue')
            ax3.set_ylabel('Value')
            ax3.set_title('Quality Metrics')
            ax3.tick_params(axis='x', rotation=45)
            ax3.grid(True, axis='y')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        plt.close()
