# Inicio Rápido - Simulador 5G/6G

## Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/MAKEOUTHILL629/Simulador-Tecnicas-Codificacion.git
cd Simulador-Tecnicas-Codificacion

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar ejemplos
python main.py
```

## Uso Básico

```python
from src.simulator import CommunicationSimulator
import numpy as np

# Configurar simulador
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

# Ejecutar
results = sim.run_simulation(data)

# Ver resultados
print(f"BER: {results['metrics']['ber']:.6f}")
```

## Estructura del Proyecto

```
Simulador-Tecnicas-Codificacion/
├── README.md              # Especificación completa
├── QUICKSTART.md          # Este archivo
├── job.md                 # Estado del proyecto
├── manual-user.md         # Manual de usuario
├── manual-dev.md          # Manual de desarrollador
├── main.py                # Script con ejemplos
├── requirements.txt       # Dependencias
├── src/                   # Código fuente
│   ├── simulator.py       # Simulador principal
│   ├── source_coding/     # Codificación de fuente
│   ├── channel_coding/    # Códigos LDPC/Polar
│   ├── modulation/        # QPSK, QAM
│   ├── channel/           # Modelos de canal
│   ├── metrics/           # BER, PSNR, SSIM, etc.
│   └── visualization/     # Gráficas
└── plots/                 # Gráficas generadas
```

## Documentación

- **Para Usuarios**: Leer `manual-user.md`
  - Cómo usar el simulador
  - Configuraciones disponibles
  - Interpretación de resultados
  - Ejemplos de casos de uso

- **Para Desarrolladores**: Leer `manual-dev.md`
  - Arquitectura del sistema
  - Cómo ejecutar localmente
  - Cómo extender funcionalidades
  - Guía de contribución

- **Estado del Proyecto**: Ver `job.md`
  - Qué está implementado
  - Qué falta por hacer
  - Roadmap futuro

## Ejemplos Incluidos

El script `main.py` incluye tres ejemplos:

1. **Transmisión de texto**: "HELLO WORLD" con Polar codes y QPSK
2. **Comparación de modulaciones**: BER vs SNR para QPSK, 16QAM, 64QAM
3. **Transmisión de imagen**: Usando LDPC y 64QAM

## Características Principales

✅ **Codificación de Fuente**
- Huffman, Aritmético (texto)
- HEVC, VVC (video)
- EVS, IVAS (audio)

✅ **Codificación de Canal**
- LDPC (canales de datos)
- Polar (canales de control)

✅ **Modulación**
- QPSK, 16-QAM, 64-QAM, 256-QAM, 1024-QAM

✅ **Modelos de Canal**
- AWGN (ideal)
- Rayleigh (NLOS)
- Rician (LOS)

✅ **Métricas**
- BER, SER
- Entropía, Información Mutua
- PSNR, SSIM, MSE

✅ **Visualizaciones**
- Diagramas de constelación
- Curvas BER vs Eb/N0
- Calidad vs SNR
- Formas de onda

## Tecnologías Soportadas

| Tecnología | Códecs de Fuente | Códigos de Canal | Modulación |
|------------|------------------|------------------|------------|
| **5G** | HEVC, EVS | LDPC, Polar | Hasta 256-QAM |
| **5G Advanced** | VVC, IVAS | LDPC, Polar | Hasta 256-QAM |
| **6G** | VVC, IVAS, AI-based | LDPC, Polar, Novel | Hasta 1024-QAM |

## Requisitos

- Python 3.7+
- NumPy >= 1.21.0
- SciPy >= 1.7.0
- Matplotlib >= 3.4.0
- Seaborn >= 0.11.0

## Soporte

Para preguntas o problemas:
1. Consultar documentación en `manual-user.md` o `manual-dev.md`
2. Revisar ejemplos en `main.py`
3. Ver estado del proyecto en `job.md`

## Licencia

[Especificar licencia del proyecto]

## Contacto

[Información de contacto del proyecto]
