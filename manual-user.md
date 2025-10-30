# Manual de Usuario - Simulador de Sistemas de Comunicación 5G/6G

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Inicio Rápido](#inicio-rápido)
4. [Configuración del Simulador](#configuración-del-simulador)
5. [Parámetros de Entrada](#parámetros-de-entrada)
6. [Interpretación de Resultados](#interpretación-de-resultados)
7. [Métricas Explicadas](#métricas-explicadas)
8. [Interpretación de Gráficas](#interpretación-de-gráficas)
9. [Casos de Uso y Ejemplos](#casos-de-uso-y-ejemplos)
10. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

### ¿Qué es este simulador?

Este simulador modela sistemas de comunicación inalámbrica de las generaciones 5G y 6G. Permite:

- **Transmitir diferentes tipos de datos**: texto, audio, imagen y video
- **Comparar tecnologías**: 5G, 5G Advanced y 6G (exploratorio)
- **Evaluar rendimiento**: bajo diferentes condiciones de canal y configuraciones
- **Visualizar resultados**: mediante gráficas comparativas profesionales
- **Analizar trade-offs**: entre calidad, tasa de bits y robustez

### ¿Para quién es este simulador?

- Estudiantes de telecomunicaciones e ingeniería
- Investigadores en comunicaciones inalámbricas
- Profesionales evaluando diseños de sistemas
- Cualquier persona interesada en entender cómo funcionan las redes 5G/6G

---

## Instalación

### Requisitos Previos

- **Python 3.7 o superior**
- **pip** (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el repositorio:**
```bash
git clone https://github.com/MAKEOUTHILL629/Simulador-Tecnicas-Codificacion.git
cd Simulador-Tecnicas-Codificacion
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Verificar instalación:**
```bash
python main.py
```

Si todo está correcto, verás los ejemplos ejecutándose y gráficas generándose en `./plots/`.

---

## Inicio Rápido

### Ejecutar Ejemplos Predefinidos

El simulador incluye tres ejemplos listos para usar:

```bash
python main.py
```

Esto ejecutará:
1. **Ejemplo 1**: Transmisión de texto usando Polar codes y QPSK
2. **Ejemplo 2**: Comparación de BER para diferentes modulaciones
3. **Ejemplo 3**: Transmisión de imagen usando LDPC y 64-QAM

Las gráficas se guardarán en el directorio `./plots/`.

### Tu Primera Simulación Personalizada

Crea un archivo `mi_simulacion.py`:

```python
import numpy as np
from src.simulator import CommunicationSimulator

# Configurar el simulador
config = {
    'technology': '5G',
    'data_type': 'text',
    'channel_code': 'LDPC',
    'modulation': 'QPSK',
    'channel_model': 'AWGN',
    'snr_db': 10.0,
    'mode': 'SSCC'
}

# Crear simulador
sim = CommunicationSimulator(config)

# Datos de prueba
data = np.random.randint(0, 2, 1000)

# Ejecutar simulación
results = sim.run_simulation(data)

# Ver métricas
print("BER:", results['metrics']['ber'])
```

Ejecuta:
```bash
python mi_simulacion.py
```

---

## Configuración del Simulador

El simulador se configura mediante un diccionario Python con los siguientes parámetros:

### Configuración Básica

```python
config = {
    'technology': '5G',           # Tecnología a usar
    'data_type': 'text',          # Tipo de datos
    'channel_code': 'LDPC',       # Código de canal
    'modulation': 'QPSK',         # Esquema de modulación
    'channel_model': 'AWGN',      # Modelo de canal
    'snr_db': 10.0,               # SNR en dB
    'mode': 'SSCC'                # Modo de operación
}
```

---

## Parámetros de Entrada

### 1. Technology (Tecnología)

Determina qué opciones de codificación y modulación están disponibles.

| Valor | Descripción | Opciones Habilitadas |
|-------|-------------|---------------------|
| `'5G'` | 5G NR (New Radio) estándar | HEVC, EVS, LDPC, Polar, hasta 256-QAM |
| `'5G_Advanced'` | 5G Advanced (Release 17+) | VVC, IVAS, LDPC, Polar, hasta 256-QAM |
| `'6G'` | 6G exploratorio | VVC, IVAS, códigos novedosos, hasta 1024-QAM |

**Ejemplo:**
```python
config['technology'] = '5G_Advanced'
```

### 2. Data Type (Tipo de Datos)

Especifica el tipo de información a transmitir.

| Valor | Descripción | Codec de Fuente Recomendado |
|-------|-------------|----------------------------|
| `'text'` | Texto ASCII/UTF-8 | Huffman, Aritmético |
| `'audio'` | Señales de voz/música | EVS (5G), IVAS (5G-A/6G) |
| `'image'` | Imágenes estáticas | HEVC (5G), VVC (5G-A/6G) |
| `'video'` | Secuencias de video | HEVC (5G), VVC (5G-A/6G) |

**Ejemplo:**
```python
config['data_type'] = 'audio'
```

### 3. Channel Code (Código de Canal)

Esquema de codificación para protección contra errores.

| Valor | Descripción | Uso en 5G | Características |
|-------|-------------|-----------|----------------|
| `'LDPC'` | Low-Density Parity-Check | Canales de datos | Alto rendimiento, bloques grandes |
| `'Polar'` | Códigos Polares | Canales de control | Alcanza capacidad teórica, bloques cortos |

**Ejemplo:**
```python
config['channel_code'] = 'Polar'
```

**¿Cuándo usar cada uno?**
- **LDPC**: Para datos grandes (streaming, archivos)
- **Polar**: Para información de control, baja latencia

### 4. Modulation (Modulación)

Esquema de mapeo de bits a símbolos.

| Valor | Bits/Símbolo | Uso Típico | Robustez vs Eficiencia |
|-------|--------------|------------|----------------------|
| `'QPSK'` | 2 | Canales de baja calidad | Alta robustez, baja tasa |
| `'16QAM'` | 4 | Balance | Media robustez, media tasa |
| `'64QAM'` | 6 | Buenas condiciones | Menor robustez, alta tasa |
| `'256QAM'` | 8 | Excelentes condiciones | Baja robustez, muy alta tasa |
| `'1024QAM'` | 10 | 6G, condiciones óptimas | Muy baja robustez, máxima tasa |

**Ejemplo:**
```python
config['modulation'] = '64QAM'
```

**Regla práctica**: A mayor SNR, puedes usar modulaciones de orden superior.

### 5. Channel Model (Modelo de Canal)

Simula el medio de transmisión inalámbrico.

| Valor | Descripción | Cuándo Usarlo |
|-------|-------------|---------------|
| `'AWGN'` | Ruido Gaussiano Blanco Aditivo | Caso ideal, análisis teórico |
| `'Rayleigh'` | Desvanecimiento sin línea de vista | Entornos urbanos densos, NLOS |
| `'Rician'` | Desvanecimiento con línea de vista | Entornos rurales, LOS parcial |

**Ejemplo:**
```python
config['channel_model'] = 'Rayleigh'
```

**Características del canal:**
- **AWGN**: Solo ruido, sin desvanecimiento. Más fácil de analizar.
- **Rayleigh**: Variaciones de amplitud significativas. Realista para ciudades.
- **Rician**: Combina componente directa y difusa. Realista para exteriores.

### 6. SNR (Signal-to-Noise Ratio)

Relación entre potencia de señal y ruido en decibeles (dB).

| Rango SNR | Condiciones | Modulación Recomendada |
|-----------|-------------|----------------------|
| 0-5 dB | Muy malas | QPSK |
| 5-10 dB | Malas | QPSK, 16QAM |
| 10-15 dB | Regulares | 16QAM, 64QAM |
| 15-20 dB | Buenas | 64QAM, 256QAM |
| >20 dB | Excelentes | 256QAM, 1024QAM |

**Ejemplo:**
```python
config['snr_db'] = 12.0
```

**Nota**: SNR más alto = mejor calidad de canal = menor BER.

### 7. Mode (Modo de Operación)

| Valor | Descripción | Características |
|-------|-------------|----------------|
| `'SSCC'` | Separated Source-Channel Coding | Codificación tradicional, efecto acantilado |
| `'JSCC'` | Joint Source-Channel Coding | Degradación gradual (futuro) |

**Ejemplo:**
```python
config['mode'] = 'SSCC'
```

**Nota**: JSCC está en desarrollo. Actualmente use 'SSCC'.

---

## Interpretación de Resultados

### Estructura de Resultados

Cuando ejecutas una simulación, obtienes un diccionario con:

```python
results = {
    'reconstructed_data': array([...]),    # Datos reconstruidos
    'metrics': {                           # Métricas de rendimiento
        'ber': 0.0123,
        'psnr': 32.45,
        'ssim': 0.89,
        ...
    },
    'intermediate_states': {               # Estados intermedios
        'encoded_source': ...,
        'modulated_signal': ...,
        ...
    }
}
```

### Acceder a Resultados

```python
# Ver datos reconstruidos
reconstructed = results['reconstructed_data']

# Ver BER
ber = results['metrics']['ber']
print(f"BER: {ber:.6f}")

# Ver señal modulada
symbols = results['intermediate_states']['modulated_signal']
```

---

## Métricas Explicadas

### 1. BER (Bit Error Rate)

**Qué mide**: Proporción de bits erróneos respecto al total.

**Fórmula**: BER = (Bits erróneos) / (Total de bits)

**Rango**: 0 (perfecto) a 0.5 (aleatorio)

**Interpretación**:
- BER < 10⁻⁶: Excelente (calidad broadcast)
- BER < 10⁻³: Bueno (comunicaciones de voz)
- BER < 10⁻²: Aceptable (con corrección de errores adicional)
- BER > 10⁻¹: Inaceptable

**Ejemplo**:
```
BER = 0.001 = 10⁻³
Significa: 1 error cada 1000 bits
```

### 2. Entropía (H)

**Qué mide**: Contenido promedio de información en bits por símbolo.

**Fórmula**: H(X) = -Σ p(x) log₂(p(x))

**Rango**: 0 (determinista) a log₂(M) donde M es el tamaño del alfabeto

**Interpretación**:
- Entropía alta: Mucha información, difícil de comprimir
- Entropía baja: Redundante, fácil de comprimir

**Ejemplo**:
```
H = 4.2 bits/símbolo
Significa: Cada símbolo porta en promedio 4.2 bits de información
```

### 3. Información Mutua (I)

**Qué mide**: Información compartida entre entrada y salida.

**Fórmula**: I(X;Y) = H(X) - H(X|Y)

**Rango**: 0 (sin información transferida) a H(X) (transferencia perfecta)

**Interpretación**:
- I = H(X): Canal perfecto
- I < H(X): Pérdida de información
- I = 0: No se transmitió información

**Ejemplo**:
```
I = 3.8 bits
Si H(X) = 4.0, se transfirió el 95% de la información
```

### 4. PSNR (Peak Signal-to-Noise Ratio)

**Qué mide**: Calidad de reconstrucción de imagen/video.

**Fórmula**: PSNR = 10 log₁₀(MAX²/MSE)

**Rango**: Típicamente 20-50 dB (mayor es mejor)

**Interpretación**:
- PSNR > 40 dB: Excelente calidad, visualmente idéntico
- PSNR 30-40 dB: Buena calidad, pérdidas imperceptibles
- PSNR 20-30 dB: Calidad aceptable, artefactos visibles
- PSNR < 20 dB: Mala calidad

**Ejemplo**:
```
PSNR = 35 dB
Calidad buena, adecuada para streaming
```

### 5. SSIM (Structural Similarity Index)

**Qué mide**: Similitud estructural perceptual.

**Fórmula**: Compara luminancia, contraste y estructura

**Rango**: -1 a 1 (típicamente 0 a 1)

**Interpretación**:
- SSIM > 0.95: Excelente, casi idéntico
- SSIM 0.9-0.95: Muy bueno
- SSIM 0.8-0.9: Bueno
- SSIM < 0.8: Degradación visible

**Ventaja sobre PSNR**: Correlaciona mejor con percepción humana.

**Ejemplo**:
```
SSIM = 0.92
Alta similitud estructural, calidad perceptual muy buena
```

### 6. MSE (Mean Squared Error)

**Qué mide**: Error cuadrático promedio.

**Fórmula**: MSE = (1/N) Σ(original - reconstruido)²

**Rango**: 0 (perfecto) a ∞

**Interpretación**:
- MSE = 0: Reconstrucción perfecta
- MSE bajo: Buena reconstrucción
- MSE alto: Mala reconstrucción

**Relación con PSNR**: PSNR = 10 log₁₀(MAX²/MSE)

---

## Interpretación de Gráficas

### 1. Diagrama de Constelación

**Qué muestra**: Símbolos modulados en el plano complejo (I/Q).

**Cómo leerlo**:
- **Eje X (I)**: Componente en fase
- **Eje Y (Q)**: Componente en cuadratura
- **Puntos agrupados**: Símbolos transmitidos
- **Dispersión**: Efecto del ruido

**Ejemplo**: ![Constelación](ejemplo_constellation.png)

**Interpretación**:
- **Puntos bien definidos**: Alto SNR, buen canal
- **Puntos dispersos**: Bajo SNR, canal ruidoso
- **Forma**: QPSK (4 puntos), 16-QAM (16 puntos), etc.

### 2. BER vs Eb/N0

**Qué muestra**: Rendimiento del sistema en función de la relación señal-ruido.

**Ejes**:
- **X**: Eb/N0 (energía por bit a densidad de ruido) en dB
- **Y**: BER (escala logarítmica)

**Cómo leerlo**:
- **Pendiente**: Qué tan rápido mejora el sistema con mejor SNR
- **Comparación**: Líneas más abajo = mejor rendimiento

**Ejemplo**:
```
A 10 dB Eb/N0:
- QPSK: BER = 10⁻⁴
- 16QAM: BER = 10⁻³
- 64QAM: BER = 10⁻²

Conclusión: QPSK es más robusto a bajo SNR
```

**Curva típica**: Cascada (waterfall curve)
- Zona de error alto (< umbral SNR)
- Transición rápida
- Zona de error bajo (> umbral SNR)

### 3. Calidad vs SNR (PSNR/SSIM vs SNR)

**Qué muestra**: Calidad de reconstrucción según condiciones de canal.

**Característica clave**: Efecto acantilado (cliff effect)

**Cómo leerlo**:

**SSCC (Separated Source-Channel Coding)**:
- Calidad alta hasta SNR umbral
- Caída abrupta (cliff) en el umbral
- Calidad muy baja después

**JSCC (Joint Source-Channel Coding)**:
- Degradación gradual (graceful degradation)
- Calidad disminuye suavemente
- Siempre recupera algo de información

**Ejemplo**:
```
SSCC a 15 dB: PSNR = 40 dB (excelente)
SSCC a 12 dB: PSNR = 15 dB (mala) ← cliff effect
JSCC a 12 dB: PSNR = 25 dB (aceptable) ← graceful
```

### 4. Curvas Tasa-Distorsión

**Qué muestra**: Trade-off entre bitrate y calidad.

**Ejes**:
- **X**: Tasa de bits (kbps o Mbps)
- **Y**: Distorsión (MSE) o calidad (PSNR)

**Cómo leerlo**:
- Curva más arriba/izquierda = mejor codec
- Punto óptimo depende de requisitos

**Ejemplo**:
```
VVC a 2 Mbps: PSNR = 38 dB
HEVC a 2 Mbps: PSNR = 35 dB

Conclusión: VVC es 50% más eficiente
```

### 5. Información Mutua vs SNR

**Qué muestra**: Capacidad efectiva del canal.

**Ejes**:
- **X**: SNR del canal (dB)
- **Y**: Información mutua (bits)

**Cómo leerlo**:
- Curva creciente con SNR
- Saturación cerca de H(X) (entropía de la fuente)
- Comparar con capacidad de Shannon

**Interpretación**:
```
SNR = 5 dB: I = 2 bits (canal limitado)
SNR = 20 dB: I = 4 bits (cerca de capacidad)
```

### 6. Forma de Onda I/Q

**Qué muestra**: Señal modulada en el dominio del tiempo.

**Componentes**:
- **I (In-Phase)**: Parte real
- **Q (Quadrature)**: Parte imaginaria

**Cómo leerlo**:
- Variaciones rápidas = modulación de orden alto
- Amplitud constante = modulación de fase (QPSK)
- Amplitud variable = QAM

### 7. Espectrograma (Audio)

**Qué muestra**: Contenido frecuencial en el tiempo.

**Ejes**:
- **X**: Tiempo (s)
- **Y**: Frecuencia (Hz)
- **Color**: Intensidad (dB)

**Cómo leerlo**:
- Patrones horizontales: Tonos puros
- Bandas verticales: Transientes
- Áreas blancas: Alta energía
- Áreas oscuras: Baja energía

---

## Casos de Uso y Ejemplos

### Caso 1: Transmisión de Mensaje de Texto en Entorno Ruidoso

**Objetivo**: Transmitir "HELLO WORLD" con alta confiabilidad en canal ruidoso (SNR bajo).

**Configuración óptima**:
```python
config = {
    'technology': '5G',
    'data_type': 'text',
    'channel_code': 'Polar',      # Excelente para bloques cortos
    'modulation': 'QPSK',          # Máxima robustez
    'channel_model': 'AWGN',
    'snr_db': 5.0,                 # Canal ruidoso
    'mode': 'SSCC'
}
```

**Ejecución**:
```python
import numpy as np
from src.simulator import CommunicationSimulator

sim = CommunicationSimulator(config)
message = "HELLO WORLD"
bits = np.unpackbits(np.array([ord(c) for c in message], dtype=np.uint8))
results = sim.run_simulation(bits)

print(f"BER: {results['metrics']['ber']}")
# Esperado: BER < 10⁻³
```

**Por qué esta configuración**:
- Polar: Óptimo para datos de control/mensajes cortos
- QPSK: 2 bits/símbolo, mayor espacio entre símbolos, más robusto
- SNR 5 dB: Suficiente para QPSK con FEC

### Caso 2: Streaming de Video 4K en Buenas Condiciones

**Objetivo**: Transmitir video 4K con alta calidad y eficiencia espectral.

**Configuración óptima**:
```python
config = {
    'technology': '5G_Advanced',
    'data_type': 'video',
    'channel_code': 'LDPC',        # Alto rendimiento para datos grandes
    'modulation': '256QAM',        # Alta eficiencia espectral
    'channel_model': 'Rician',     # LOS parcial (típico en celdas)
    'snr_db': 18.0,                # Buenas condiciones
    'mode': 'SSCC'
}
```

**Ejecución**:
```python
# Simular frames de video 4K
video_data = np.random.randint(0, 256, (100, 3840, 2160), dtype=np.uint8)

sim = CommunicationSimulator(config)
results = sim.run_simulation(video_data.flatten())

print(f"PSNR: {results['metrics'].get('psnr', 0)} dB")
# Esperado: PSNR > 35 dB
```

**Por qué esta configuración**:
- 5G Advanced: Soporta VVC, más eficiente que HEVC
- LDPC: Diseñado para bloques grandes de datos
- 256-QAM: 8 bits/símbolo, alta tasa de datos
- SNR 18 dB: Necesario para 256-QAM

### Caso 3: VoIP en Movimiento (Rayleigh)

**Objetivo**: Llamada de voz clara en automóvil en ciudad.

**Configuración óptima**:
```python
config = {
    'technology': '5G',
    'data_type': 'audio',
    'channel_code': 'Polar',       # Baja latencia
    'modulation': '16QAM',         # Balance entre tasa y robustez
    'channel_model': 'Rayleigh',   # Entorno urbano, NLOS
    'snr_db': 10.0,                # Condiciones moderadas
    'mode': 'SSCC'
}
```

**Ejecución**:
```python
# Simular 1 segundo de voz a 16 kHz
sample_rate = 16000
audio_data = np.random.randn(sample_rate)

sim = CommunicationSimulator(config)
results = sim.run_simulation(audio_data)

print(f"SNR: {results['metrics'].get('snr', 0)} dB")
# Esperado: SNR > 15 dB para voz clara
```

**Por qué esta configuración**:
- EVS codec: Optimizado para voz
- Polar: Latencia ultra-baja (<1 ms)
- 16-QAM: Suficiente tasa para voz comprimida
- Rayleigh: Realista para ciudad con desvanecimiento

### Caso 4: Comparar Diferentes Modulaciones

**Objetivo**: Determinar la mejor modulación para tu escenario.

**Código**:
```python
from src.modulation.modulators import create_modulator
from src.channel.models import create_channel
import numpy as np

snr_values = np.arange(0, 20, 2)
modulations = ['QPSK', '16QAM', '64QAM', '256QAM']

results = {}
for mod in modulations:
    ber_values = []
    for snr in snr_values:
        modulator = create_modulator(mod)
        channel = create_channel('AWGN', snr)
        
        bits = np.random.randint(0, 2, 10000)
        symbols = modulator.modulate(bits)
        received = channel.transmit(symbols)
        llrs = modulator.demodulate(received, channel.get_noise_variance())
        decoded = (llrs < 0).astype(np.uint8)[:len(bits)]
        
        ber = np.sum(bits != decoded) / len(bits)
        ber_values.append(ber)
    
    results[mod] = (snr_values, ber_values)

# Visualizar
from src.visualization.plots import SimulatorVisualizer
viz = SimulatorVisualizer()
viz.plot_ber_vs_ebn0(results, "modulation_comparison.png")
```

**Interpretación**:
- A bajo SNR (<10 dB): QPSK gana
- A medio SNR (10-15 dB): 16/64-QAM balance óptimo
- A alto SNR (>15 dB): 256-QAM máxima eficiencia

### Caso 5: Evaluar Efecto de Canal (AWGN vs Rayleigh)

**Objetivo**: Comparar rendimiento en canal ideal vs realista.

**Código**:
```python
config_base = {
    'technology': '5G',
    'data_type': 'text',
    'channel_code': 'LDPC',
    'modulation': '64QAM',
    'snr_db': 15.0,
    'mode': 'SSCC'
}

channels = ['AWGN', 'Rayleigh', 'Rician']
results = {}

for channel_type in channels:
    config = config_base.copy()
    config['channel_model'] = channel_type
    
    sim = CommunicationSimulator(config)
    data = np.random.randint(0, 2, 5000)
    result = sim.run_simulation(data)
    
    results[channel_type] = result['metrics']['ber']
    print(f"{channel_type}: BER = {results[channel_type]:.6f}")

# Esperado:
# AWGN < Rician < Rayleigh (BER)
```

### Caso 6: Optimizar Tasa de Código

**Objetivo**: Encontrar la mejor tasa de código (trade-off redundancia vs tasa).

**Código**:
```python
from src.channel_coding.codes import LDPCEncoder
import numpy as np

code_rates = [1/3, 1/2, 2/3, 3/4, 5/6]
snr_db = 8.0

for rate in code_rates:
    encoder = LDPCEncoder(code_rate=rate, block_size=1024)
    
    # Simular transmisión
    data = np.random.randint(0, 2, encoder.k * 10)
    encoded = encoder.encode(data)
    
    overhead = len(encoded) / len(data)
    print(f"Rate {rate:.3f}: Overhead = {overhead:.2f}x")

# Interpretación:
# Rate = 1/3: Máxima protección, 3x overhead
# Rate = 5/6: Mínima protección, 1.2x overhead
# Rate = 1/2: Balance común
```

---

## Solución de Problemas

### Problema 1: Error al importar módulos

**Síntoma**:
```
ModuleNotFoundError: No module named 'src'
```

**Solución**:
```bash
# Asegúrate de ejecutar desde el directorio raíz
cd /ruta/a/Simulador-Tecnicas-Codificacion
python main.py

# O agrega el directorio al PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Problema 2: Gráficas no se generan

**Síntoma**: No hay archivos en `./plots/`

**Solución**:
```python
# Verificar que matplotlib esté instalado
pip install matplotlib

# Verificar permisos del directorio
import os
os.makedirs('./plots', exist_ok=True)
```

### Problema 3: BER siempre 0 o 0.5

**Síntoma**: BER no realista

**Posibles causas**:
1. **BER = 0**: SNR demasiado alto o datos muy cortos
   - Reducir SNR o aumentar longitud de datos
2. **BER = 0.5**: Sistema no funciona, decisiones aleatorias
   - Revisar configuración, verificar compatibilidad de parámetros

### Problema 4: Simulación muy lenta

**Síntoma**: Toma mucho tiempo ejecutar

**Soluciones**:
```python
# Reducir tamaño de datos
data = np.random.randint(0, 2, 1000)  # En vez de 100000

# Usar bloques más pequeños
encoder = LDPCEncoder(code_rate=0.5, block_size=256)  # En vez de 1024

# Reducir número de puntos en gráficas
snr_range = np.arange(0, 20, 5)  # En vez de np.arange(0, 20, 0.5)
```

### Problema 5: Valores de PSNR infinitos

**Síntoma**: `PSNR = inf`

**Causa**: Imágenes idénticas (MSE = 0)

**Solución**: Normal para datos de prueba simples. Usar datos reales o añadir ruido.

### Problema 6: Configuración inválida

**Síntoma**:
```
ValueError: Modulación 1024QAM no válida para tecnología 5G
```

**Solución**: Verificar tabla de compatibilidad:
```python
# 1024-QAM solo en 6G
config['technology'] = '6G'
config['modulation'] = '1024QAM'

# O usar modulación compatible con 5G
config['technology'] = '5G'
config['modulation'] = '256QAM'  # Máximo para 5G
```

---

## Consejos Prácticos

### 1. Empezar Simple
Comienza con configuraciones básicas:
- QPSK
- AWGN
- SNR moderado (10 dB)

### 2. Variar Un Parámetro a la Vez
Para entender efectos individuales.

### 3. Guardar Configuraciones
```python
import json

# Guardar
with open('mi_config.json', 'w') as f:
    json.dump(config, f, indent=2)

# Cargar
with open('mi_config.json', 'r') as f:
    config = json.load(f)
```

### 4. Comparar con Teoría
Usar curvas teóricas para validar:
```python
from src.channel.models import calculate_ber_theoretical_awgn

ber_theoretical = calculate_ber_theoretical_awgn(ebn0_db=10, modulation='QPSK')
```

### 5. Experimentar
El simulador es una herramienta de aprendizaje. ¡Prueba configuraciones extremas!

---

## Glosario

- **5G NR**: 5G New Radio, estándar actual
- **AWGN**: Additive White Gaussian Noise, ruido blanco gaussiano
- **BER**: Bit Error Rate, tasa de error de bit
- **Eb/N0**: Energía por bit sobre densidad espectral de ruido
- **FEC**: Forward Error Correction, corrección de errores
- **JSCC**: Joint Source-Channel Coding, codificación conjunta
- **LDPC**: Low-Density Parity-Check, código de paridad de baja densidad
- **LLR**: Log-Likelihood Ratio, razón de verosimilitud logarítmica
- **LOS**: Line of Sight, línea de vista
- **NLOS**: Non-Line of Sight, sin línea de vista
- **PSNR**: Peak Signal-to-Noise Ratio, relación señal-ruido de pico
- **QAM**: Quadrature Amplitude Modulation, modulación de amplitud en cuadratura
- **QPSK**: Quadrature Phase Shift Keying, modulación por desplazamiento de fase en cuadratura
- **SNR**: Signal-to-Noise Ratio, relación señal-ruido
- **SSCC**: Separated Source-Channel Coding, codificación separada
- **SSIM**: Structural Similarity Index, índice de similitud estructural

---

## Recursos Adicionales

### Documentación Relacionada
- `README.md`: Especificación técnica completa
- `manual-dev.md`: Guía para desarrolladores
- `job.md`: Estado del proyecto

### Referencias Teóricas
- Shannon, C. E. (1948). "A Mathematical Theory of Communication"
- 3GPP TS 38.212: 5G NR Channel coding
- ITU-T Recommendations: P.862 (PESQ), P.863 (POLQA)

### Soporte
Para preguntas o problemas, consultar la documentación técnica o crear un issue en el repositorio.

---

**Versión del Manual**: 1.0  
**Última actualización**: 2025-10-29  
**Compatibilidad**: Python 3.7+, Simulador v0.1.0
