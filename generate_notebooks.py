"""
Script to generate Jupyter notebooks for the simulator.

This creates educational notebooks programmatically.
"""

import json
import os

def create_notebook(cells, filename):
    """Create a Jupyter notebook from cells."""
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)
    
    print(f"Created: {filename}")

def markdown_cell(text):
    """Create a markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.split('\n')
    }

def code_cell(code):
    """Create a code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code.split('\n')
    }

# ============================================================================
# Notebook 1: Introducción
# ============================================================================

notebook1_cells = [
    markdown_cell("""# Introducción al Simulador 5G/6G

## Objetivos de Aprendizaje

Al completar este notebook, serás capaz de:
- Configurar y ejecutar una simulación básica
- Interpretar métricas fundamentales (BER, PSNR, entropía)
- Visualizar resultados de transmisión
- Modificar parámetros de configuración

## Requisitos Previos

- Python 3.8+
- Conocimientos básicos de comunicaciones digitales
- Familiaridad con NumPy y Matplotlib"""),
    
    code_cell("""# Importar librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Agregar directorio padre al path
sys.path.insert(0, os.path.abspath('..'))

from src.simulator import CommunicationSimulator
from src.visualization import plots

print("✅ Librerías importadas correctamente")"""),
    
    markdown_cell("""## 1. Primera Simulación Simple

Vamos a transmitir un mensaje de texto simple usando tecnología 5G."""),
    
    code_cell("""# Configuración básica para 5G
config = {
    'technology': '5G',
    'data_type': 'text',
    'channel_code': 'Polar',
    'modulation': 'QPSK',
    'channel_model': 'AWGN',
    'snr_db': 10.0
}

print("Configuración:")
for key, value in config.items():
    print(f"  {key}: {value}")"""),
    
    code_cell("""# Crear datos de prueba (mensaje simple en bits)
message = "Hola 5G"
data_bits = np.array([int(b) for byte in message.encode() for b in format(byte, '08b')])

print(f"Mensaje original: '{message}'")
print(f"Longitud en bits: {len(data_bits)}")
print(f"Primeros 32 bits: {data_bits[:32]}")"""),
    
    code_cell("""# Crear simulador y ejecutar
sim = CommunicationSimulator(config)
results = sim.run_simulation(data_bits)

print("\\n✅ Simulación completada")
print(f"\\nMétricas principales:")
print(f"  BER (Bit Error Rate): {results['metrics']['ber']:.6f}")
print(f"  Entropía: {results['metrics']['entropy']:.4f} bits")
print(f"  Info. Mutua: {results['metrics']['mutual_info']:.4f} bits")"""),
    
    markdown_cell("""## 2. Visualización de Resultados

Vamos a visualizar la constelación de señal y analizar el canal."""),
    
    code_cell("""# Visualizar constelación
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Diagrama de constelación
plots.plot_constellation(
    results['intermediate_states']['modulated_symbols'],
    results['intermediate_states']['received_symbols'],
    config['modulation'],
    ax=axes[0]
)
axes[0].set_title('Diagrama de Constelación')

# Distribución de LLRs
llrs = results['intermediate_states']['llrs']
axes[1].hist(llrs, bins=50, alpha=0.7, edgecolor='black')
axes[1].set_xlabel('LLR Value')
axes[1].set_ylabel('Frecuencia')
axes[1].set_title('Distribución de LLRs')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\\n📊 Gráficas generadas")"""),
    
    markdown_cell("""## 3. Experimentar con Parámetros

Ahora puedes experimentar cambiando los parámetros:

### Prueba cambiar:
- `snr_db`: Relación señal a ruido (0-20 dB típicamente)
- `modulation`: 'QPSK', '16-QAM', '64-QAM', '256-QAM'
- `channel_code`: 'LDPC', 'Polar'
- `channel_model`: 'AWGN', 'Rayleigh', 'Rician'

### Ejercicio:
1. Ejecuta la simulación con SNR = 5 dB
2. Compara el BER con el resultado anterior
3. ¿Qué sucede con la constelación?"""),
    
    code_cell("""# Tu turno: Experimenta aquí
config_experiment = config.copy()
config_experiment['snr_db'] = 5.0  # Cambiar SNR

sim_exp = CommunicationSimulator(config_experiment)
results_exp = sim_exp.run_simulation(data_bits)

print(f"BER con SNR={config_experiment['snr_db']} dB: {results_exp['metrics']['ber']:.6f}")
print(f"BER con SNR={config['snr_db']} dB: {results['metrics']['ber']:.6f}")
print(f"\\nDiferencia: {abs(results_exp['metrics']['ber'] - results['metrics']['ber']):.6f}")"""),
    
    markdown_cell("""## 4. Conclusiones

### Has aprendido:
- ✅ Cómo configurar una simulación básica
- ✅ Ejecutar la transmisión end-to-end
- ✅ Interpretar métricas clave (BER, entropía, info. mutua)
- ✅ Visualizar resultados con diagramas de constelación
- ✅ Experimentar con diferentes parámetros

### Próximos pasos:
- Notebook 2: Comparación de tecnologías 5G vs 6G
- Notebook 3: Análisis profundo de códigos de canal
- Notebook 4: JSCC vs SSCC (avanzado)

### Para más información:
- Ver `../manual-user.md` para documentación completa
- Ver `../main.py` para más ejemplos
- Ver `../examples_advanced.py` para análisis avanzados""")
]

# ============================================================================
# Generate notebooks
# ============================================================================

if __name__ == '__main__':
    os.makedirs('notebooks', exist_ok=True)
    
    create_notebook(notebook1_cells, 'notebooks/01_Introduccion_Simulador.ipynb')
    
    print("\n✅ Notebooks generados exitosamente")
    print("\nPara usar los notebooks:")
    print("  1. pip install -r requirements-notebooks.txt")
    print("  2. jupyter notebook notebooks/")
