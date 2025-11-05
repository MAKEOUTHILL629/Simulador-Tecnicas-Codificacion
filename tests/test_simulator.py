"""
Tests unitarios para el simulador de sistemas de comunicación.
"""

import pytest
import numpy as np
from src.simulator import CommunicationSimulator, create_default_config


class TestSimulatorBasics:
    """Tests básicos del simulador"""
    
    def test_simulator_initialization(self):
        """Test que el simulador se inicializa correctamente"""
        config = create_default_config()
        sim = CommunicationSimulator(config)
        assert sim.config['technology'] == '5G'
        assert sim.config['data_type'] == 'text'
    
    def test_default_config_creation(self):
        """Test creación de configuración por defecto"""
        config = create_default_config()
        assert 'technology' in config
        assert 'channel_code' in config
        assert 'modulation' in config
        assert config['snr_db'] == 10.0
    
    def test_basic_simulation(self):
        """Test simulación básica extremo a extremo"""
        config = create_default_config()
        config['snr_db'] = 20.0  # Alto SNR para BER bajo
        
        sim = CommunicationSimulator(config)
        data = np.random.randint(0, 2, 1000)
        results = sim.run_simulation(data)
        
        # Verificar que retorna resultados
        assert 'metrics' in results
        assert 'ber' in results['metrics']
        assert 'reconstructed_data' in results
        assert 'intermediate_states' in results
        
        # A SNR alto, BER debe ser bajo
        assert results['metrics']['ber'] < 0.1


class TestConfigurationValidation:
    """Tests de validación de configuración"""
    
    def test_invalid_modulation_for_5g(self):
        """Test que configuración inválida lanza error"""
        config = {
            'technology': '5G',
            'modulation': '1024QAM',  # No válido para 5G
            'channel_code': 'LDPC',
            'data_type': 'text',
            'channel_model': 'AWGN',
            'snr_db': 10.0,
            'mode': 'SSCC'
        }
        
        with pytest.raises(ValueError):
            sim = CommunicationSimulator(config)
    
    def test_valid_6g_modulation(self):
        """Test que 1024-QAM es válido para 6G"""
        config = {
            'technology': '6G',
            'modulation': '1024QAM',
            'channel_code': 'LDPC',
            'data_type': 'text',
            'channel_model': 'AWGN',
            'snr_db': 10.0,
            'mode': 'SSCC'
        }
        
        sim = CommunicationSimulator(config)
        assert sim.config['technology'] == '6G'


class TestDataTypes:
    """Tests para diferentes tipos de datos"""
    
    def test_text_transmission(self):
        """Test transmisión de texto"""
        config = create_default_config()
        config['data_type'] = 'text'
        
        sim = CommunicationSimulator(config)
        # Simular texto convertido a bits
        message = "HELLO"
        bits = np.unpackbits(np.array([ord(c) for c in message], dtype=np.uint8))
        
        results = sim.run_simulation(bits)
        assert 'metrics' in results
    
    def test_audio_configuration(self):
        """Test configuración para audio"""
        config = create_default_config()
        config['data_type'] = 'audio'
        
        sim = CommunicationSimulator(config)
        assert sim.config['data_type'] == 'audio'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
