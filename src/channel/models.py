"""
Módulo de modelado de canal inalámbrico.
Implementa AWGN, Rayleigh y Rician fading.
"""

import numpy as np
from typing import Optional
from abc import ABC, abstractmethod


class Channel(ABC):
    """Clase base abstracta para modelos de canal."""
    
    @abstractmethod
    def transmit(self, signal: np.ndarray) -> np.ndarray:
        """Transmite señal a través del canal."""
        pass
    
    @abstractmethod
    def get_noise_variance(self) -> float:
        """Retorna la varianza del ruido."""
        pass


class AWGNChannel(Channel):
    """
    Canal AWGN (Additive White Gaussian Noise).
    Modelo más simple: añade ruido gaussiano blanco.
    """
    
    def __init__(self, snr_db: float):
        """
        Args:
            snr_db: Relación señal a ruido en dB
        """
        self.snr_db = snr_db
        self.snr_linear = 10 ** (snr_db / 10)
        
        # Varianza del ruido (asumiendo potencia de señal = 1)
        self.noise_variance = 1 / self.snr_linear
    
    def transmit(self, signal: np.ndarray) -> np.ndarray:
        """
        Añade ruido AWGN a la señal.
        
        Args:
            signal: Señal transmitida (símbolos complejos)
        
        Returns:
            Señal recibida con ruido
        """
        # Calcular potencia de la señal
        signal_power = np.mean(np.abs(signal) ** 2)
        
        # Ajustar varianza del ruido según la potencia real de la señal
        noise_var = signal_power / self.snr_linear
        
        # Generar ruido complejo
        noise_std = np.sqrt(noise_var / 2)  # Dividir entre 2 para I y Q
        noise = noise_std * (
            np.random.randn(len(signal)) + 1j * np.random.randn(len(signal))
        )
        
        return signal + noise
    
    def get_noise_variance(self) -> float:
        return self.noise_variance
    
    def set_snr(self, snr_db: float):
        """Actualiza el SNR del canal."""
        self.snr_db = snr_db
        self.snr_linear = 10 ** (snr_db / 10)
        self.noise_variance = 1 / self.snr_linear


class RayleighChannel(Channel):
    """
    Canal con desvanecimiento Rayleigh.
    Modela propagación sin línea de vista (NLOS).
    """
    
    def __init__(self, snr_db: float, doppler_freq: float = 0.0):
        """
        Args:
            snr_db: SNR en dB
            doppler_freq: Frecuencia Doppler normalizada (para canal variable en tiempo)
        """
        self.snr_db = snr_db
        self.snr_linear = 10 ** (snr_db / 10)
        self.doppler_freq = doppler_freq
        self.noise_variance = 1 / self.snr_linear
    
    def transmit(self, signal: np.ndarray) -> np.ndarray:
        """
        Transmite a través de canal Rayleigh.
        
        Args:
            signal: Señal transmitida
        
        Returns:
            Señal recibida con desvanecimiento y ruido
        """
        # Generar coeficientes de desvanecimiento Rayleigh
        # Rayleigh: amplitud sigue distribución Rayleigh, fase uniforme
        h_real = np.random.randn(len(signal))
        h_imag = np.random.randn(len(signal))
        h = (h_real + 1j * h_imag) / np.sqrt(2)  # Normalizado: E[|h|²] = 1
        
        # Aplicar desvanecimiento
        faded_signal = h * signal
        
        # Calcular potencia de señal desvanecida
        signal_power = np.mean(np.abs(faded_signal) ** 2)
        
        # Añadir ruido AWGN
        noise_var = signal_power / self.snr_linear
        noise_std = np.sqrt(noise_var / 2)
        noise = noise_std * (
            np.random.randn(len(signal)) + 1j * np.random.randn(len(signal))
        )
        
        received = faded_signal + noise
        
        # En un sistema real, el receptor estimaría h y ecualizaría
        # Para simplificar, asumimos conocimiento perfecto de canal
        # y ecualizamos dividiendo por h
        h_mag_sq = np.abs(h) ** 2
        # Evitar división por cero
        h_mag_sq = np.maximum(h_mag_sq, 1e-10)
        equalized = received * np.conj(h) / h_mag_sq
        
        return equalized
    
    def get_noise_variance(self) -> float:
        return self.noise_variance


