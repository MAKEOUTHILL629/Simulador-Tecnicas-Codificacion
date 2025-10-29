"""
Módulo de modulación digital.
Implementa esquemas QPSK, 16-QAM, 64-QAM, 256-QAM, 1024-QAM.
"""

import numpy as np
from typing import Dict, Tuple
from abc import ABC, abstractmethod


class Modulator(ABC):
    """Clase base abstracta para moduladores."""
    
    @abstractmethod
    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """Modula bits a símbolos complejos."""
        pass
    
    @abstractmethod
    def demodulate(self, symbols: np.ndarray) -> np.ndarray:
        """Demodula símbolos a LLRs."""
        pass
    
    @abstractmethod
    def get_constellation(self) -> np.ndarray:
        """Retorna los puntos de la constelación."""
        pass


class QPSKModulator(Modulator):
    """
    Modulador QPSK (Quadrature Phase Shift Keying).
    2 bits por símbolo.
    """
    
    def __init__(self):
        self.bits_per_symbol = 2
        self.M = 4  # Tamaño de la constelación
        
        # Constelación QPSK normalizada
        self.constellation = np.array([
            1 + 1j,   # 00
            1 - 1j,   # 01
            -1 + 1j,  # 10
            -1 - 1j   # 11
        ]) / np.sqrt(2)
        
        # Mapeo de bits a símbolos
        self.bit_map = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 2,
            (1, 1): 3
        }
    
    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """
        Modula bits a símbolos QPSK.
        
        Args:
            bits: Array de bits (0s y 1s)
        
        Returns:
            Array de símbolos complejos
        """
        # Rellenar bits para completar símbolos
        padding = (self.bits_per_symbol - len(bits) % self.bits_per_symbol) % self.bits_per_symbol
        if padding > 0:
            bits = np.pad(bits, (0, padding), 'constant')
        
        # Agrupar bits en símbolos
        bit_pairs = bits.reshape(-1, self.bits_per_symbol)
        
        # Mapear a constelación
        symbols = []
        for pair in bit_pairs:
            idx = self.bit_map[tuple(pair)]
            symbols.append(self.constellation[idx])
        
        return np.array(symbols)
    
    def demodulate(self, symbols: np.ndarray, noise_var: float = 0.1) -> np.ndarray:
        """
        Demodula símbolos a LLRs.
        
        Args:
            symbols: Símbolos recibidos (posiblemente con ruido)
            noise_var: Varianza del ruido
        
        Returns:
            LLRs para cada bit
        """
        llrs = []
        
        for symbol in symbols:
            # Calcular distancias euclidianas a todos los puntos de la constelación
            distances = np.abs(symbol - self.constellation) ** 2
            
            # Para cada bit, calcular LLR
            for bit_pos in range(self.bits_per_symbol):
                # Símbolos con bit=0 en esta posición
                indices_0 = [i for i, bits in enumerate(self.bit_map.items()) 
                            if bits[0][bit_pos] == 0]
                # Símbolos con bit=1 en esta posición
                indices_1 = [i for i, bits in enumerate(self.bit_map.items()) 
                            if bits[0][bit_pos] == 1]
                
                # LLR = log(P(bit=0|y) / P(bit=1|y))
                # Aproximación: LLR ≈ (min_d1 - min_d0) / noise_var
                min_d0 = np.min(distances[indices_0])
                min_d1 = np.min(distances[indices_1])
                
                llr = (min_d1 - min_d0) / noise_var
                llrs.append(llr)
        
        return np.array(llrs)
    
    def get_constellation(self) -> np.ndarray:
        return self.constellation


