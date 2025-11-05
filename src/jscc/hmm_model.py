"""
Hidden Markov Model (HMM) for Source Modeling

Implements HMM-based modeling of source redundancy for JSCC decoding.
"""

import numpy as np
from typing import Tuple, Optional


class HMMSourceModel:
    """
    Hidden Markov Model for modeling source statistics.
    
    This model captures residual redundancy left by suboptimal source encoders,
    enabling joint source-channel decoding.
    """
    
    def __init__(self, n_states: int = 4, alphabet_size: int = 256):
        """
        Initialize HMM source model.
        
        Args:
            n_states: Number of hidden states
            alphabet_size: Size of source alphabet (e.g., 256 for bytes)
        """
        self.n_states = n_states
        self.alphabet_size = alphabet_size
        
        # Initialize transition matrix (state to state)
        self.transition_matrix = self._init_transition_matrix()
        
        # Initialize emission matrix (state to symbol)
        self.emission_matrix = self._init_emission_matrix()
        
        # Initial state probabilities
        self.initial_probs = np.ones(n_states) / n_states
    
    def _init_transition_matrix(self) -> np.ndarray:
        """Initialize transition probability matrix."""
        # Start with uniform + diagonal bias (states tend to persist)
        trans = np.random.rand(self.n_states, self.n_states)
        trans = trans + 2 * np.eye(self.n_states)  # Bias toward staying in state
        # Normalize rows
        trans = trans / trans.sum(axis=1, keepdims=True)
        return trans
    
    def _init_emission_matrix(self) -> np.ndarray:
        """Initialize emission probability matrix."""
        # Each state has different symbol distribution
        emis = np.random.rand(self.n_states, self.alphabet_size)
        # Add structure: each state prefers certain symbols
        for i in range(self.n_states):
            start = (i * self.alphabet_size) // self.n_states
            end = ((i + 1) * self.alphabet_size) // self.n_states
            emis[i, start:end] += 2.0  # Boost certain symbols per state
        # Normalize rows
        emis = emis / emis.sum(axis=1, keepdims=True)
        return emis
    
    def train(self, data: np.ndarray, n_iterations: int = 10):
        """
        Train HMM using Baum-Welch algorithm (EM for HMMs).
        
        Args:
            data: Observed symbol sequence (numpy array of integers)
            n_iterations: Number of training iterations
        """
        for _ in range(n_iterations):
            # Forward-backward algorithm
            alpha = self._forward(data)
            beta = self._backward(data)
            
            # E-step: Compute expected state occupancies
            gamma = alpha * beta
            gamma = gamma / gamma.sum(axis=0, keepdims=True)
            
            # M-step: Update parameters
            self._update_parameters(data, gamma)
    
    def _forward(self, data: np.ndarray) -> np.ndarray:
        """Forward algorithm for HMM."""
        T = len(data)
        alpha = np.zeros((self.n_states, T))
        
        # Initialization
        alpha[:, 0] = self.initial_probs * self.emission_matrix[:, data[0]]
        alpha[:, 0] = alpha[:, 0] / (alpha[:, 0].sum() + 1e-10)
        
        # Recursion
        for t in range(1, T):
            for s in range(self.n_states):
                alpha[s, t] = np.sum(alpha[:, t-1] * self.transition_matrix[:, s])
                alpha[s, t] *= self.emission_matrix[s, data[t]]
            alpha[:, t] = alpha[:, t] / (alpha[:, t].sum() + 1e-10)
        
        return alpha
    
    def _backward(self, data: np.ndarray) -> np.ndarray:
        """Backward algorithm for HMM."""
        T = len(data)
        beta = np.zeros((self.n_states, T))
        
        # Initialization
        beta[:, -1] = 1.0
        
        # Recursion (backward)
        for t in range(T-2, -1, -1):
            for s in range(self.n_states):
                beta[s, t] = np.sum(
                    self.transition_matrix[s, :] * 
                    self.emission_matrix[:, data[t+1]] * 
                    beta[:, t+1]
                )
            beta[:, t] = beta[:, t] / (beta[:, t].sum() + 1e-10)
        
        return beta
    
    def _update_parameters(self, data: np.ndarray, gamma: np.ndarray):
        """Update HMM parameters based on expected counts."""
        T = len(data)
        
        # Update initial probabilities
        self.initial_probs = gamma[:, 0]
        
        # Update emission probabilities
        for s in range(self.n_states):
            for symbol in range(self.alphabet_size):
                mask = (data == symbol)
                self.emission_matrix[s, symbol] = np.sum(gamma[s, mask])
        
        # Normalize
        self.emission_matrix = self.emission_matrix / (
            self.emission_matrix.sum(axis=1, keepdims=True) + 1e-10
        )
    
    def viterbi_decode(self, observations: np.ndarray) -> np.ndarray:
        """
        Viterbi algorithm for finding most likely state sequence.
        
        Args:
            observations: Sequence of observed symbols
            
        Returns:
            Most likely state sequence
        """
        T = len(observations)
        
        # Initialize
        delta = np.zeros((self.n_states, T))
        psi = np.zeros((self.n_states, T), dtype=int)
        
        delta[:, 0] = self.initial_probs * self.emission_matrix[:, observations[0]]
        
        # Recursion
        for t in range(1, T):
            for s in range(self.n_states):
                temp = delta[:, t-1] * self.transition_matrix[:, s]
                psi[s, t] = np.argmax(temp)
                delta[s, t] = np.max(temp) * self.emission_matrix[s, observations[t]]
        
        # Backtrack
        states = np.zeros(T, dtype=int)
        states[-1] = np.argmax(delta[:, -1])
        
        for t in range(T-2, -1, -1):
            states[t] = psi[states[t+1], t+1]
        
        return states
    
    def compute_sequence_probability(self, data: np.ndarray) -> float:
        """
        Compute probability of observing a sequence.
        
        Args:
            data: Observed symbol sequence
            
        Returns:
            Log probability of sequence
        """
        alpha = self._forward(data)
        return np.log(alpha[:, -1].sum() + 1e-10)
