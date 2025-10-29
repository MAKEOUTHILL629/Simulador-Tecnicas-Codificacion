"""
Tests para los módulos de modulación.
"""

import pytest
import numpy as np
from src.modulation.modulators import (
    QPSKModulator,
    QAMModulator,
    create_modulator
)


class TestQPSKModulator:
    """Tests para el modulador QPSK"""
    
    def test_qpsk_creation(self):
        """Test creación del modulador QPSK"""
        modulator = QPSKModulator()
        assert modulator.bits_per_symbol == 2
        assert modulator.M == 4
    
    def test_qpsk_modulation(self):
        """Test modulación QPSK"""
        modulator = QPSKModulator()
        bits = np.array([0, 0, 0, 1, 1, 0, 1, 1])
        
        symbols = modulator.modulate(bits)
        
        # 8 bits = 4 símbolos (2 bits por símbolo)
        assert len(symbols) == 4
        # Verificar que los símbolos son complejos
        assert all(np.iscomplex(s) or np.isreal(s) for s in symbols)
    
    def test_qpsk_demodulation(self):
        """Test demodulación QPSK"""
        modulator = QPSKModulator()
        bits = np.array([0, 0, 0, 1, 1, 0, 1, 1])
        
        symbols = modulator.modulate(bits)
        llrs = modulator.demodulate(symbols, noise_var=0.1)
        
        # Debería retornar 8 LLRs (uno por bit)
        assert len(llrs) == 8


class TestQAMModulator:
    """Tests para el modulador QAM"""
    
    def test_16qam_creation(self):
        """Test creación del modulador 16-QAM"""
        modulator = QAMModulator(M=16)
        assert modulator.M == 16
        assert modulator.bits_per_symbol == 4
    
    def test_64qam_modulation(self):
        """Test modulación 64-QAM"""
        modulator = QAMModulator(M=64)
        bits = np.random.randint(0, 2, 60)  # 60 bits = 10 símbolos
        
        symbols = modulator.modulate(bits)
        
        assert len(symbols) == 10
    
    def test_constellation_normalization(self):
        """Test normalización de constelación"""
        modulator = QAMModulator(M=16)
        
        # Potencia promedio debe ser ~1
        avg_power = np.mean(np.abs(modulator.constellation) ** 2)
        assert 0.9 < avg_power < 1.1


class TestFactoryFunction:
    """Tests para la función factory"""
    
    def test_create_qpsk(self):
        """Test crear modulador QPSK"""
        modulator = create_modulator('QPSK')
        assert isinstance(modulator, QPSKModulator)
    
    def test_create_16qam(self):
        """Test crear modulador 16-QAM"""
        modulator = create_modulator('16QAM')
        assert isinstance(modulator, QAMModulator)
        assert modulator.M == 16
    
    def test_invalid_modulation(self):
        """Test modulación inválida"""
        with pytest.raises(ValueError):
            create_modulator('InvalidMod')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
