"""
Parallel simulator for running multiple simulations concurrently.

Uses multiprocessing to speed up Monte Carlo simulations and parameter sweeps.
"""

import numpy as np
from multiprocessing import Pool, cpu_count
from typing import List, Dict, Any, Callable
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.simulator import CommunicationSimulator


class ParallelSimulator:
    """
    Parallel wrapper for CommunicationSimulator.
    
    Enables running multiple simulations concurrently using multiprocessing.
    """
    
    def __init__(self, n_workers=None):
        """
        Initialize parallel simulator.
        
        Args:
            n_workers: Number of worker processes. None = use all CPUs.
        """
        self.n_workers = n_workers or cpu_count()
    
    def run_monte_carlo(self, config: Dict, n_iterations: int, 
                       data_generator: Callable = None) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation with multiple iterations in parallel.
        
        Args:
            config: Simulator configuration
            n_iterations: Number of Monte Carlo iterations
            data_generator: Function to generate random data for each iteration
        
        Returns:
            Dictionary with aggregated results
        """
        # Default data generator
        if data_generator is None:
            def data_generator():
                return np.random.randint(0, 2, 1000)
        
        # Create tasks
        tasks = [(config, data_generator()) for _ in range(n_iterations)]
        
        # Run in parallel
        with Pool(self.n_workers) as pool:
            results = pool.starmap(_run_single_simulation, tasks)
        
        # Aggregate results
        return self._aggregate_results(results)
    
    def run_parameter_sweep(self, base_config: Dict, 
                           param_name: str, 
                           param_values: List,
                           data_bits: np.ndarray = None) -> List[Dict]:
        """
        Run parameter sweep in parallel.
        
        Args:
            base_config: Base configuration
            param_name: Name of parameter to sweep
            param_values: List of values to test
            data_bits: Data to transmit (same for all)
        
        Returns:
            List of results for each parameter value
        """
        if data_bits is None:
            data_bits = np.random.randint(0, 2, 1000)
        
        # Create configurations for each parameter value
        configs = []
        for value in param_values:
            config = base_config.copy()
            config[param_name] = value
            configs.append((config, data_bits))
        
        # Run in parallel
        with Pool(self.n_workers) as pool:
            results = pool.starmap(_run_single_simulation, configs)
        
        return results
    
    def run_snr_sweep(self, config: Dict, snr_values: List[float],
                      data_bits: np.ndarray = None, 
                      n_trials_per_snr: int = 1) -> Dict:
        """
        Run SNR sweep in parallel.
        
        Args:
            config: Base configuration
            snr_values: List of SNR values to test
            data_bits: Data to transmit
            n_trials_per_snr: Number of trials per SNR point
        
        Returns:
            Dictionary with SNR values and corresponding metrics
        """
        if data_bits is None:
            data_bits = np.random.randint(0, 2, 1000)
        
        # Create tasks
        tasks = []
        for snr in snr_values:
            for _ in range(n_trials_per_snr):
                config_copy = config.copy()
                config_copy['snr_db'] = snr
                tasks.append((config_copy, data_bits))
        
        # Run in parallel
        with Pool(self.n_workers) as pool:
            results = pool.starmap(_run_single_simulation, tasks)
        
        # Organize results by SNR
        snr_results = {snr: [] for snr in snr_values}
        idx = 0
        for snr in snr_values:
            for _ in range(n_trials_per_snr):
                snr_results[snr].append(results[idx])
                idx += 1
        
        # Average results for each SNR
        averaged_results = {}
        for snr, trial_results in snr_results.items():
            averaged_results[snr] = self._aggregate_results(trial_results)
        
        return averaged_results
    
    def _aggregate_results(self, results: List[Dict]) -> Dict[str, Any]:
        """
        Aggregate results from multiple simulations.
        
        Args:
            results: List of simulation results
        
        Returns:
            Dictionary with averaged metrics
        """
        if not results:
            return {}
        
        aggregated = {
            'n_simulations': len(results),
            'metrics': {}
        }
        
        # Average metrics
        metric_keys = results[0]['metrics'].keys()
        for key in metric_keys:
            values = [r['metrics'][key] for r in results if key in r['metrics']]
            if values and isinstance(values[0], (int, float)):
                aggregated['metrics'][key] = np.mean(values)
                aggregated['metrics'][f'{key}_std'] = np.std(values)
        
        return aggregated


def _run_single_simulation(config: Dict, data_bits: np.ndarray) -> Dict:
    """
    Helper function to run a single simulation (must be at module level for pickling).
    
    Args:
        config: Simulator configuration
        data_bits: Data to transmit
    
    Returns:
        Simulation results
    """
    sim = CommunicationSimulator(config)
    return sim.run_simulation(data_bits)
