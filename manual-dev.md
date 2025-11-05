# Manual de Desarrollador - Simulador de Sistemas de Comunicación 5G/6G

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Guía de Módulos](#guía-de-módulos)
6. [Ejecución Local](#ejecución-local)
7. [Testing y Validación](#testing-y-validación)
8. [Extensión del Simulador](#extensión-del-simulador)
9. [Contribución al Proyecto](#contribución-al-proyecto)
10. [Debugging y Troubleshooting](#debugging-y-troubleshooting)

---

## Introducción

### Propósito del Documento

Este manual está dirigido a desarrolladores que desean:
- Entender la arquitectura interna del simulador
- Ejecutar y debuggear el código localmente
- Extender funcionalidades existentes
- Agregar nuevos módulos o características
- Contribuir al proyecto

### Requisitos Previos

**Conocimientos**:
- Python 3.7+
- NumPy y computación científica
- Conceptos de sistemas de comunicación
- Git y control de versiones

**Software**:
- Python 3.7 o superior
- pip (gestor de paquetes)
- Git
- Editor de código (VS Code, PyCharm, etc.)

---

## Arquitectura del Sistema

### Principios de Diseño

El simulador sigue estos principios arquitectónicos:

1. **Modularidad**: Cada componente es independiente y reemplazable
2. **Separación de Responsabilidades**: Cada módulo tiene una función clara
3. **Extensibilidad**: Fácil agregar nuevos esquemas sin modificar código existente
4. **Configurabilidad**: Parámetros externalizados en diccionarios
5. **Testeabilidad**: Componentes pueden probarse de forma aislada

### Patrón de Arquitectura

El simulador implementa un **Pipeline Pattern** con estos componentes:

```
[Fuente] → [Codif. Fuente] → [Codif. Canal] → [Modulación] 
    ↓
[Canal] → [Demodulación] → [Decodif. Canal] → [Decodif. Fuente]
    ↓
[Métricas] → [Visualización]
```

Cada componente:
- Recibe entrada del componente anterior
- Realiza su transformación
- Pasa salida al siguiente componente
- Opcionalmente guarda estado intermedio

### Diagrama de Clases Principal

```
CommunicationSimulator (orquestador)
    ├── SourceEncoder (abstracto)
    │   ├── HuffmanEncoder
    │   ├── ArithmeticEncoder
    │   ├── VideoEncoder
    │   └── AudioEncoder
    ├── ChannelEncoder (abstracto)
    │   ├── LDPCEncoder
    │   └── PolarEncoder
    ├── Modulator (abstracto)
    │   ├── QPSKModulator
    │   └── QAMModulator
    ├── Channel (abstracto)
    │   ├── AWGNChannel
    │   ├── RayleighChannel
    │   └── RicianChannel
    ├── MetricsCalculator
    └── SimulatorVisualizer
```

### Flujo de Datos

```python
# Entrada: bits originales
original_bits = [0, 1, 1, 0, ...]

# 1. Codificación de fuente (compresión)
compressed_bits = source_encoder.encode(original_bits)
# Output: [1, 0, 1, ...] (menos bits)

# 2. Codificación de canal (FEC)
encoded_bits = channel_encoder.encode(compressed_bits)
# Output: [1, 0, 1, 0, 1, ...] (más bits con redundancia)

# 3. Modulación
symbols = modulator.modulate(encoded_bits)
# Output: [1+1j, -1+1j, ...] (símbolos complejos)

# 4. Canal
received_symbols = channel.transmit(symbols)
# Output: [0.9+1.1j, -1.2+0.8j, ...] (con ruido)

# 5. Demodulación
llrs = modulator.demodulate(received_symbols)
# Output: [2.3, -1.8, 0.5, ...] (soft decisions)

# 6. Decodificación de canal
decoded_bits = channel_decoder.decode(llrs)
# Output: [1, 0, 1, ...] (bits recuperados)

# 7. Decodificación de fuente
reconstructed = source_decoder.decode(decoded_bits)
# Output: bits reconstruidos
```

---

## Configuración del Entorno de Desarrollo

### Instalación Paso a Paso

#### 1. Clonar el Repositorio

```bash
# Clonar
git clone https://github.com/MAKEOUTHILL629/Simulador-Tecnicas-Codificacion.git
cd Simulador-Tecnicas-Codificacion

# Verificar estructura
ls -la
```

#### 2. Crear Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar (Linux/Mac)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# Verificar activación
which python  # Debe apuntar a venv/bin/python
```

#### 3. Instalar Dependencias

```bash
# Instalar paquetes
pip install -r requirements.txt

# Verificar instalación
python -c "import numpy; import matplotlib; print('OK')"
```

#### 4. Verificar Instalación

```bash
# Ejecutar tests básicos
python -c "from src.simulator import CommunicationSimulator; print('Simulator OK')"

# Ejecutar ejemplo
python main.py
```

Si todo funciona, verás:
```
=====================================...
SIMULADOR DE SISTEMAS DE COMUNICACIÓN 5G/6G
...
✓ Simulación completada exitosamente
```

### Configuración de IDE

#### VS Code

Crear `.vscode/settings.json`:
```json
{
    "python.pythonPath": "venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false
}
```

#### PyCharm

1. File → Settings → Project → Python Interpreter
2. Seleccionar `venv/bin/python`
3. Marcar `src/` como "Sources Root"

---

## Estructura del Proyecto

### Árbol de Directorios

```
Simulador-Tecnicas-Codificacion/
│
├── README.md                  # Especificación técnica completa
├── job.md                     # Estado del proyecto
├── manual-user.md             # Manual de usuario
├── manual-dev.md              # Este archivo
├── requirements.txt           # Dependencias Python
├── main.py                    # Script principal con ejemplos
│
├── src/                       # Código fuente
│   ├── __init__.py
│   ├── simulator.py           # Simulador principal
│   │
│   ├── source_coding/         # Codificación de fuente
│   │   ├── __init__.py
│   │   └── encoders.py        # Codificadores de fuente
│   │
│   ├── channel_coding/        # Codificación de canal
│   │   ├── __init__.py
│   │   └── codes.py           # Códigos LDPC y Polar
│   │
│   ├── modulation/            # Modulación digital
│   │   ├── __init__.py
│   │   └── modulators.py      # Moduladores QPSK/QAM
│   │
│   ├── channel/               # Modelos de canal
│   │   ├── __init__.py
│   │   └── models.py          # Canales AWGN/Rayleigh/Rician
│   │
│   ├── metrics/               # Métricas de rendimiento
│   │   ├── __init__.py
│   │   └── performance.py     # Cálculo de métricas
│   │
│   └── visualization/         # Visualización
│       ├── __init__.py
│       └── plots.py           # Generación de gráficas
│
├── data/                      # Datos de prueba (opcional)
│   ├── text/
│   ├── audio/
│   ├── image/
│   └── video/
│
├── tests/                     # Tests unitarios (a crear)
│   ├── __init__.py
│   ├── test_simulator.py
│   ├── test_encoders.py
│   ├── test_channel_codes.py
│   ├── test_modulators.py
│   └── test_metrics.py
│
└── plots/                     # Gráficas generadas (output)
    └── .gitkeep
```

### Descripción de Módulos Principales

#### `src/simulator.py`
Orquestador principal que:
- Coordina todos los componentes
- Valida configuración
- Ejecuta pipeline completo E2E
- Almacena estados intermedios
- Retorna resultados y métricas

**Clase principal**: `CommunicationSimulator`

#### `src/source_coding/encoders.py`
Implementa compresión de datos:
- `HuffmanEncoder`: Codificación Huffman para texto
- `ArithmeticEncoder`: Codificación aritmética
- `VideoEncoder`: Simulación HEVC/VVC
- `AudioEncoder`: Simulación EVS/IVAS

**Factory**: `create_source_encoder(data_type, technology)`

#### `src/channel_coding/codes.py`
Códigos de corrección de errores:
- `LDPCEncoder/Decoder`: Códigos LDPC para datos
- `PolarEncoder/Decoder`: Códigos Polar para control

**Factory**: `create_channel_encoder(code_type, code_rate, block_size)`

#### `src/modulation/modulators.py`
Modulación digital:
- `QPSKModulator`: QPSK (2 bits/símbolo)
- `QAMModulator`: 16/64/256/1024-QAM

Incluye:
- Generación de constelaciones
- Demodulación con LLRs
- Cálculo de Eb/N0

**Factory**: `create_modulator(scheme)`

#### `src/channel/models.py`
Modelos de canal inalámbrico:
- `AWGNChannel`: Ruido gaussiano
- `RayleighChannel`: Desvanecimiento NLOS
- `RicianChannel`: Desvanecimiento con LOS

**Factory**: `create_channel(channel_type, snr_db, **kwargs)`

#### `src/metrics/performance.py`
Cálculo de métricas:
- Teoría de información: entropía, información mutua
- Errores: BER, SER
- Calidad: PSNR, SSIM, MSE

**Clase principal**: `MetricsCalculator`

#### `src/visualization/plots.py`
Generación de gráficas:
- Diagramas de constelación
- Curvas BER vs Eb/N0
- Comparaciones de calidad
- Formas de onda

**Clase principal**: `SimulatorVisualizer`

---

## Guía de Módulos

### Cómo Funciona Cada Módulo

#### Módulo: Source Coding

**Propósito**: Comprimir datos eliminando redundancia

**Implementación**:
```python
# Clase base abstracta
class SourceEncoder(ABC):
    @abstractmethod
    def encode(self, data: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_compression_ratio(self) -> float:
        pass

# Ejemplo: Huffman
class HuffmanEncoder(SourceEncoder):
    def encode(self, data):
        # 1. Calcular frecuencias
        symbols, counts = np.unique(data, return_counts=True)
        frequencies = dict(zip(symbols, counts))
        
        # 2. Construir árbol Huffman
        codebook = self._build_huffman_tree(frequencies)
        
        # 3. Codificar datos
        encoded_bits = []
        for symbol in data:
            encoded_bits.extend(codebook[symbol])
        
        return np.array(encoded_bits), {'codebook': codebook}
```

**Puntos de extensión**:
- Agregar nuevo codificador: heredar de `SourceEncoder`
- Modificar factory `create_source_encoder()`

#### Módulo: Channel Coding

**Propósito**: Agregar redundancia para detectar/corregir errores

**Implementación LDPC**:
```python
class LDPCEncoder(ChannelEncoder):
    def __init__(self, code_rate, block_size):
        self.code_rate = code_rate
        self.n = block_size
        self.k = int(block_size * code_rate)
        
        # Generar matriz de paridad H
        self._generate_parity_matrix()
    
    def encode(self, data):
        # Codificación: c = u * G (mod 2)
        encoded = []
        for i in range(0, len(data), self.k):
            block = data[i:i+self.k]
            coded_block = np.dot(block, self.G) % 2
            encoded.extend(coded_block)
        return np.array(encoded)
```

**Decodificación**:
```python
class LDPCDecoder:
    def decode(self, llrs):
        # Belief Propagation iterativo
        for iteration in range(self.max_iterations):
            # 1. Check node update
            # 2. Variable node update
            # 3. Verificar convergencia
            syndrome = np.dot(self.H, decoded_block) % 2
            if np.all(syndrome == 0):
                break
```

**Puntos de extensión**:
- Agregar códigos convolucionales
- Implementar códigos Turbo
- Usar matrices 3GPP reales

#### Módulo: Modulation

**Propósito**: Mapear bits a símbolos complejos

**Implementación QAM**:
```python
class QAMModulator:
    def __init__(self, M):
        self.M = M  # Tamaño de constelación
        self.bits_per_symbol = int(np.log2(M))
        
        # Generar constelación cuadrada
        self.constellation = self._generate_qam_constellation()
    
    def modulate(self, bits):
        # Agrupar bits en símbolos
        bit_groups = bits.reshape(-1, self.bits_per_symbol)
        
        # Mapear a constelación
        symbols = []
        for group in bit_groups:
            idx = self.bit_map[tuple(group)]
            symbols.append(self.constellation[idx])
        
        return np.array(symbols)
    
    def demodulate(self, symbols, noise_var):
        # Calcular LLRs usando distancias euclidianas
        llrs = []
        for symbol in symbols:
            distances = np.abs(symbol - self.constellation) ** 2
            
            for bit_pos in range(self.bits_per_symbol):
                # LLR para bit_pos
                min_d0 = min(dist for i, dist in enumerate(distances) 
                            if bit_at_pos(i, bit_pos) == 0)
                min_d1 = min(dist for i, dist in enumerate(distances) 
                            if bit_at_pos(i, bit_pos) == 1)
                
                llr = (min_d1 - min_d0) / noise_var
                llrs.append(llr)
        
        return np.array(llrs)
```

**LLR Concept**:
```
LLR > 0: bit probablemente es 0
LLR < 0: bit probablemente es 1
|LLR|: confianza de la decisión

Ejemplo:
LLR = +5: muy confiado que es 0
LLR = -0.1: poco confiado que es 1
```

#### Módulo: Channel

**Propósito**: Simular degradación en transmisión

**Implementación AWGN**:
```python
class AWGNChannel:
    def __init__(self, snr_db):
        self.snr_db = snr_db
        self.snr_linear = 10 ** (snr_db / 10)
        self.noise_variance = 1 / self.snr_linear
    
    def transmit(self, signal):
        # Calcular potencia de señal
        signal_power = np.mean(np.abs(signal) ** 2)
        
        # Ajustar varianza de ruido
        noise_var = signal_power / self.snr_linear
        noise_std = np.sqrt(noise_var / 2)
        
        # Generar ruido complejo
        noise = noise_std * (
            np.random.randn(len(signal)) + 
            1j * np.random.randn(len(signal))
        )
        
        return signal + noise
```

**Implementación Rayleigh**:
```python
class RayleighChannel:
    def transmit(self, signal):
        # Coeficientes de desvanecimiento
        h = (np.random.randn(len(signal)) + 
             1j * np.random.randn(len(signal))) / np.sqrt(2)
        
        # Aplicar desvanecimiento
        faded = h * signal
        
        # Agregar ruido
        noise = self._generate_noise(len(signal))
        received = faded + noise
        
        # Ecualización (asumiendo CSI perfecto)
        equalized = received * np.conj(h) / np.abs(h)**2
        
        return equalized
```

#### Módulo: Metrics

**Propósito**: Evaluar rendimiento del sistema

**Métricas Implementadas**:
```python
def calculate_ber(original, received):
    errors = np.sum(original != received)
    return errors / len(original)

def calculate_entropy(data):
    symbols, counts = np.unique(data, return_counts=True)
    probs = counts / len(data)
    return -np.sum(probs * np.log2(probs + 1e-10))

def calculate_mutual_information(X, Y):
    H_X = calculate_entropy(X)
    H_Y = calculate_entropy(Y)
    H_XY = calculate_joint_entropy(X, Y)
    return H_X + H_Y - H_XY

def calculate_psnr(original, reconstructed):
    mse = np.mean((original - reconstructed) ** 2)
    max_val = np.max(original)
    return 10 * np.log10(max_val**2 / mse)

def calculate_ssim(x, y):
    # Simplificado
    mu_x, mu_y = np.mean(x), np.mean(y)
    sigma_x, sigma_y = np.std(x), np.std(y)
    sigma_xy = np.mean((x - mu_x) * (y - mu_y))
    
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2
    
    ssim = ((2*mu_x*mu_y + C1) * (2*sigma_xy + C2)) / \
           ((mu_x**2 + mu_y**2 + C1) * (sigma_x**2 + sigma_y**2 + C2))
    
    return ssim
```

---

## Ejecución Local

### Ejecutar Ejemplos Predefinidos

```bash
# Desde directorio raíz
python main.py
```

Output esperado:
```
======================================================================
SIMULADOR DE SISTEMAS DE COMUNICACIÓN 5G/6G
======================================================================

Este simulador implementa:
  • Codificación de fuente (HEVC, VVC, EVS, IVAS, Huffman)
  ...

======================================================================
EJEMPLO 1: SIMULACIÓN DE TRANSMISIÓN DE TEXTO
======================================================================

Mensaje original: HELLO WORLD
...
✓ Simulación completada exitosamente

...
```

### Ejecutar Simulación Personalizada

Crear `test_custom.py`:
```python
#!/usr/bin/env python3
import numpy as np
import sys
sys.path.insert(0, 'src')

from simulator import CommunicationSimulator

# Tu configuración
config = {
    'technology': '5G',
    'data_type': 'text',
    'channel_code': 'Polar',
    'modulation': 'QPSK',
    'channel_model': 'AWGN',
    'snr_db': 8.0,
    'mode': 'SSCC'
}

# Datos
data = np.random.randint(0, 2, 5000)

# Simular
sim = CommunicationSimulator(config)
results = sim.run_simulation(data)

# Resultados
print(f"BER: {results['metrics']['ber']:.6f}")
print(f"Entropía: {results['metrics']['entropy']:.4f}")
```

Ejecutar:
```bash
python test_custom.py
```

### Modo Debug

Agregar logging detallado:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

sim = CommunicationSimulator(config)
# Verás logs detallados de cada etapa
```

### Profiling de Rendimiento

Para identificar cuellos de botella:
```bash
# Instalar
pip install line_profiler memory_profiler

# Usar
python -m cProfile -o profile.stats main.py

# Analizar
python -m pstats profile.stats
>>> sort time
>>> stats 10
```

---

## Testing y Validación

### Estructura de Tests

Crear `tests/test_simulator.py`:
```python
import pytest
import numpy as np
from src.simulator import CommunicationSimulator, create_default_config

def test_simulator_initialization():
    """Test que el simulador se inicializa correctamente"""
    config = create_default_config()
    sim = CommunicationSimulator(config)
    assert sim.config['technology'] == '5G'

def test_basic_simulation():
    """Test simulación básica extremo a extremo"""
    config = create_default_config()
    config['snr_db'] = 20.0  # Alto SNR para BER bajo
    
    sim = CommunicationSimulator(config)
    data = np.random.randint(0, 2, 1000)
    results = sim.run_simulation(data)
    
    # Verificar que retorna resultados
    assert 'metrics' in results
    assert 'ber' in results['metrics']
    
    # A SNR alto, BER debe ser bajo
    assert results['metrics']['ber'] < 0.1

def test_invalid_configuration():
    """Test que configuración inválida lanza error"""
    config = {
        'technology': '5G',
        'modulation': '1024QAM',  # No válido para 5G
        'channel_code': 'LDPC',
        'data_type': 'text',
        'channel_model': 'AWGN',
        'snr_db': 10.0
    }
    
    with pytest.raises(ValueError):
        sim = CommunicationSimulator(config)
```

### Ejecutar Tests

```bash
# Instalar pytest
pip install pytest pytest-cov

# Ejecutar todos los tests
pytest tests/

# Con cobertura
pytest --cov=src tests/

# Test específico
pytest tests/test_simulator.py::test_basic_simulation

# Verbose
pytest -v tests/
```

### Tests de Integración

```python
def test_end_to_end_text_transmission():
    """Test transmisión completa de texto"""
    config = {
        'technology': '5G',
        'data_type': 'text',
        'channel_code': 'Polar',
        'modulation': 'QPSK',
        'channel_model': 'AWGN',
        'snr_db': 15.0,
        'mode': 'SSCC'
    }
    
    message = "TEST MESSAGE"
    bits = np.unpackbits(np.array([ord(c) for c in message], dtype=np.uint8))
    
    sim = CommunicationSimulator(config)
    results = sim.run_simulation(bits)
    
    # Verificar métricas razonables
    assert results['metrics']['ber'] < 0.01
    assert 'entropy' in results['metrics']
```

### Validación contra Teoría

```python
def test_ber_theoretical_comparison():
    """Comparar BER simulado con teórico"""
    from src.channel.models import calculate_ber_theoretical_awgn
    from src.modulation.modulators import create_modulator, calculate_ebn0_from_snr
    from src.channel.models import AWGNChannel
    
    snr_db = 10.0
    n_bits = 100000
    
    # BER teórico
    ebn0_db = calculate_ebn0_from_snr(snr_db, code_rate=1.0, bits_per_symbol=2)
    ber_theory = calculate_ber_theoretical_awgn(ebn0_db, 'QPSK')
    
    # BER simulado
    modulator = create_modulator('QPSK')
    channel = AWGNChannel(snr_db)
    
    bits = np.random.randint(0, 2, n_bits)
    symbols = modulator.modulate(bits)
    received = channel.transmit(symbols)
    llrs = modulator.demodulate(received, channel.get_noise_variance())
    decoded = (llrs < 0).astype(np.uint8)[:n_bits]
    
    ber_sim = np.sum(bits != decoded) / n_bits
    
    # Deben estar cerca (dentro de 20% por varianza Monte Carlo)
    assert abs(ber_sim - ber_theory) / ber_theory < 0.2
```

---

## Extensión del Simulador

### Agregar Nuevo Modulador

**Paso 1**: Crear clase heredando de `Modulator`:
```python
# En src/modulation/modulators.py

class OFDMModulator(Modulator):
    """Modulador OFDM"""
    
    def __init__(self, n_subcarriers=64, cp_length=16):
        self.n_subcarriers = n_subcarriers
        self.cp_length = cp_length
        self.bits_per_symbol = 2  # Ejemplo con QPSK por subportadora
    
    def modulate(self, bits):
        # 1. Modular cada subportadora (ej: QPSK)
        qpsk_symbols = self._qpsk_modulate(bits)
        
        # 2. Agrupar en bloques OFDM
        ofdm_blocks = qpsk_symbols.reshape(-1, self.n_subcarriers)
        
        # 3. IFFT
        time_domain = np.fft.ifft(ofdm_blocks, axis=1)
        
        # 4. Agregar prefijo cíclico
        cp = time_domain[:, -self.cp_length:]
        ofdm_symbols = np.hstack([cp, time_domain])
        
        return ofdm_symbols.flatten()
    
    def demodulate(self, symbols, noise_var):
        # Implementar demodulación OFDM
        pass
    
    def get_constellation(self):
        # Retornar constelación de subportadora
        return self._qpsk_constellation()
```

**Paso 2**: Actualizar factory:
```python
def create_modulator(scheme: str) -> Modulator:
    if scheme == 'QPSK':
        return QPSKModulator()
    elif scheme == 'OFDM':
        return OFDMModulator()
    # ... otros
```

**Paso 3**: Agregar tests:
```python
def test_ofdm_modulator():
    mod = OFDMModulator(n_subcarriers=64)
    bits = np.random.randint(0, 2, 1000)
    symbols = mod.modulate(bits)
    assert len(symbols) > 0
```

### Agregar Nuevo Canal

**Ejemplo**: Canal con interferencia

```python
# En src/channel/models.py

class InterferenceChannel(Channel):
    """Canal con interferencia de usuarios múltiples"""
    
    def __init__(self, snr_db, sir_db=10.0):
        """
        Args:
            snr_db: SNR deseado
            sir_db: Signal-to-Interference Ratio
        """
        self.snr_db = snr_db
        self.sir_db = sir_db
        self.snr_linear = 10 ** (snr_db / 10)
        self.sir_linear = 10 ** (sir_db / 10)
    
    def transmit(self, signal):
        # Señal interferente
        interference_power = np.mean(np.abs(signal)**2) / self.sir_linear
        interference = np.sqrt(interference_power / 2) * (
            np.random.randn(len(signal)) + 
            1j * np.random.randn(len(signal))
        )
        
        # Ruido térmico
        noise_power = np.mean(np.abs(signal)**2) / self.snr_linear
        noise = np.sqrt(noise_power / 2) * (
            np.random.randn(len(signal)) + 
            1j * np.random.randn(len(signal))
        )
        
        return signal + interference + noise
    
    def get_noise_variance(self):
        # Varianza efectiva (ruido + interferencia)
        return 1 / self.snr_linear + 1 / self.sir_linear
```

**Usar**:
```python
channel = InterferenceChannel(snr_db=15, sir_db=10)
received = channel.transmit(symbols)
```

### Agregar Nueva Métrica

**Ejemplo**: Delay spread

```python
# En src/metrics/performance.py

def calculate_delay_spread(channel_impulse_response):
    """
    Calcula delay spread RMS del canal.
    
    Args:
        channel_impulse_response: Respuesta impulsiva del canal
    
    Returns:
        Delay spread en segundos
    """
    h = np.abs(channel_impulse_response)
    power = h ** 2
    power_norm = power / np.sum(power)
    
    # Delay promedio
    delays = np.arange(len(h))
    mean_delay = np.sum(delays * power_norm)
    
    # RMS delay spread
    delay_spread = np.sqrt(
        np.sum((delays - mean_delay)**2 * power_norm)
    )
    
    return delay_spread

# Agregar a MetricsCalculator
class MetricsCalculator:
    def calculate_all_metrics(self, ...):
        # ... métricas existentes
        
        if 'channel_ir' in additional_data:
            metrics['delay_spread'] = calculate_delay_spread(
                additional_data['channel_ir']
            )
```

### Agregar Visualización Nueva

**Ejemplo**: Diagrama ojo (eye diagram)

```python
# En src/visualization/plots.py

class SimulatorVisualizer:
    def plot_eye_diagram(
        self,
        signal: np.ndarray,
        samples_per_symbol: int = 8,
        filename: str = "eye_diagram.png"
    ):
        """
        Dibuja diagrama de ojo.
        
        Args:
            signal: Señal en el tiempo
            samples_per_symbol: Muestras por símbolo
            filename: Nombre del archivo
        """
        # Reshape en trazas de 2 símbolos
        n_traces = len(signal) // (2 * samples_per_symbol)
        traces = signal[:n_traces * 2 * samples_per_symbol].reshape(
            n_traces, 2 * samples_per_symbol
        )
        
        plt.figure(figsize=(10, 6))
        
        # Dibujar todas las trazas superpuestas
        for trace in traces:
            if np.iscomplexobj(trace):
                plt.plot(trace.real, alpha=0.1, color='blue')
            else:
                plt.plot(trace, alpha=0.1, color='blue')
        
        plt.xlabel('Samples')
        plt.ylabel('Amplitude')
        plt.title('Eye Diagram')
        plt.grid(True)
        
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        plt.close()
```

---

## Contribución al Proyecto

### Workflow de Contribución

1. **Fork** el repositorio
2. **Clone** tu fork localmente
3. **Crear** branch para tu feature
4. **Implementar** cambios con tests
5. **Commit** con mensajes descriptivos
6. **Push** a tu fork
7. **Pull Request** al repositorio principal

### Estándares de Código

**PEP 8**: Seguir guía de estilo de Python
```bash
# Instalar linter
pip install pylint black

# Formatear código
black src/

# Verificar estilo
pylint src/
```

**Docstrings**: Documentar todas las funciones
```python
def my_function(param1: int, param2: str) -> bool:
    """
    Descripción breve de la función.
    
    Descripción más detallada si es necesaria.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
    
    Returns:
        Descripción del valor de retorno
    
    Raises:
        ValueError: Cuándo se lanza esta excepción
    
    Example:
        >>> my_function(5, "test")
        True
    """
    # Implementación
    pass
```

**Type Hints**: Usar anotaciones de tipo
```python
from typing import List, Dict, Optional, Tuple

def process_data(
    data: np.ndarray,
    config: Dict[str, Any]
) -> Tuple[np.ndarray, Dict[str, float]]:
    pass
```

### Proceso de Review

Pull requests son revisados por:
- **Correctitud**: ¿El código hace lo que dice?
- **Tests**: ¿Hay tests adecuados?
- **Documentación**: ¿Está documentado?
- **Estilo**: ¿Sigue PEP 8?
- **Performance**: ¿Es eficiente?

---

## Debugging y Troubleshooting

### Debugging Común

**Problema**: Dimensiones incompatibles
```python
# Agregar asserts para verificar
def modulate(self, bits):
    assert len(bits) % self.bits_per_symbol == 0, \
        f"Bits length {len(bits)} not divisible by {self.bits_per_symbol}"
    # ... resto del código
```

**Problema**: Valores NaN o Inf
```python
# Verificar antes de calcular
if noise_var < 1e-10:
    logging.warning("Noise variance too small, clipping")
    noise_var = 1e-10

llr = (min_d1 - min_d0) / noise_var
assert not np.isnan(llr).any(), "LLRs contain NaN"
```

**Problema**: BER siempre 0.5 (aleatorio)
```python
# Verificar que modulación y demodulación sean consistentes
print(f"Sent bits: {bits[:10]}")
print(f"Received LLRs: {llrs[:10]}")
print(f"Decoded bits: {decoded[:10]}")

# Verificar constelación
plt.scatter(symbols.real, symbols.imag)
plt.title("Sent constellation")
plt.savefig("debug_constellation.png")
```

### Herramientas de Debug

**IPython debugger**:
```python
# Agregar breakpoint
import ipdb; ipdb.set_trace()

# O usar built-in (Python 3.7+)
breakpoint()
```

**Logging estratégico**:
```python
logging.debug(f"Shape antes: {data.shape}")
data = process(data)
logging.debug(f"Shape después: {data.shape}")
logging.debug(f"Min: {data.min()}, Max: {data.max()}")
```

### Optimización

**Profiling**:
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Código a perfilar
sim.run_simulation(data)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

**NumPy Vectorization**:
```python
# Lento (loop Python)
result = []
for i in range(len(data)):
    result.append(data[i] ** 2)

# Rápido (vectorizado)
result = data ** 2
```

---

## Recursos Adicionales

### Referencias de Implementación

- **CommPy**: https://github.com/veeresht/CommPy
- **SciPy Signal**: https://docs.scipy.org/doc/scipy/reference/signal.html
- **GNU Radio**: https://www.gnuradio.org/

### Papers Relevantes

1. "5G NR: The Next Generation Wireless Access Technology"
2. "Deep Learning for Joint Source-Channel Coding"
3. "Polar Codes: Characterization of Exponent, Bounds, and Constructions"
4. "LDPC Codes: An Introduction"

### Tutoriales Online

- 3GPP Specifications: https://www.3gpp.org/specifications
- Wireless Pi: https://wirelesspi.com/
- Math works 5G Toolbox: https://www.mathworks.com/products/5g.html

---

**Versión**: 1.0  
**Última actualización**: 2025-10-29  
**Mantenedor**: Proyecto Simulador 5G/6G

Para preguntas técnicas, consultar `job.md` para estado del proyecto o abrir un issue en GitHub.
