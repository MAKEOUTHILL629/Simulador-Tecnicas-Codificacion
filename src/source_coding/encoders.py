"""
Módulo de codificación de fuente (compresión).
Implementa algoritmos de compresión para diferentes tipos de datos.
"""

import numpy as np
from typing import Dict, Any, Tuple
from abc import ABC, abstractmethod


class SourceEncoder(ABC):
    """Clase base abstracta para codificadores de fuente."""
    
    @abstractmethod
    def encode(self, data: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Codifica (comprime) los datos de entrada.
        
        Returns:
            Tuple de (datos codificados, metadatos)
        """
        pass
    
    @abstractmethod
    def get_compression_ratio(self) -> float:
        """Retorna la tasa de compresión alcanzada."""
        pass


class HuffmanEncoder(SourceEncoder):
    """
    Codificador de Huffman para compresión de texto.
    Implementa codificación de entropía básica.
    """
    
    def __init__(self):
        self.codebook = {}
        self.original_size = 0
        self.compressed_size = 0
    
    def encode(self, data: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Codifica datos usando Huffman.
        
        Args:
            data: Array de símbolos a codificar
        
        Returns:
            Tuple de (bits codificados, metadatos con el codebook)
        """
        # Calcular frecuencias
        symbols, counts = np.unique(data, return_counts=True)
        frequencies = dict(zip(symbols, counts))
        
        # Construir árbol de Huffman (simplificado)
        self.codebook = self._build_huffman_tree(frequencies)
        
        # Codificar datos
        encoded_bits = []
        for symbol in data:
            encoded_bits.extend(self.codebook[symbol])
        
        self.original_size = len(data) * 8  # asumiendo 8 bits por símbolo
        self.compressed_size = len(encoded_bits)
        
        metadata = {
            'codebook': self.codebook,
            'original_size': self.original_size,
            'compressed_size': self.compressed_size,
            'symbols': symbols.tolist()
        }
        
        return np.array(encoded_bits, dtype=np.uint8), metadata
    
    def _build_huffman_tree(self, frequencies: Dict) -> Dict:
        """
        Construye un árbol de Huffman y genera el codebook.
        Implementación simplificada.
        """
        # Para una implementación básica, asignamos códigos de longitud variable
        # basados en las frecuencias
        sorted_symbols = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        
        codebook = {}
        code_length = 1
        remaining = len(sorted_symbols)
        
        for symbol, freq in sorted_symbols:
            # Asignar códigos más cortos a símbolos más frecuentes
            code = format(len(codebook), f'0{code_length}b')
            codebook[symbol] = [int(b) for b in code]
            
            if len(codebook) >= 2**code_length - 1:
                code_length += 1
        
        return codebook
    
    def get_compression_ratio(self) -> float:
        """Retorna la tasa de compresión."""
        if self.original_size == 0:
            return 1.0
        return self.compressed_size / self.original_size


class ArithmeticEncoder(SourceEncoder):
    """
    Codificador aritmético para compresión de texto.
    Más eficiente que Huffman para ciertos tipos de datos.
    """
    
    def __init__(self):
        self.original_size = 0
        self.compressed_size = 0
    
    def encode(self, data: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Codifica datos usando codificación aritmética (simplificado)."""
        # Implementación placeholder - en producción usaría un algoritmo completo
        self.original_size = len(data) * 8
        self.compressed_size = int(len(data) * 6)  # Asumiendo 25% de compresión
        
        # Por ahora, simulamos compresión reduciendo redundancia
        compressed = data[::2] if len(data) > 1 else data
        
        metadata = {
            'method': 'arithmetic',
            'original_size': self.original_size,
            'compressed_size': self.compressed_size
        }
        
        return compressed, metadata
    
    def get_compression_ratio(self) -> float:
        if self.original_size == 0:
            return 1.0
        return self.compressed_size / self.original_size


class VideoEncoder(SourceEncoder):
    """
    Codificador de video (simulación de HEVC/VVC).
    En una implementación real, usaría librerías como FFmpeg.
    """
    
    def __init__(self, codec='HEVC', quality='high'):
        """
        Args:
            codec: 'HEVC' (H.265) o 'VVC' (H.266)
            quality: 'low', 'medium', 'high'
        """
        self.codec = codec
        self.quality = quality
        self.original_size = 0
        self.compressed_size = 0
        
        # Tasas de compresión típicas
        self.compression_ratios = {
            'HEVC': {'low': 0.1, 'medium': 0.05, 'high': 0.02},
            'VVC': {'low': 0.08, 'medium': 0.04, 'high': 0.015}
        }
    
    def encode(self, data: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Simula la codificación de video.
        
        Args:
            data: Frames de video como array
        """
        self.original_size = data.size * 8
        ratio = self.compression_ratios[self.codec][self.quality]
        self.compressed_size = int(self.original_size * ratio)
        
        # Simulación: reducir datos según la tasa de compresión
        target_samples = max(1, int(data.size * ratio))
        compressed = np.resize(data, target_samples)
        
        metadata = {
            'codec': self.codec,
            'quality': self.quality,
            'original_size': self.original_size,
            'compressed_size': self.compressed_size,
            'frames': data.shape[0] if data.ndim > 1 else 1
        }
        
        return compressed, metadata
    
    def get_compression_ratio(self) -> float:
        if self.original_size == 0:
            return 1.0
        return self.compressed_size / self.original_size


class AudioEncoder(SourceEncoder):
    """
    Codificador de audio (simulación de EVS/IVAS).
    """
    
    def __init__(self, codec='EVS', bitrate=24000):
        """
        Args:
            codec: 'EVS' o 'IVAS'
            bitrate: Tasa de bits en bps
        """
        self.codec = codec
        self.bitrate = bitrate
        self.original_size = 0
        self.compressed_size = 0
    
    def encode(self, data: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Simula la codificación de audio.
        
        Args:
            data: Muestras de audio
        """
        # Asumiendo una tasa de muestreo estándar
        sample_rate = 16000  # Hz para voz
        duration = len(data) / sample_rate
        
        self.original_size = len(data) * 16  # 16 bits por muestra
        self.compressed_size = int(self.bitrate * duration)
        
        # Simulación de compresión
        ratio = self.compressed_size / self.original_size
        target_samples = max(1, int(len(data) * ratio))
        compressed = np.resize(data, target_samples)
        
        metadata = {
            'codec': self.codec,
            'bitrate': self.bitrate,
            'sample_rate': sample_rate,
            'duration': duration,
            'original_size': self.original_size,
            'compressed_size': self.compressed_size
        }
        
        return compressed, metadata
    
    def get_compression_ratio(self) -> float:
        if self.original_size == 0:
            return 1.0
        return self.compressed_size / self.original_size


def create_source_encoder(data_type: str, technology: str = '5G') -> SourceEncoder:
    """
    Factory function para crear el codificador apropiado según el tipo de datos
    y la tecnología.
    
    Args:
        data_type: 'text', 'audio', 'image', 'video'
        technology: '5G', '5G_Advanced', '6G'
    
    Returns:
        Instancia del codificador apropiado
    """
    if data_type == 'text':
        return HuffmanEncoder()
    
    elif data_type == 'audio':
        codec = 'IVAS' if technology in ['5G_Advanced', '6G'] else 'EVS'
        return AudioEncoder(codec=codec)
    
    elif data_type in ['image', 'video']:
        codec = 'VVC' if technology in ['5G_Advanced', '6G'] else 'HEVC'
        return VideoEncoder(codec=codec)
    
    else:
        raise ValueError(f"Tipo de datos no soportado: {data_type}")
