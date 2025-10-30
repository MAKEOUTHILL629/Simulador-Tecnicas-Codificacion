"""
Tests para los módulos de codificación de fuente.
"""

import pytest
import numpy as np
from src.source_coding.encoders import (
    HuffmanEncoder,
    VideoEncoder,
    AudioEncoder,
    create_source_encoder
)


class TestHuffmanEncoder:
    """Tests para el codificador Huffman"""
    
    def test_huffman_encoder_creation(self):
        """Test creación del codificador Huffman"""
        encoder = HuffmanEncoder()
        assert encoder is not None
    
    def test_huffman_encoding(self):
        """Test codificación Huffman"""
        encoder = HuffmanEncoder()
        data = np.array([1, 2, 1, 3, 1, 2, 1], dtype=np.uint8)
        
        encoded, metadata = encoder.encode(data)
        
        assert len(encoded) > 0
        assert 'codebook' in metadata
        assert encoder.get_compression_ratio() <= 1.0


class TestVideoEncoder:
    """Tests para el codificador de video"""
    
    def test_hevc_encoder(self):
        """Test codificador HEVC"""
        encoder = VideoEncoder(codec='HEVC', quality='high')
        assert encoder.codec == 'HEVC'
        assert encoder.quality == 'high'
    
    def test_video_encoding(self):
        """Test codificación de video"""
        encoder = VideoEncoder(codec='HEVC')
        # Simular frames de video
        video_data = np.random.randint(0, 256, (10, 64, 64), dtype=np.uint8)
        
        encoded, metadata = encoder.encode(video_data)
        
        assert len(encoded) > 0
        assert 'codec' in metadata


class TestFactoryFunction:
    """Tests para la función factory"""
    
    def test_create_text_encoder(self):
        """Test crear codificador para texto"""
        encoder = create_source_encoder('text', '5G')
        assert isinstance(encoder, HuffmanEncoder)
    
    def test_create_audio_encoder_5g(self):
        """Test crear codificador de audio para 5G"""
        encoder = create_source_encoder('audio', '5G')
        assert isinstance(encoder, AudioEncoder)
        assert encoder.codec == 'EVS'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
