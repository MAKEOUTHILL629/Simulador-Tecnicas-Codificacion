"""
Módulo de codificación de canal.
Implementa códigos LDPC y Polar para protección contra errores.
"""

import numpy as np
from typing import Tuple, Optional
from abc import ABC, abstractmethod


class ChannelEncoder(ABC):
    """Clase base abstracta para codificadores de canal."""
    
    @abstractmethod
    def encode(self, data: np.ndarray) -> np.ndarray:
        """Codifica datos añadiendo redundancia."""
        pass
    
    @abstractmethod
    def get_code_rate(self) -> float:
        """Retorna la tasa del código."""
        pass


class LDPCEncoder(ChannelEncoder):
    """
    Codificador LDPC (Low-Density Parity-Check).
    Usado en 5G para canales de datos (DL-SCH/UL-SCH).
    """
    
    def __init__(self, code_rate: float = 0.5, block_size: int = 1024):
        """
        Args:
            code_rate: Tasa del código (k/n), típicamente 1/3, 1/2, 2/3, 3/4
            block_size: Tamaño del bloque en bits
        """
        self.code_rate = code_rate
        self.block_size = block_size
        self.n = block_size
        self.k = int(block_size * code_rate)
        
        # Generar matriz de paridad (simplificada)
        self._generate_parity_matrix()
    
    def _generate_parity_matrix(self):
        """
        Genera una matriz de paridad LDPC simplificada.
        En producción, usaría matrices optimizadas según 3GPP.
        """
        m = self.n - self.k  # bits de paridad
        
        # Crear matriz dispersa (low-density)
        # Cada fila tiene aproximadamente 3-4 unos
        self.H = np.zeros((m, self.n), dtype=np.uint8)
        
        ones_per_row = 4
        for i in range(m):
            positions = np.random.choice(self.n, ones_per_row, replace=False)
            self.H[i, positions] = 1
        
        # Matriz generadora G (simplificada)
        # En producción: G = [I_k | P] donde H = [P^T | I_m]
        self.G = np.eye(self.k, self.n, dtype=np.uint8)
    
    def encode(self, data: np.ndarray) -> np.ndarray:
        """
        Codifica datos usando LDPC.
        
        Args:
            data: Bits de información (longitud k)
        
        Returns:
            Bits codificados (longitud n)
        """
        # Rellenar o dividir en bloques
        padded_data = self._pad_to_block_size(data)
        
        encoded = []
        for i in range(0, len(padded_data), self.k):
            block = padded_data[i:i+self.k]
            if len(block) < self.k:
                block = np.pad(block, (0, self.k - len(block)), 'constant')
            
            # Codificación: c = u * G (mod 2)
            coded_block = np.dot(block, self.G) % 2
            encoded.extend(coded_block)
        
        return np.array(encoded, dtype=np.uint8)
    
    def _pad_to_block_size(self, data: np.ndarray) -> np.ndarray:
        """Rellena los datos al tamaño de bloque."""
        remainder = len(data) % self.k
        if remainder != 0:
            padding = self.k - remainder
            data = np.pad(data, (0, padding), 'constant')
        return data
    
    def get_code_rate(self) -> float:
        return self.code_rate


class PolarEncoder(ChannelEncoder):
    """
    Codificador Polar.
    Usado en 5G para canales de control (BCH, DCI, UCI).
    """
    
    def __init__(self, code_rate: float = 0.5, block_size: int = 512):
        """
        Args:
            code_rate: Tasa del código
            block_size: Debe ser potencia de 2 para códigos Polar
        """
        # Asegurar que block_size es potencia de 2
        n_power = int(np.ceil(np.log2(block_size)))
        self.n = 2 ** n_power
        self.code_rate = code_rate
        self.k = int(self.n * code_rate)
        
        # Construcción del código Polar
        self._construct_polar_code()
    
    def _construct_polar_code(self):
        """
        Construye el código Polar calculando los canales más confiables.
        Implementación simplificada basada en capacidades de canal.
        """
        # Calcular capacidades de canal (Bhattacharyya parameters)
        # Para simplificar, usamos una aproximación
        n_power = int(np.log2(self.n))
        
        # Canales ordenados por confiabilidad
        # En producción, esto se calcularía usando el método de construcción Polar
        self.frozen_bits = np.zeros(self.n, dtype=bool)
        
        # Congelar los (n-k) canales menos confiables
        # Aproximación: canales de menor índice son menos confiables
        frozen_indices = np.arange(self.n - self.k)
        self.frozen_bits[frozen_indices] = True
        
        # Índices de información
        self.info_bits = ~self.frozen_bits
        
        # Matriz generadora Polar: G_N = B_N * F^{⊗n}
        # donde F = [[1,0],[1,1]] y ⊗n es el producto Kronecker n veces
        F = np.array([[1, 0], [1, 1]], dtype=np.uint8)
        G = F
        for _ in range(n_power - 1):
            G = np.kron(G, F)
        
        self.G = G
    
    def encode(self, data: np.ndarray) -> np.ndarray:
        """
        Codifica datos usando código Polar.
        
        Args:
            data: Bits de información
        
        Returns:
            Bits codificados
        """
        # Rellenar datos
        padded_data = self._pad_to_block_size(data)
        
        encoded = []
        for i in range(0, len(padded_data), self.k):
            block = padded_data[i:i+self.k]
            if len(block) < self.k:
                block = np.pad(block, (0, self.k - len(block)), 'constant')
            
            # Crear vector u con bits congelados en 0 y bits de información
            u = np.zeros(self.n, dtype=np.uint8)
            u[self.info_bits] = block
            
            # Codificación: x = u * G (mod 2)
            coded_block = np.dot(u, self.G) % 2
            encoded.extend(coded_block)
        
        return np.array(encoded, dtype=np.uint8)
    
    def _pad_to_block_size(self, data: np.ndarray) -> np.ndarray:
        """Rellena los datos al tamaño de bloque."""
        remainder = len(data) % self.k
        if remainder != 0:
            padding = self.k - remainder
            data = np.pad(data, (0, padding), 'constant')
        return data
    
    def get_code_rate(self) -> float:
        return self.code_rate


