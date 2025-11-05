"""
Results Export Utilities

Functions to save simulation results to various formats (CSV, JSON, Excel).
"""

import json
import csv
import numpy as np
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime


class ResultsExporter:
    """Export simulation results to various formats."""
    
    def __init__(self, output_dir: str = "./results"):
        """
        Initialize results exporter.
        
        Args:
            output_dir: Directory to save results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_to_json(self, results: Dict[str, Any], filename: str = None) -> str:
        """
        Export results to JSON format.
        
        Args:
            results: Dictionary of simulation results
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simulation_results_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Convert numpy arrays to lists for JSON serialization
        json_results = self._convert_for_json(results)
        
        with open(filepath, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        return str(filepath)
    
    def export_to_csv(self, results: Dict[str, Any], filename: str = None) -> str:
        """
        Export results to CSV format.
        
        Args:
            results: Dictionary of simulation results
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simulation_results_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        # Flatten results for CSV
        flat_results = self._flatten_dict(results)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Parameter', 'Value'])
            for key, value in flat_results.items():
                writer.writerow([key, value])
        
        return str(filepath)
    
    def export_metrics_table(self, metrics_list: List[Dict[str, Any]], 
                            filename: str = None) -> str:
        """
        Export multiple simulation metrics to CSV table.
        
        Args:
            metrics_list: List of metric dictionaries
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_table_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        if not metrics_list:
            return str(filepath)
        
        # Get all possible keys
        all_keys = set()
        for metrics in metrics_list:
            all_keys.update(metrics.keys())
        
        all_keys = sorted(list(all_keys))
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            for metrics in metrics_list:
                # Convert numpy types to Python types
                row = {k: self._convert_value(v) for k, v in metrics.items()}
                writer.writerow(row)
        
        return str(filepath)
    
    def export_configuration(self, config: Dict[str, Any], filename: str = None) -> str:
        """
        Export simulation configuration to JSON.
        
        Args:
            config: Configuration dictionary
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"config_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        return str(filepath)
    
    def create_experiment_log(self, experiment_name: str, config: Dict[str, Any],
                             results: Dict[str, Any], notes: str = "") -> str:
        """
        Create comprehensive experiment log.
        
        Args:
            experiment_name: Name of experiment
            config: Configuration used
            results: Results obtained
            notes: Additional notes
            
        Returns:
            Path to log file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"experiment_{experiment_name}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        log = {
            'experiment_name': experiment_name,
            'timestamp': timestamp,
            'configuration': config,
            'results': self._convert_for_json(results),
            'notes': notes
        }
        
        with open(filepath, 'w') as f:
            json.dump(log, f, indent=2)
        
        return str(filepath)
    
    def _convert_for_json(self, obj: Any) -> Any:
        """Convert object to JSON-serializable format."""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: self._convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_for_json(item) for item in obj]
        else:
            return obj
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', 
                     sep: str = '.') -> Dict[str, Any]:
        """Flatten nested dictionary."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, np.ndarray):
                # For arrays, store summary statistics
                items.append((f"{new_key}.mean", float(np.mean(v))))
                items.append((f"{new_key}.std", float(np.std(v))))
                items.append((f"{new_key}.min", float(np.min(v))))
                items.append((f"{new_key}.max", float(np.max(v))))
            else:
                items.append((new_key, self._convert_value(v)))
        return dict(items)
    
    def _convert_value(self, value: Any) -> Any:
        """Convert value to basic Python type."""
        if isinstance(value, np.ndarray):
            return value.tolist()
        elif isinstance(value, (np.integer, np.int64, np.int32)):
            return int(value)
        elif isinstance(value, (np.floating, np.float64, np.float32)):
            return float(value)
        elif isinstance(value, complex):
            return f"{value.real}+{value.imag}j"
        else:
            return value


def save_comparison_results(results_dict: Dict[str, Dict[str, Any]], 
                           output_file: str = "comparison_results.csv"):
    """
    Save comparison results from multiple simulations.
    
    Args:
        results_dict: Dictionary mapping simulation names to results
        output_file: Output CSV file path
    """
    exporter = ResultsExporter()
    
    # Create comparison table
    comparison_data = []
    for sim_name, results in results_dict.items():
        row = {'simulation': sim_name}
        if 'metrics' in results:
            row.update(results['metrics'])
        if 'config' in results:
            row.update({f"config_{k}": v for k, v in results['config'].items()})
        comparison_data.append(row)
    
    return exporter.export_metrics_table(comparison_data, output_file)
