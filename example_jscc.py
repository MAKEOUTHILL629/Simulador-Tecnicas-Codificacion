"""
Example demonstrating Joint Source-Channel Coding (JSCC) vs SSCC

This example shows the key difference between traditional separate source-channel
coding (SSCC) and joint source-channel coding (JSCC), particularly the "cliff effect"
vs "graceful degradation" behavior.
"""

import numpy as np
import matplotlib.pyplot as plt
from src.simulator import CommunicationSimulator
from src.jscc.hmm_model import HMMSourceModel
from src.jscc.jscc_decoder import JSCCDecoder, demonstrate_cliff_effect
from src.utils import ResultsExporter
import os

# Create output directories
os.makedirs('plots', exist_ok=True)
os.makedirs('results', exist_ok=True)

print("=" * 80)
print("JSCC vs SSCC Demonstration")
print("=" * 80)
print()

# Example 1: Train HMM on sample text data
print("Example 1: Training HMM Source Model")
print("-" * 40)

# Load sample text
with open('data/text/sample_text.txt', 'r') as f:
    sample_text = f.read()

# Convert text to bytes
text_bytes = np.frombuffer(sample_text.encode('utf-8'), dtype=np.uint8)

print(f"Training HMM on {len(text_bytes)} bytes of text...")
hmm = HMMSourceModel(n_states=8, alphabet_size=256)
hmm.train(text_bytes[:min(500, len(text_bytes))], n_iterations=5)
print("✓ HMM trained")
print(f"  States: {hmm.n_states}")
print(f"  Alphabet size: {hmm.alphabet_size}")
print()

# Example 2: Compare SSCC vs JSCC performance over SNR range
print("Example 2: SSCC vs JSCC Performance Comparison")
print("-" * 40)

# Configuration
config_base = {
    'technology': '5G',
    'data_type': 'text',
    'channel_code': 'Polar',
    'code_rate': 0.5,
    'modulation': 'QPSK',
    'channel_model': 'AWGN'
}

# SNR range
snr_range = np.linspace(0, 15, 8)
sscc_ber = []
jscc_ber = []
jscc_decoder = JSCCDecoder(hmm)

# Test data
np.random.seed(42)
test_bits = np.random.randint(0, 2, 1000)

print(f"Testing over SNR range: {snr_range[0]:.1f} to {snr_range[-1]:.1f} dB")
print()

for snr in snr_range:
    print(f"  SNR = {snr:5.1f} dB...", end=" ")
    
    config = config_base.copy()
    config['snr_db'] = snr
    
    # SSCC: Traditional separate decoding
    sim_sscc = CommunicationSimulator(config)
    results_sscc = sim_sscc.run_simulation(test_bits)
    ber_sscc = results_sscc['metrics']['ber']
    sscc_ber.append(ber_sscc)
    
    # JSCC: Use source decoder to improve
    # Get LLRs and decoded bits from SSCC
    llrs = results_sscc['intermediate_states']['demodulated_llrs']
    decoded_bits_sscc = results_sscc['intermediate_states']['decoded_channel']
    
    # Apply JSCC decoder
    decoded_bits_jscc = jscc_decoder.decode(llrs, decoded_bits_sscc)
    ber_jscc = np.sum(decoded_bits_jscc[:len(test_bits)] != test_bits) / len(test_bits)
    jscc_ber.append(ber_jscc)
    
    print(f"SSCC BER={ber_sscc:.4f}, JSCC BER={ber_jscc:.4f}")

print("\n✓ Simulation complete")
print()

# Analyze cliff effect
analysis = demonstrate_cliff_effect(
    np.array(sscc_ber),
    np.array(jscc_ber),
    snr_range
)

print("Cliff Effect Analysis:")
print(f"  SSCC cliff occurs at: {analysis['sscc_cliff_snr']:.2f} dB")
print(f"  Cliff magnitude: {analysis['sscc_cliff_magnitude']:.4f}")
print(f"  JSCC smoothness: {analysis['jscc_smoothness']:.6f}")
print(f"  Average BER improvement: {analysis['avg_ber_improvement']:.4f}")
print(f"  Maximum BER improvement: {analysis['max_ber_improvement']:.4f}")
print()

# Plot comparison
plt.figure(figsize=(10, 6))
plt.semilogy(snr_range, sscc_ber, 'o-', label='SSCC (Traditional)', linewidth=2, markersize=8)
plt.semilogy(snr_range, jscc_ber, 's-', label='JSCC (Proposed)', linewidth=2, markersize=8)
plt.xlabel('SNR (dB)', fontsize=12)
plt.ylabel('Bit Error Rate (BER)', fontsize=12)
plt.title('JSCC vs SSCC: Cliff Effect vs Graceful Degradation', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('plots/jscc_vs_sscc_comparison.png', dpi=150, bbox_inches='tight')
print("✓ Saved: plots/jscc_vs_sscc_comparison.png")
print()

# Example 3: Export results to various formats
print("Example 3: Exporting Results")
print("-" * 40)

exporter = ResultsExporter(output_dir='./results')

# Export configuration
config_file = exporter.export_configuration(config_base, 'jscc_config.json')
print(f"✓ Config saved: {config_file}")

# Export comparison results
comparison_results = {
    'SSCC': {
        'config': config_base,
        'metrics': {'ber': sscc_ber, 'snr_range': snr_range.tolist()}
    },
    'JSCC': {
        'config': config_base,
        'metrics': {'ber': jscc_ber, 'snr_range': snr_range.tolist()}
    }
}

json_file = exporter.export_to_json(comparison_results, 'jscc_comparison.json')
print(f"✓ Results saved: {json_file}")

# Export metrics table
metrics_table = []
for i, snr in enumerate(snr_range):
    metrics_table.append({
        'SNR_dB': snr,
        'SSCC_BER': sscc_ber[i],
        'JSCC_BER': jscc_ber[i],
        'Improvement': sscc_ber[i] - jscc_ber[i]
    })

csv_file = exporter.export_metrics_table(metrics_table, 'jscc_metrics_table.csv')
print(f"✓ Metrics table saved: {csv_file}")

# Create experiment log
log_file = exporter.create_experiment_log(
    experiment_name='JSCC_vs_SSCC',
    config=config_base,
    results=comparison_results,
    notes="Demonstration of cliff effect (SSCC) vs graceful degradation (JSCC)"
)
print(f"✓ Experiment log saved: {log_file}")
print()

print("=" * 80)
print("JSCC Demonstration Complete!")
print("=" * 80)
print()
print("Key Findings:")
print(f"  • SSCC exhibits cliff effect at {analysis['sscc_cliff_snr']:.1f} dB")
print(f"  • JSCC provides graceful degradation (smoothness: {analysis['jscc_smoothness']:.6f})")
print(f"  • Average BER improvement: {analysis['avg_ber_improvement']*100:.2f}%")
print()
print("Files Generated:")
print("  • plots/jscc_vs_sscc_comparison.png")
print(f"  • {csv_file}")
print(f"  • {json_file}")
print(f"  • {log_file}")
print()