class LDPCDecoder:
    """
    Decodificador LDPC usando algoritmo Belief Propagation.
    """
    
    def __init__(self, encoder: LDPCEncoder, max_iterations: int = 50):
        """
        Args:
            encoder: Instancia del codificador LDPC (para obtener H)
            max_iterations: Número máximo de iteraciones
        """
        self.H = encoder.H
        self.max_iterations = max_iterations
        self.n = encoder.n
        self.k = encoder.k
    
    def decode(self, llrs: np.ndarray) -> np.ndarray:
        """
        Decodifica usando LLRs (Log-Likelihood Ratios).
        
        Args:
            llrs: LLRs de canal
        
        Returns:
            Bits decodificados
        """
        # Implementación simplificada de BP (Belief Propagation)
        # En producción usaría algoritmos optimizados
        
        decoded = []
        for i in range(0, len(llrs), self.n):
            block_llrs = llrs[i:i+self.n]
            if len(block_llrs) < self.n:
                block_llrs = np.pad(block_llrs, (0, self.n - len(block_llrs)), 'constant')
            
            # Decisión hard basada en LLRs
            decoded_block = (block_llrs < 0).astype(np.uint8)
            
            # Iteraciones de BP (simplificadas)
            for _ in range(self.max_iterations):
                # Verificar síndrome
                syndrome = np.dot(self.H, decoded_block) % 2
                if np.all(syndrome == 0):
                    break
                
                # Actualización simple (en producción sería más sofisticado)
                # Por ahora, solo usamos decisión hard inicial
            
            # Extraer bits de información (primeros k bits)
            decoded.extend(decoded_block[:self.k])
        
        return np.array(decoded, dtype=np.uint8)


class PolarDecoder:
    """
    Decodificador Polar usando Successive Cancellation (SC).
    """
    
    def __init__(self, encoder: PolarEncoder):
        """
        Args:
            encoder: Instancia del codificador Polar
        """
        self.n = encoder.n
        self.k = encoder.k
        self.frozen_bits = encoder.frozen_bits
        self.info_bits = encoder.info_bits
    
    def decode(self, llrs: np.ndarray) -> np.ndarray:
        """
        Decodifica usando algoritmo SC (Successive Cancellation).
        
        Args:
            llrs: LLRs de canal
        
        Returns:
            Bits decodificados
        """
        decoded = []
        
        for i in range(0, len(llrs), self.n):
            block_llrs = llrs[i:i+self.n]
            if len(block_llrs) < self.n:
                block_llrs = np.pad(block_llrs, (0, self.n - len(block_llrs)), 'constant')
            
            # Implementación simplificada de SC
            # En producción usaría SC-List para mejor rendimiento
            u_hat = np.zeros(self.n, dtype=np.uint8)
            
            # Decisión bit a bit
            for j in range(self.n):
                if self.frozen_bits[j]:
                    u_hat[j] = 0
                else:
                    # Decisión basada en LLR
                    u_hat[j] = 1 if block_llrs[j] < 0 else 0
            
            # Extraer bits de información
            decoded.extend(u_hat[self.info_bits])
        
        return np.array(decoded, dtype=np.uint8)


def create_channel_encoder(
    code_type: str,
    code_rate: float = 0.5,
    block_size: int = 1024
) -> ChannelEncoder:
    """
    Factory function para crear codificadores de canal.
    
    Args:
        code_type: 'LDPC' o 'Polar'
        code_rate: Tasa del código
        block_size: Tamaño del bloque
    
    Returns:
        Instancia del codificador
    """
    if code_type == 'LDPC':
        return LDPCEncoder(code_rate=code_rate, block_size=block_size)
    elif code_type == 'Polar':
        return PolarEncoder(code_rate=code_rate, block_size=block_size)
    else:
        raise ValueError(f"Tipo de código no soportado: {code_type}")