class QAMModulator(Modulator):
    """
    Modulador QAM genérico (16-QAM, 64-QAM, 256-QAM, 1024-QAM).
    """
    
    def __init__(self, M: int = 16):
        """
        Args:
            M: Tamaño de la constelación (16, 64, 256, 1024)
        """
        if M not in [16, 64, 256, 1024]:
            raise ValueError("M debe ser 16, 64, 256 o 1024")
        
        self.M = M
        self.bits_per_symbol = int(np.log2(M))
        
        # Generar constelación QAM
        self.constellation = self._generate_qam_constellation()
        
        # Crear mapeo de bits a símbolos (Gray coding)
        self.bit_map = self._create_gray_mapping()
    
    def _generate_qam_constellation(self) -> np.ndarray:
        """
        Genera constelación QAM cuadrada.
        """
        # Número de puntos por dimensión (I y Q)
        sqrt_M = int(np.sqrt(self.M))
        
        # Crear grid
        levels = np.arange(sqrt_M) - (sqrt_M - 1) / 2
        levels = levels * 2  # Espaciado
        
        # Crear constelación
        constellation = []
        for qi in levels:
            for ii in levels:
                constellation.append(ii + 1j * qi)
        
        constellation = np.array(constellation)
        
        # Normalizar potencia promedio a 1
        avg_power = np.mean(np.abs(constellation) ** 2)
        constellation = constellation / np.sqrt(avg_power)
        
        return constellation
    
    def _create_gray_mapping(self) -> Dict:
        """
        Crea mapeo de bits a índices usando Gray coding.
        Simplificado para esta implementación.
        """
        bit_map = {}
        for i in range(self.M):
            # Convertir índice a bits
            bits = tuple(int(b) for b in format(i, f'0{self.bits_per_symbol}b'))
            bit_map[bits] = i
        return bit_map
    
    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """Modula bits a símbolos QAM."""
        # Rellenar bits
        padding = (self.bits_per_symbol - len(bits) % self.bits_per_symbol) % self.bits_per_symbol
        if padding > 0:
            bits = np.pad(bits, (0, padding), 'constant')
        
        # Agrupar bits
        bit_groups = bits.reshape(-1, self.bits_per_symbol)
        
        # Mapear a constelación
        symbols = []
        for group in bit_groups:
            idx = self.bit_map[tuple(group)]
            symbols.append(self.constellation[idx])
        
        return np.array(symbols)
    
    def demodulate(self, symbols: np.ndarray, noise_var: float = 0.1) -> np.ndarray:
        """Demodula símbolos a LLRs."""
        llrs = []
        
        for symbol in symbols:
            # Calcular distancias
            distances = np.abs(symbol - self.constellation) ** 2
            
            # Para cada posición de bit
            for bit_pos in range(self.bits_per_symbol):
                # Índices con bit=0 y bit=1 en esta posición
                indices_0 = [i for bits, i in self.bit_map.items() 
                            if bits[bit_pos] == 0]
                indices_1 = [i for bits, i in self.bit_map.items() 
                            if bits[bit_pos] == 1]
                
                # Calcular LLR
                min_d0 = np.min(distances[indices_0])
                min_d1 = np.min(distances[indices_1])
                
                llr = (min_d1 - min_d0) / noise_var
                llrs.append(llr)
        
        return np.array(llrs)
    
    def get_constellation(self) -> np.ndarray:
        return self.constellation


def create_modulator(scheme: str) -> Modulator:
    """
    Factory function para crear moduladores.
    
    Args:
        scheme: 'QPSK', '16QAM', '64QAM', '256QAM', '1024QAM'
    
    Returns:
        Instancia del modulador
    """
    if scheme == 'QPSK':
        return QPSKModulator()
    elif scheme == '16QAM':
        return QAMModulator(M=16)
    elif scheme == '64QAM':
        return QAMModulator(M=64)
    elif scheme == '256QAM':
        return QAMModulator(M=256)
    elif scheme == '1024QAM':
        return QAMModulator(M=1024)
    else:
        raise ValueError(f"Esquema de modulación no soportado: {scheme}")


def calculate_ebn0_from_snr(snr_db: float, code_rate: float, bits_per_symbol: int) -> float:
    """
    Convierte SNR a Eb/N0.
    
    Args:
        snr_db: SNR en dB
        code_rate: Tasa del código de canal
        bits_per_symbol: Bits por símbolo de modulación
    
    Returns:
        Eb/N0 en dB
    """
    snr_linear = 10 ** (snr_db / 10)
    ebn0_linear = snr_linear / (code_rate * bits_per_symbol)
    ebn0_db = 10 * np.log10(ebn0_linear)
    return ebn0_db
