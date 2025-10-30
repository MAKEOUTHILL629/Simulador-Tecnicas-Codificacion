"""
Módulo de métricas de rendimiento.
Implementa cálculos de entropía, información mutua, BER, PSNR, SSIM, etc.
"""

import numpy as np
from typing import Dict, Any, Optional
from scipy.stats import entropy as scipy_entropy


def calculate_entropy(data: np.ndarray) -> float:
    """
    Calcula la entropía de Shannon H(X) = -Σ p(x) log₂(p(x)).
    
    Args:
        data: Array de símbolos
    
    Returns:
        Entropía en bits/símbolo
    """
    # Calcular probabilidades de cada símbolo
    symbols, counts = np.unique(data, return_counts=True)
    probabilities = counts / len(data)
    
    # Calcular entropía (base 2 para bits)
    H = -np.sum(probabilities * np.log2(probabilities + 1e-10))
    
    return H


def calculate_mutual_information(
    original: np.ndarray,
    reconstructed: np.ndarray
) -> float:
    """
    Calcula la información mutua I(X;Y) = H(X) - H(X|Y).
    
    Args:
        original: Datos originales
        reconstructed: Datos reconstruidos
    
    Returns:
        Información mutua en bits
    """
    # Entropía de la fuente
    H_X = calculate_entropy(original)
    
    # Para calcular H(X|Y), necesitamos la distribución conjunta
    # Simplificación: usar entropía condicional aproximada
    
    # Discretizar si es necesario
    if original.dtype == np.float64 or reconstructed.dtype == np.float64:
        original_discrete = (original * 255).astype(np.uint8)
        reconstructed_discrete = (reconstructed * 255).astype(np.uint8)
    else:
        original_discrete = original
        reconstructed_discrete = reconstructed
    
    # Calcular H(X,Y)
    joint = np.column_stack([original_discrete.flatten(), reconstructed_discrete.flatten()])
    
    # Convertir pares a índices únicos
    _, inverse = np.unique(joint, axis=0, return_inverse=True)
    H_XY = calculate_entropy(inverse)
    
    # H(Y)
    H_Y = calculate_entropy(reconstructed_discrete.flatten())
    
    # I(X;Y) = H(X) + H(Y) - H(X,Y)
    MI = H_X + H_Y - H_XY
    
    return max(0, MI)  # La información mutua no puede ser negativa


def calculate_ber(original_bits: np.ndarray, received_bits: np.ndarray) -> float:
    """
    Calcula la Tasa de Error de Bit (BER).
    
    Args:
        original_bits: Bits originales
        received_bits: Bits recibidos
    
    Returns:
        BER (entre 0 y 1)
    """
    # Asegurar misma longitud
    min_len = min(len(original_bits), len(received_bits))
    original_bits = original_bits[:min_len]
    received_bits = received_bits[:min_len]
    
    # Contar errores
    errors = np.sum(original_bits != received_bits)
    ber = errors / len(original_bits)
    
    return ber


def calculate_ser(original_symbols: np.ndarray, received_symbols: np.ndarray) -> float:
    """
    Calcula la Tasa de Error de Símbolo (SER).
    
    Args:
        original_symbols: Símbolos originales
        received_symbols: Símbolos recibidos
    
    Returns:
        SER (entre 0 y 1)
    """
    min_len = min(len(original_symbols), len(received_symbols))
    original_symbols = original_symbols[:min_len]
    received_symbols = received_symbols[:min_len]
    
    errors = np.sum(original_symbols != received_symbols)
    ser = errors / len(original_symbols)
    
    return ser


def calculate_psnr(original: np.ndarray, reconstructed: np.ndarray) -> float:
    """
    Calcula PSNR (Peak Signal-to-Noise Ratio).
    PSNR = 10 log₁₀(MAX²/MSE)
    
    Args:
        original: Imagen/video original
        reconstructed: Imagen/video reconstruido
    
    Returns:
        PSNR en dB
    """
    # Asegurar misma forma
    min_size = min(original.size, reconstructed.size)
    original = original.flatten()[:min_size]
    reconstructed = reconstructed.flatten()[:min_size]
    
    # Calcular MSE
    mse = np.mean((original - reconstructed) ** 2)
    
    if mse == 0:
        return float('inf')  # Imágenes idénticas
    
    # MAX es el valor máximo posible del píxel
    if original.dtype == np.uint8:
        max_val = 255
    else:
        max_val = np.max(original)
    
    psnr = 10 * np.log10((max_val ** 2) / mse)
    
    return psnr


