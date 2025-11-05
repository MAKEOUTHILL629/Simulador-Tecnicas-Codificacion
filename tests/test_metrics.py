"""
Tests para las métricas de rendimiento.
"""

import pytest
import numpy as np
from src.metrics.performance import (
    calculate_entropy,
    calculate_ber,
    calculate_psnr,
    calculate_ssim,
    MetricsCalculator
)


class TestEntropyCalculation:
    """Tests para cálculo de entropía"""
    
    def test_entropy_uniform_distribution(self):
        """Test entropía de distribución uniforme"""
        # 4 símbolos equiprobables: H = log2(4) = 2 bits
        data = np.array([0, 1, 2, 3] * 100)
        entropy = calculate_entropy(data)
        
        assert 1.9 < entropy < 2.1
    
    def test_entropy_deterministic(self):
        """Test entropía de señal determinista"""
        # Un solo símbolo: H = 0
        data = np.array([1] * 100)
        entropy = calculate_entropy(data)
        
        assert entropy < 0.1


class TestBERCalculation:
    """Tests para cálculo de BER"""
    
    def test_ber_no_errors(self):
        """Test BER sin errores"""
        original = np.array([0, 1, 0, 1, 1, 0])
        received = np.array([0, 1, 0, 1, 1, 0])
        
        ber = calculate_ber(original, received)
        assert ber == 0.0
    
    def test_ber_all_errors(self):
        """Test BER con todos los bits erróneos"""
        original = np.array([0, 0, 0, 0])
        received = np.array([1, 1, 1, 1])
        
        ber = calculate_ber(original, received)
        assert ber == 1.0
    
    def test_ber_partial_errors(self):
        """Test BER con errores parciales"""
        original = np.array([0, 1, 0, 1, 1, 0, 1, 1])
        received = np.array([0, 1, 1, 1, 1, 0, 0, 1])
        
        ber = calculate_ber(original, received)
        # 2 errores de 8 bits = 0.25
        assert 0.24 < ber < 0.26


class TestPSNRCalculation:
    """Tests para cálculo de PSNR"""
    
    def test_psnr_identical_signals(self):
        """Test PSNR para señales idénticas"""
        signal = np.random.randint(0, 256, 100, dtype=np.uint8)
        
        psnr = calculate_psnr(signal, signal)
        # PSNR infinito para señales idénticas
        assert psnr > 100
    
    def test_psnr_noisy_signal(self):
        """Test PSNR para señal con ruido"""
        original = np.ones(100, dtype=np.uint8) * 128
        noisy = original + np.random.randint(-10, 10, 100)
        
        psnr = calculate_psnr(original, noisy)
        # Debe ser un valor finito positivo
        assert 20 < psnr < 50


class TestMetricsCalculator:
    """Tests para la clase MetricsCalculator"""
    
    def test_calculator_creation(self):
        """Test creación del calculador de métricas"""
        calc = MetricsCalculator()
        assert calc is not None
    
    def test_calculate_all_metrics(self):
        """Test cálculo de todas las métricas"""
        calc = MetricsCalculator()
        
        original = np.random.randint(0, 256, 100, dtype=np.uint8)
        reconstructed = original + np.random.randint(-5, 5, 100)
        
        metrics = calc.calculate_all_metrics(
            original, reconstructed,
            data_type='image'
        )
        
        assert 'entropy' in metrics
        assert 'mse' in metrics
        assert 'psnr' in metrics


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
