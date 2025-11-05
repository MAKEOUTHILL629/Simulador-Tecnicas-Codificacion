"""
Benchmarking tools for performance analysis.

Provides utilities to measure and compare simulation performance.
"""

import time
import numpy as np
from typing import Dict, List, Callable, Any
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.simulator import CommunicationSimulator


def benchmark_simulation(config: Dict, data_bits: np.ndarray, 
                        n_runs: int = 10) -> Dict[str, float]:
    """
    Benchmark a single simulation configuration.
    
    Args:
        config: Simulator configuration
        data_bits: Data to transmit
        n_runs: Number of benchmark runs
    
    Returns:
        Dictionary with timing statistics
    """
    times = []
    
    for _ in range(n_runs):
        sim = CommunicationSimulator(config)
        
        start_time = time.time()
        sim.run_simulation(data_bits)
        end_time = time.time()
        
        times.append(end_time - start_time)
    
    return {
        'mean_time': np.mean(times),
        'std_time': np.std(times),
        'min_time': np.min(times),
        'max_time': np.max(times),
        'total_time': np.sum(times),
        'n_runs': n_runs
    }


def compare_performance(configs: List[Dict], labels: List[str],
                       data_bits: np.ndarray, n_runs: int = 10) -> Dict:
    """
    Compare performance of multiple configurations.
    
    Args:
        configs: List of configurations to benchmark
        labels: Labels for each configuration
        data_bits: Data to transmit
        n_runs: Number of runs per configuration
    
    Returns:
        Dictionary with comparative results
    """
    results = {}
    
    for config, label in zip(configs, labels):
        print(f"Benchmarking {label}...")
        results[label] = benchmark_simulation(config, data_bits, n_runs)
    
    # Calculate speedups relative to first configuration
    baseline_time = results[labels[0]]['mean_time']
    for label in labels:
        results[label]['speedup'] = baseline_time / results[label]['mean_time']
    
    return results


def benchmark_parallel_vs_sequential(config: Dict, n_simulations: int,
                                    n_workers: int = None) -> Dict:
    """
    Compare parallel vs sequential execution.
    
    Args:
        config: Simulator configuration
        n_simulations: Number of simulations to run
        n_workers: Number of parallel workers
    
    Returns:
        Dictionary with comparison results
    """
    from .parallel_simulator import ParallelSimulator
    
    data_bits = np.random.randint(0, 2, 1000)
    
    # Sequential execution
    print("Running sequential simulations...")
    start_time = time.time()
    for _ in range(n_simulations):
        sim = CommunicationSimulator(config)
        sim.run_simulation(data_bits)
    sequential_time = time.time() - start_time
    
    # Parallel execution
    print(f"Running parallel simulations with {n_workers or 'all'} workers...")
    parallel_sim = ParallelSimulator(n_workers=n_workers)
    start_time = time.time()
    parallel_sim.run_monte_carlo(config, n_simulations, 
                                 lambda: np.random.randint(0, 2, 1000))
    parallel_time = time.time() - start_time
    
    return {
        'sequential_time': sequential_time,
        'parallel_time': parallel_time,
        'speedup': sequential_time / parallel_time,
        'n_simulations': n_simulations,
        'n_workers': n_workers or 'all'
    }