def calculate_ssim(
    original: np.ndarray,
    reconstructed: np.ndarray,
    data_range: Optional[float] = None
) -> float:
    """
    Calcula SSIM (Structural Similarity Index).
    Implementación simplificada.
    
    Args:
        original: Imagen original
        reconstructed: Imagen reconstruida
        data_range: Rango de datos (ej: 255 para uint8)
    
    Returns:
        SSIM (entre -1 y 1, típicamente entre 0 y 1)
    """
    # Asegurar misma forma
    min_size = min(original.size, reconstructed.size)
    x = original.flatten()[:min_size]
    y = reconstructed.flatten()[:min_size]
    
    if data_range is None:
        if original.dtype == np.uint8:
            data_range = 255
        else:
            data_range = np.max(x) - np.min(x)
    
    # Constantes para estabilidad numérica
    C1 = (0.01 * data_range) ** 2
    C2 = (0.03 * data_range) ** 2
    
    # Cálculos
    mu_x = np.mean(x)
    mu_y = np.mean(y)
    
    sigma_x = np.std(x)
    sigma_y = np.std(y)
    sigma_xy = np.mean((x - mu_x) * (y - mu_y))
    
    # SSIM
    numerator = (2 * mu_x * mu_y + C1) * (2 * sigma_xy + C2)
    denominator = (mu_x**2 + mu_y**2 + C1) * (sigma_x**2 + sigma_y**2 + C2)
    
    ssim = numerator / denominator
    
    return ssim


def calculate_mse(original: np.ndarray, reconstructed: np.ndarray) -> float:
    """
    Calcula el Error Cuadrático Medio (MSE).
    
    Args:
        original: Datos originales
        reconstructed: Datos reconstruidos
    
    Returns:
        MSE
    """
    min_size = min(original.size, reconstructed.size)
    original = original.flatten()[:min_size]
    reconstructed = reconstructed.flatten()[:min_size]
    
    mse = np.mean((original - reconstructed) ** 2)
    return mse


def calculate_snr_signal(signal: np.ndarray, noise: np.ndarray) -> float:
    """
    Calcula SNR de una señal.
    
    Args:
        signal: Señal limpia
        noise: Ruido o error
    
    Returns:
        SNR en dB
    """
    signal_power = np.mean(np.abs(signal) ** 2)
    noise_power = np.mean(np.abs(noise) ** 2)
    
    if noise_power == 0:
        return float('inf')
    
    snr = signal_power / noise_power
    snr_db = 10 * np.log10(snr)
    
    return snr_db


class MetricsCalculator:
    """
    Clase para calcular y almacenar todas las métricas de rendimiento.
    """
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_all_metrics(
        self,
        original_data: np.ndarray,
        reconstructed_data: np.ndarray,
        original_bits: Optional[np.ndarray] = None,
        received_bits: Optional[np.ndarray] = None,
        data_type: str = 'generic'
    ) -> Dict[str, float]:
        """
        Calcula todas las métricas relevantes.
        
        Args:
            original_data: Datos originales
            reconstructed_data: Datos reconstruidos
            original_bits: Bits originales (opcional)
            received_bits: Bits recibidos (opcional)
            data_type: Tipo de datos ('text', 'audio', 'image', 'video')
        
        Returns:
            Diccionario con todas las métricas
        """
        metrics = {}
        
        # Métricas de teoría de la información
        try:
            metrics['entropy'] = calculate_entropy(original_data.flatten())
        except:
            metrics['entropy'] = 0.0
        
        try:
            metrics['mutual_information'] = calculate_mutual_information(
                original_data, reconstructed_data
            )
        except:
            metrics['mutual_information'] = 0.0
        
        # Métricas de error de bits
        if original_bits is not None and received_bits is not None:
            metrics['ber'] = calculate_ber(original_bits, received_bits)
        
        # Métricas de calidad de reconstrucción
        try:
            metrics['mse'] = calculate_mse(original_data, reconstructed_data)
        except:
            metrics['mse'] = 0.0
        
        # Métricas específicas por tipo de datos
        if data_type in ['image', 'video']:
            try:
                metrics['psnr'] = calculate_psnr(original_data, reconstructed_data)
            except:
                metrics['psnr'] = 0.0
            
            try:
                metrics['ssim'] = calculate_ssim(original_data, reconstructed_data)
            except:
                metrics['ssim'] = 0.0
        
        # Métricas de audio
        if data_type == 'audio':
            try:
                # PESQ y STOI requerirían librerías especializadas
                # Por ahora, usamos SNR como proxy
                noise = original_data - reconstructed_data
                metrics['snr'] = calculate_snr_signal(original_data, noise)
            except:
                metrics['snr'] = 0.0
        
        self.metrics = metrics
        return metrics
    
    def get_metrics_summary(self) -> str:
        """
        Genera un resumen legible de las métricas.
        
        Returns:
            String con resumen formateado
        """
        summary = "\n=== Métricas de Rendimiento ===\n"
        
        for key, value in self.metrics.items():
            if isinstance(value, float):
                summary += f"{key.upper()}: {value:.4f}\n"
            else:
                summary += f"{key.upper()}: {value}\n"
        
        return summary
