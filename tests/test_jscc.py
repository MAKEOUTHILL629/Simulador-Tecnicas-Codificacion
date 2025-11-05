"""
Tests for JSCC (Joint Source-Channel Coding) module
"""

import pytest
import numpy as np
from src.jscc.hmm_model import HMMSourceModel
from src.jscc.jscc_decoder import JSCCDecoder, TurboJSCCDecoder, demonstrate_cliff_effect


class TestHMMSourceModel:
    """Tests for HMM source model."""
    
    def test_hmm_initialization(self):
        """Test HMM can be initialized."""
        hmm = HMMSourceModel(n_states=4, alphabet_size=256)
        assert hmm.n_states == 4
        assert hmm.alphabet_size == 256
        assert hmm.transition_matrix.shape == (4, 4)
        assert hmm.emission_matrix.shape == (4, 256)
    
    def test_hmm_training(self):
        """Test HMM training doesn't crash."""
        hmm = HMMSourceModel(n_states=4, alphabet_size=10)
        data = np.random.randint(0, 10, 100)
        hmm.train(data, n_iterations=2)
        # Check matrices are still valid probabilities
        assert np.allclose(hmm.transition_matrix.sum(axis=1), 1.0)
        assert np.allclose(hmm.emission_matrix.sum(axis=1), 1.0)
    
    def test_viterbi_decode(self):
        """Test Viterbi decoding."""
        hmm = HMMSourceModel(n_states=4, alphabet_size=10)
        observations = np.random.randint(0, 10, 20)
        states = hmm.viterbi_decode(observations)
        assert len(states) == len(observations)
        assert all(0 <= s < 4 for s in states)


class TestJSCCDecoder:
    """Tests for JSCC decoder."""
    
    def test_jscc_decoder_creation(self):
        """Test JSCC decoder can be created."""
        hmm = HMMSourceModel(n_states=4, alphabet_size=256)
        decoder = JSCCDecoder(hmm)
        assert decoder.source_model == hmm
    
    def test_jscc_decode(self):
        """Test JSCC decoding."""
        hmm = HMMSourceModel(n_states=4, alphabet_size=256)
        decoder = JSCCDecoder(hmm)
        
        # Create test data
        llrs = np.random.randn(800)
        hard_bits = np.random.randint(0, 2, 800)
        
        decoded = decoder.decode(llrs, hard_bits)
        assert len(decoded) == len(hard_bits)
        assert all(b in [0, 1] for b in decoded)


class TestTurboJSCCDecoder:
    """Tests for Turbo JSCC decoder."""
    
    def test_turbo_decoder_creation(self):
        """Test Turbo JSCC decoder can be created."""
        hmm = HMMSourceModel(n_states=4, alphabet_size=256)
        decoder = TurboJSCCDecoder(hmm, n_iterations=3)
        assert decoder.n_iterations == 3


class TestCliffEffectAnalysis:
    """Tests for cliff effect analysis."""
    
    def test_demonstrate_cliff_effect(self):
        """Test cliff effect analysis."""
        snr_range = np.linspace(0, 15, 8)
        sscc_ber = np.array([0.5, 0.4, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001])
        jscc_ber = np.array([0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005])
        
        analysis = demonstrate_cliff_effect(sscc_ber, jscc_ber, snr_range)
        
        assert 'sscc_cliff_snr' in analysis
        assert 'jscc_smoothness' in analysis
        assert 'avg_ber_improvement' in analysis
        assert isinstance(analysis['sscc_cliff_snr'], (int, float))
