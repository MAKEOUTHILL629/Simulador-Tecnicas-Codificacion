"""
Performance optimization module for the communication simulator.

This module provides tools for:
- Parallel simulations using multiprocessing
- Intelligent caching of results
- Benchmarking and performance analysis
"""

from .parallel_simulator import ParallelSimulator
from .cache_manager import CacheManager
from .benchmarks import benchmark_simulation, compare_performance

__all__ = [
    'ParallelSimulator',
    'CacheManager',
    'benchmark_simulation',
    'compare_performance'
]
