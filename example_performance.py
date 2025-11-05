"""
Performance Optimization Demo

Demonstrates the use of parallel simulation and caching for improved performance.
"""

import numpy as np
import time
from src.performance import ParallelSimulator, CacheManager, benchmark_parallel_vs_sequential
from src.simulator import CommunicationSimulator

print("=" * 70)
print("PERFORMANCE OPTIMIZATION DEMO")
print("=" * 70)

# Base configuration
base_config = {
    'technology': '5G',
    'data_type': 'text',
    'channel_code': 'Polar',
    'modulation': 'QPSK',
    'channel_model': 'AWGN',
    'snr_db': 10.0
}

# ============================================================================
# Example 1: Parallel Monte Carlo Simulation
# ============================================================================
print("\n" + "=" * 70)
print("Example 1: Parallel Monte Carlo Simulation")
print("=" * 70)

n_iterations = 20
data_bits = np.random.randint(0, 2, 1000)

print(f"\nRunning {n_iterations} Monte Carlo iterations...")

# Sequential
print("\n1. Sequential execution:")
start = time.time()
results_seq = []
for i in range(n_iterations):
    sim = CommunicationSimulator(base_config)
    result = sim.run_simulation(data_bits)
    results_seq.append(result)
    print(f"  Iteration {i+1}/{n_iterations} complete", end='\r')
sequential_time = time.time() - start
print(f"\n  Time: {sequential_time:.2f}s")

# Parallel
print("\n2. Parallel execution:")
parallel_sim = ParallelSimulator(n_workers=4)
start = time.time()
result_parallel = parallel_sim.run_monte_carlo(
    base_config, 
    n_iterations,
    lambda: np.random.randint(0, 2, 1000)
)
parallel_time = time.time() - start
print(f"  Time: {parallel_time:.2f}s")

speedup = sequential_time / parallel_time
print(f"\n✅ Speedup: {speedup:.2f}x faster with parallel execution!")

# ============================================================================
# Example 2: SNR Sweep with Parallelization
# ============================================================================
print("\n" + "=" * 70)
print("Example 2: SNR Sweep with Parallelization")
print("=" * 70)

snr_values = np.linspace(0, 20, 11)
print(f"\nRunning SNR sweep from {snr_values[0]} to {snr_values[-1]} dB...")

start = time.time()
snr_results = parallel_sim.run_snr_sweep(
    base_config,
    snr_values,
    data_bits,
    n_trials_per_snr=3
)
sweep_time = time.time() - start

print(f"Time: {sweep_time:.2f}s")
print("\nResults:")
print(f"{'SNR (dB)':<10} {'BER':<12} {'PSNR':<10}")
print("-" * 35)
for snr in snr_values:
    ber = snr_results[snr]['metrics'].get('ber', 0)
    psnr = snr_results[snr]['metrics'].get('psnr', 0)
    print(f"{snr:<10.1f} {ber:<12.6f} {psnr:<10.2f}")

# ============================================================================
# Example 3: Caching System
# ============================================================================
print("\n" + "=" * 70)
print("Example 3: Intelligent Caching")
print("=" * 70)

cache_manager = CacheManager(cache_dir="./cache")

# Clear previous cache
cache_manager.clear()
print("\nCache cleared.")

# First run (no cache)
print("\n1. First run (no cache):")
cache_key = cache_manager._config_hash(base_config)
cached_result = cache_manager.get(base_config)

if cached_result is None:
    print("  No cached result found. Running simulation...")
    start = time.time()
    sim = CommunicationSimulator(base_config)
    result = sim.run_simulation(data_bits)
    first_run_time = time.time() - start
    cache_manager.set(base_config, result)
    print(f"  Time: {first_run_time:.3f}s")
    print("  Result cached.")

# Second run (with cache)
print("\n2. Second run (with cache):")
start = time.time()
cached_result = cache_manager.get(base_config)
cache_hit_time = time.time() - start

if cached_result is not None:
    print("  ✅ Cache hit! Result retrieved from cache.")
    print(f"  Time: {cache_hit_time:.6f}s")
    
    cache_speedup = first_run_time / cache_hit_time
    print(f"\n  Cache speedup: {cache_speedup:.0f}x faster!")
    print(f"  Time saved: {first_run_time - cache_hit_time:.3f}s")

# Cache statistics
print("\nCache statistics:")
print(f"  Cached results: {cache_manager.get_cache_count()}")
print(f"  Cache size: {cache_manager.get_cache_size() / 1024:.2f} KB")

# ============================================================================
# Example 4: Parameter Sweep
# ============================================================================
print("\n" + "=" * 70)
print("Example 4: Parallel Parameter Sweep")
print("=" * 70)

print("\nComparing different modulation schemes...")
modulations = ['QPSK', '16-QAM', '64-QAM', '256-QAM']

start = time.time()
mod_results = parallel_sim.run_parameter_sweep(
    base_config,
    'modulation',
    modulations,
    data_bits
)
sweep_time = time.time() - start

print(f"Time: {sweep_time:.2f}s")
print("\nResults:")
print(f"{'Modulation':<12} {'BER':<12} {'SER':<12}")
print("-" * 40)
for mod, result in zip(modulations, mod_results):
    ber = result['metrics'].get('ber', 0)
    ser = result['metrics'].get('ser', 0)
    print(f"{mod:<12} {ber:<12.6f} {ser:<12.6f}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"\n✅ Parallel execution provides {speedup:.2f}x speedup")
print(f"✅ Caching provides {cache_speedup:.0f}x speedup for repeated simulations")
print(f"✅ SNR sweep completed in {sweep_time:.2f}s")
print(f"✅ Parameter sweep completed in {sweep_time:.2f}s")
print("\nPerformance optimizations successfully demonstrated!")
print("\nTips:")
print("  - Use ParallelSimulator for Monte Carlo and parameter sweeps")
print("  - Use CacheManager to avoid re-running identical simulations")
print("  - Adjust n_workers based on your CPU cores")
print("  - Clear cache periodically to free disk space")
print("=" * 70)
