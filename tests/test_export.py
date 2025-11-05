"""
Tests for results export utilities
"""

import pytest
import numpy as np
import json
import csv
from pathlib import Path
from src.utils import ResultsExporter, save_comparison_results


class TestResultsExporter:
    """Tests for ResultsExporter class."""
    
    def test_exporter_creation(self, tmp_path):
        """Test exporter can be created."""
        exporter = ResultsExporter(output_dir=str(tmp_path))
        assert exporter.output_dir.exists()
    
    def test_export_to_json(self, tmp_path):
        """Test exporting results to JSON."""
        exporter = ResultsExporter(output_dir=str(tmp_path))
        
        results = {
            'ber': 0.001,
            'snr': 10.0,
            'data': np.array([1, 2, 3])
        }
        
        filepath = exporter.export_to_json(results, 'test.json')
        assert Path(filepath).exists()
        
        # Verify JSON is valid
        with open(filepath, 'r') as f:
            loaded = json.load(f)
        assert loaded['ber'] == 0.001
        assert loaded['data'] == [1, 2, 3]
    
    def test_export_to_csv(self, tmp_path):
        """Test exporting results to CSV."""
        exporter = ResultsExporter(output_dir=str(tmp_path))
        
        results = {
            'ber': 0.001,
            'snr': 10.0,
            'nested': {'value': 5}
        }
        
        filepath = exporter.export_to_csv(results, 'test.csv')
        assert Path(filepath).exists()
        
        # Verify CSV is valid
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert len(rows) > 1  # Header + data
    
    def test_export_metrics_table(self, tmp_path):
        """Test exporting metrics table."""
        exporter = ResultsExporter(output_dir=str(tmp_path))
        
        metrics_list = [
            {'snr': 5, 'ber': 0.1},
            {'snr': 10, 'ber': 0.01},
            {'snr': 15, 'ber': 0.001}
        ]
        
        filepath = exporter.export_metrics_table(metrics_list, 'metrics.csv')
        assert Path(filepath).exists()
        
        # Verify CSV structure
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 3
        assert 'snr' in rows[0]
        assert 'ber' in rows[0]
    
    def test_export_configuration(self, tmp_path):
        """Test exporting configuration."""
        exporter = ResultsExporter(output_dir=str(tmp_path))
        
        config = {
            'technology': '5G',
            'modulation': 'QPSK',
            'snr_db': 10.0
        }
        
        filepath = exporter.export_configuration(config, 'config.json')
        assert Path(filepath).exists()
        
        with open(filepath, 'r') as f:
            loaded = json.load(f)
        assert loaded['technology'] == '5G'
    
    def test_create_experiment_log(self, tmp_path):
        """Test creating experiment log."""
        exporter = ResultsExporter(output_dir=str(tmp_path))
        
        config = {'snr': 10}
        results = {'ber': 0.001}
        
        filepath = exporter.create_experiment_log(
            experiment_name='test_exp',
            config=config,
            results=results,
            notes='Test experiment'
        )
        assert Path(filepath).exists()
        
        with open(filepath, 'r') as f:
            log = json.load(f)
        assert log['experiment_name'] == 'test_exp'
        assert 'timestamp' in log
        assert log['configuration'] == config
    
    def test_handle_numpy_types(self, tmp_path):
        """Test handling of numpy types."""
        exporter = ResultsExporter(output_dir=str(tmp_path))
        
        results = {
            'int64': np.int64(5),
            'float64': np.float64(3.14),
            'array': np.array([1, 2, 3])
        }
        
        filepath = exporter.export_to_json(results, 'numpy_test.json')
        
        with open(filepath, 'r') as f:
            loaded = json.load(f)
        assert loaded['int64'] == 5
        assert isinstance(loaded['float64'], float)
        assert loaded['array'] == [1, 2, 3]


class TestComparisonResults:
    """Tests for comparison results saving."""
    
    def test_save_comparison_results(self, tmp_path):
        """Test saving comparison results."""
        results_dict = {
            'Sim1': {
                'metrics': {'ber': 0.01, 'snr': 10},
                'config': {'modulation': 'QPSK'}
            },
            'Sim2': {
                'metrics': {'ber': 0.005, 'snr': 10},
                'config': {'modulation': '16QAM'}
            }
        }
        
        output_file = str(tmp_path / 'comparison.csv')
        filepath = save_comparison_results(results_dict, output_file)
        
        assert Path(filepath).exists()
        
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 2
        assert rows[0]['simulation'] == 'Sim1'
        assert rows[1]['simulation'] == 'Sim2'