class RicianChannel(Channel):
    """
    Canal con desvanecimiento Rician.
    Modela propagación con componente de línea de vista (LOS).
    """
    
    def __init__(self, snr_db: float, K_factor_db: float = 10.0):
        """
        Args:
            snr_db: SNR en dB
            K_factor_db: Factor K de Rician en dB (relación LOS/NLOS)
        """
        self.snr_db = snr_db
        self.snr_linear = 10 ** (snr_db / 10)
        self.K_factor_db = K_factor_db
        self.K = 10 ** (K_factor_db / 10)
        self.noise_variance = 1 / self.snr_linear
    
    def transmit(self, signal: np.ndarray) -> np.ndarray:
        """
        Transmite a través de canal Rician.
        
        Args:
            signal: Señal transmitida
        
        Returns:
            Señal recibida con desvanecimiento Rician y ruido
        """
        # Componente LOS (determinística)
        h_los = np.sqrt(self.K / (self.K + 1))
        
        # Componente NLOS (aleatoria, Rayleigh)
        h_nlos_real = np.random.randn(len(signal))
        h_nlos_imag = np.random.randn(len(signal))
        h_nlos = (h_nlos_real + 1j * h_nlos_imag) * np.sqrt(1 / (2 * (self.K + 1)))
        
        # Coeficiente de canal Rician
        h = h_los + h_nlos
        
        # Aplicar desvanecimiento
        faded_signal = h * signal
        
        # Calcular potencia
        signal_power = np.mean(np.abs(faded_signal) ** 2)
        
        # Añadir ruido AWGN
        noise_var = signal_power / self.snr_linear
        noise_std = np.sqrt(noise_var / 2)
        noise = noise_std * (
            np.random.randn(len(signal)) + 1j * np.random.randn(len(signal))
        )
        
        received = faded_signal + noise
        
        # Ecualización (asumiendo conocimiento perfecto del canal)
        h_mag_sq = np.abs(h) ** 2
        h_mag_sq = np.maximum(h_mag_sq, 1e-10)
        equalized = received * np.conj(h) / h_mag_sq
        
        return equalized
    
    def get_noise_variance(self) -> float:
        return self.noise_variance


def create_channel(channel_type: str, snr_db: float, **kwargs) -> Channel:
    """
    Factory function para crear modelos de canal.
    
    Args:
        channel_type: 'AWGN', 'Rayleigh', 'Rician'
        snr_db: SNR en dB
        **kwargs: Parámetros adicionales específicos del canal
    
    Returns:
        Instancia del canal
    """
    if channel_type == 'AWGN':
        return AWGNChannel(snr_db)
    
    elif channel_type == 'Rayleigh':
        doppler_freq = kwargs.get('doppler_freq', 0.0)
        return RayleighChannel(snr_db, doppler_freq)
    
    elif channel_type == 'Rician':
        K_factor_db = kwargs.get('K_factor_db', 10.0)
        return RicianChannel(snr_db, K_factor_db)
    
    else:
        raise ValueError(f"Tipo de canal no soportado: {channel_type}")


def calculate_ber_theoretical_awgn(ebn0_db: float, modulation: str) -> float:
    """
    Calcula BER teórico para canal AWGN.
    
    Args:
        ebn0_db: Eb/N0 en dB
        modulation: Tipo de modulación
    
    Returns:
        BER teórico
    """
    from scipy.special import erfc
    
    ebn0_linear = 10 ** (ebn0_db / 10)
    
    if modulation == 'QPSK':
        # BER para QPSK
        ber = 0.5 * erfc(np.sqrt(ebn0_linear))
    
    elif modulation in ['16QAM', '64QAM', '256QAM', '1024QAM']:
        # Aproximación para M-QAM
        M = int(modulation[:-3])
        k = int(np.log2(M))
        ber = (2 / k) * (1 - 1 / np.sqrt(M)) * erfc(
            np.sqrt(3 * k * ebn0_linear / (2 * (M - 1)))
        )
    
    else:
        ber = 0.5  # Fallback
    
    return ber
