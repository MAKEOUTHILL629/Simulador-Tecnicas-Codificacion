# Historial de Trabajo del Proyecto - Simulador de Cadena de Comunicación Digital

**Fecha**: 2025-10-29  
**Agente**: Copilot Agent  
**Estado del Proyecto**: Fase Inicial - Análisis y Planificación

---

## 1. ¿Qué se ha hecho?

### 1.1. Análisis del Proyecto
- ✅ **Lectura completa del README.md**: Se ha analizado en detalle la especificación técnica del proyecto que abarca 271 líneas de documentación exhaustiva.
- ✅ **Comprensión del alcance**: El proyecto requiere desarrollar un simulador web interactivo de comunicación digital que implemente:
  - Procesamiento de 4 tipos de fuentes (Texto, Imagen, Audio, Video simplificado)
  - Múltiples técnicas de codificación de fuente (Huffman, DCT/MDCT, Codificador Aprendido conceptual)
  - Codificación de canal 5G (LDPC y Códigos Polares)
  - Esquemas de modulación (QPSK, 16-QAM, 64-QAM, 256-QAM)
  - Canal AWGN con ruido configurable
  - Demodulación y decodificación completa
  - Visualizaciones detalladas con Plotly.js
  - Métricas de rendimiento (BER, SER, PSNR, SSIM, Entropía, Información Mutua, etc.)

### 1.2. Estado Actual del Repositorio
- ✅ **Evaluación del código existente**: Se ha confirmado que el repositorio actualmente contiene:
  - Documentación: README.md (especificación técnica completa)
  - Implementación: **NINGUNA** - No existen archivos HTML, JavaScript o CSS
  - Estado: Proyecto en fase de planificación, sin código implementado

---

## 2. ¿Qué falta por hacer?

### 2.1. Estructura Base del Proyecto (Prioridad: CRÍTICA)
- [ ] Crear la estructura de archivos y carpetas del proyecto
  - [ ] `index.html` - Archivo principal HTML5
  - [ ] `css/styles.css` - Estilos del simulador
  - [ ] `js/main.js` - Lógica principal y coordinación
  - [ ] `js/source-generators.js` - Generación de datos de fuente
  - [ ] `js/source-coding.js` - Algoritmos de codificación de fuente
  - [ ] `js/channel-coding.js` - Códigos LDPC y Polares
  - [ ] `js/modulation.js` - Esquemas de modulación
  - [ ] `js/channel.js` - Modelo de canal AWGN
  - [ ] `js/demodulation.js` - Demoduladores duro y suave
  - [ ] `js/metrics.js` - Cálculo de métricas de rendimiento
  - [ ] `js/visualization.js` - Funciones de visualización con Plotly.js
  - [ ] `js/info-theory.js` - Cálculos de teoría de la información
  - [ ] `assets/` - Carpeta para recursos (imágenes de muestra, audio, etc.)

### 2.2. Interfaz de Usuario (Prioridad: ALTA)
- [ ] **Layout de tres columnas** según especificación:
  - [ ] Columna Izquierda: Panel de control con parámetros configurables
  - [ ] Columna Central: Pipeline de visualización vertical con 8 etapas
  - [ ] Columna Derecha: Análisis y resultados
- [ ] **Panel de Control** con controles para:
  - [ ] Selector de tipo de fuente (Texto/Imagen/Audio/Video)
  - [ ] Selector de algoritmo de codificación de fuente
  - [ ] Selector de código de canal (LDPC/Polar) con tasa configurable
  - [ ] Selector de esquema de modulación
  - [ ] Input numérico para SNR o Eb/N0
  - [ ] Botón "Ejecutar Simulación"

### 2.3. Módulos de Procesamiento (Prioridad: ALTA)

#### 2.3.1. Generación de Fuentes
- [ ] **Texto**: 
  - [ ] Input textarea para texto personalizado
  - [ ] Botón de carga de texto de muestra
  - [ ] Conversión a binario con TextEncoder (UTF-8)
- [ ] **Imagen**:
  - [ ] Input file para carga de imágenes PNG/JPEG
  - [ ] Imágenes de muestra (Lena, Baboon)
  - [ ] Extracción de datos con Canvas API
- [ ] **Audio**:
  - [ ] Input file para archivos WAV
  - [ ] Audio de muestra predeterminado
  - [ ] Decodificación con Web Audio API
- [ ] **Video** (simplificado):
  - [ ] Generación de video sintético (animación canvas)
  - [ ] O extracción de 10 fotogramas de video corto

#### 2.3.2. Codificación de Fuente
- [ ] **Huffman**:
  - [ ] Construcción del árbol de Huffman
  - [ ] Generación de tabla de códigos
  - [ ] Codificación y decodificación
- [ ] **DCT (Imagen/Video)**:
  - [ ] DCT 2D en bloques 8×8
  - [ ] Cuantificación con matriz configurable
  - [ ] Escaneo en zigzag
  - [ ] Codificación de entropía
- [ ] **MDCT (Audio)**:
  - [ ] Implementación de MDCT con ventanas superpuestas
  - [ ] Cuantificación de coeficientes
  - [ ] Codificación de entropía
- [ ] **Codificador Aprendido (6G conceptual)**:
  - [ ] Definir arquitectura de autoencoder CNN
  - [ ] Pesos predefinidos estáticos
  - [ ] Cuantificación del espacio latente
  - [ ] Serialización a binario

#### 2.3.3. Codificación de Canal
- [ ] **LDPC (Low-Density Parity-Check)**:
  - [ ] Implementar codificador QC-LDPC
  - [ ] Definir grafo base y factor de expansión
  - [ ] Construcción de matriz H
  - [ ] Decodificador Belief Propagation (Suma-Producto)
  - [ ] Trabajar con LLRs
  - [ ] Máximo de iteraciones configurable
- [ ] **Códigos Polares**:
  - [ ] Implementar codificador Polar
  - [ ] Construcción de matriz generadora
  - [ ] CA-Polar con CRC prepuesto
  - [ ] Decodificador SCL (Successive Cancellation List)
  - [ ] Tamaño de lista L configurable (4 u 8)
  - [ ] Selección de ruta con verificación CRC

#### 2.3.4. Modulación
- [ ] Implementar mapeadores para:
  - [ ] QPSK (k=2 bits/símbolo)
  - [ ] 16-QAM (k=4 bits/símbolo)
  - [ ] 64-QAM (k=6 bits/símbolo)
  - [ ] 256-QAM (k=8 bits/símbolo)
- [ ] Normalización de potencia unitaria
- [ ] Generación de constelaciones

#### 2.3.5. Canal AWGN
- [ ] Implementar modelo de canal con ruido gaussiano complejo
- [ ] Cálculo de varianza del ruido desde SNR o Eb/N0
- [ ] Relaciones: SNR = 1/(2σ²) y Eb/N0 = SNR/(k·Rc)

#### 2.3.6. Demodulación
- [ ] **Demodulador de Decisión Dura**:
  - [ ] Detector de distancia euclidiana mínima
- [ ] **Demodulador de Decisión Suave**:
  - [ ] Cálculo de LLR con aproximación max-log
  - [ ] Fórmula: LLR(bi) ≈ (1/2σ²)[min(|y-s|²) para s∈S0 - min(|y-s|²) para s∈S1]

#### 2.3.7. Decodificación
- [ ] Decodificación de canal (LDPC/Polar desde LLRs)
- [ ] Decodificación de fuente (inversa de cada algoritmo)
  - [ ] Decodificador Huffman
  - [ ] IDCT/IMDCT
  - [ ] Decodificador del autoencoder

### 2.4. Visualizaciones (Prioridad: ALTA)
- [ ] Integrar Plotly.js
- [ ] Implementar visualizaciones para cada etapa:
  - [ ] **Entrada**: Mostrar texto/imagen/forma de onda
  - [ ] **Datos Codificados**: Primeros N bits y longitud total
  - [ ] **Señal Modulada**: Diagrama de constelación I/Q
  - [ ] **Salida del Canal**: Símbolos ruidosos sobre constelación ideal
  - [ ] **Demodulador**: Histograma de LLRs
  - [ ] **Salida Final**: Comparación lado a lado con entrada

### 2.5. Métricas de Rendimiento (Prioridad: MEDIA)
- [ ] **BER y SER**: Comparación bit a bit y símbolo a símbolo
- [ ] **PSNR**: Para imágenes/video con fórmula estándar
- [ ] **SSIM**: Índice de similitud estructural
- [ ] **SNR Segmental**: Para audio (proxy de calidad perceptual)
- [ ] **EVM**: Magnitud del Vector de Error
- [ ] **BLER/FER**: Tasa de error de bloque/trama
- [ ] **Distancia de Levenshtein**: Para texto

### 2.6. Teoría de la Información (Prioridad: MEDIA)
- [ ] Cálculo de **Entropía H(X)** y **H(Y)**:
  - [ ] Estimación desde histogramas
  - [ ] Fórmula: H(X) = -Σ p(x)·log₂(p(x))
- [ ] Cálculo de **Información Mutua I(X;Y)**:
  - [ ] Estimación de distribución conjunta p(x,y)
  - [ ] Fórmula: I(X;Y) = Σ p(x,y)·log₂(p(x,y)/(p(x)p(y)))

### 2.7. Optimización y Refinamiento (Prioridad: BAJA)
- [ ] Implementar funciones asíncronas (async/await) para procesamiento intensivo
- [ ] Garantizar UI receptiva durante cálculos
- [ ] Testing y validación de algoritmos
- [ ] Documentación de código
- [ ] Optimización de rendimiento

---

## 3. ¿Cómo se puede implementar?

### 3.1. Fase 1: Estructura Base y UI (Semana 1-2)

#### Paso 1.1: Crear estructura de archivos
```bash
# Estructura sugerida:
/
├── index.html
├── css/
│   └── styles.css
├── js/
│   ├── main.js
│   ├── source-generators.js
│   ├── source-coding.js
│   ├── channel-coding.js
│   ├── modulation.js
│   ├── channel.js
│   ├── demodulation.js
│   ├── metrics.js
│   ├── visualization.js
│   └── info-theory.js
├── assets/
│   ├── images/
│   │   ├── lena.png
│   │   └── baboon.png
│   └── audio/
│       └── sample.wav
└── README.md
```

#### Paso 1.2: HTML Base (index.html)
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulador de Cadena de Comunicación Digital</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div class="container">
        <!-- Columna Izquierda: Panel de Control -->
        <aside class="control-panel">
            <h2>Parámetros de Configuración</h2>
            <!-- Controles aquí -->
        </aside>
        
        <!-- Columna Central: Pipeline de Visualización -->
        <main class="visualization-pipeline">
            <h1>Simulador de Comunicación Digital</h1>
            <!-- 8 etapas de visualización -->
        </main>
        
        <!-- Columna Derecha: Resultados -->
        <aside class="results-panel">
            <h2>Análisis y Resultados</h2>
            <!-- Métricas y comparaciones -->
        </aside>
    </div>
    
    <!-- Scripts -->
    <script type="module" src="js/main.js"></script>
</body>
</html>
```

#### Paso 1.3: CSS Layout (styles.css)
```css
.container {
    display: grid;
    grid-template-columns: 300px 1fr 350px;
    gap: 20px;
    padding: 20px;
    height: 100vh;
}

.control-panel, .results-panel {
    overflow-y: auto;
    padding: 20px;
    background: #f5f5f5;
    border-radius: 8px;
}

.visualization-pipeline {
    overflow-y: auto;
    padding: 20px;
}
```

### 3.2. Fase 2: Generación de Fuentes (Semana 3)

#### Paso 2.1: Implementar generadores básicos
```javascript
// source-generators.js
export class SourceGenerator {
    static async generateText(text) {
        const encoder = new TextEncoder();
        const bytes = encoder.encode(text);
        return Array.from(bytes).map(byte => 
            byte.toString(2).padStart(8, '0')
        ).join('');
    }
    
    static async generateImage(file) {
        return new Promise((resolve) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                const imageData = ctx.getImageData(0, 0, img.width, img.height);
                resolve(imageData);
            };
            img.src = URL.createObjectURL(file);
        });
    }
    
    // ... más métodos para audio y video
}
```

### 3.3. Fase 3: Codificación de Fuente (Semana 4-5)

#### Paso 3.1: Huffman Coding
```javascript
// source-coding.js
export class HuffmanCoder {
    constructor(data) {
        this.buildTree(data);
    }
    
    buildTree(data) {
        // Calcular frecuencias
        const freq = {};
        for (const symbol of data) {
            freq[symbol] = (freq[symbol] || 0) + 1;
        }
        
        // Construir árbol
        // ... implementación del algoritmo
    }
    
    encode(data) {
        // Codificar usando la tabla
    }
    
    decode(encoded) {
        // Decodificar usando el árbol
    }
}
```

#### Paso 3.2: DCT para Imágenes
```javascript
export class DCTCoder {
    static encode(imageData, quality) {
        // Dividir en bloques 8x8
        // Aplicar DCT 2D
        // Cuantificar
        // Escaneo zigzag
        // Codificación Huffman
    }
    
    static decode(encoded) {
        // Proceso inverso
    }
}
```

### 3.4. Fase 4: Codificación de Canal (Semana 6-8)

#### Paso 4.1: LDPC
```javascript
// channel-coding.js
export class LDPCCoder {
    constructor(codeRate, blockLength) {
        this.codeRate = codeRate;
        this.blockLength = blockLength;
        this.buildParityCheckMatrix();
    }
    
    buildParityCheckMatrix() {
        // Construir matriz H basada en protograph
    }
    
    encode(data) {
        // Codificación sistemática
    }
    
    decode(llrs, maxIterations = 50) {
        // Belief Propagation (Suma-Producto)
        // Iterar hasta convergencia o maxIterations
    }
}
```

#### Paso 4.2: Códigos Polares
```javascript
export class PolarCoder {
    constructor(n, k) {
        this.n = n; // Longitud del código
        this.k = k; // Bits de información
        this.buildGenerator();
        this.constructFrozenBits();
    }
    
    encode(data) {
        // Añadir CRC
        // Codificación Polar
    }
    
    decodeSCL(llrs, listSize = 8) {
        // Successive Cancellation List
        // Verificación CRC para selección de ruta
    }
}
```

### 3.5. Fase 5: Modulación y Canal (Semana 9)

#### Paso 5.1: Moduladores
```javascript
// modulation.js
export class Modulator {
    static qpsk(bits) {
        // Mapear cada 2 bits a símbolo complejo
        const symbols = [];
        for (let i = 0; i < bits.length; i += 2) {
            const b1 = parseInt(bits[i]);
            const b2 = parseInt(bits[i + 1]);
            // Gray mapping
            symbols.push(this.qpskConstellation[b1 * 2 + b2]);
        }
        return symbols;
    }
    
    // Implementar 16-QAM, 64-QAM, 256-QAM
}
```

#### Paso 5.2: Canal AWGN
```javascript
// channel.js
export class AWGNChannel {
    static addNoise(symbols, snrDB) {
        const snr = Math.pow(10, snrDB / 10);
        const noiseVariance = 1 / (2 * snr);
        
        return symbols.map(s => ({
            real: s.real + this.gaussianRandom() * Math.sqrt(noiseVariance),
            imag: s.imag + this.gaussianRandom() * Math.sqrt(noiseVariance)
        }));
    }
    
    static gaussianRandom() {
        // Box-Muller transform
    }
}
```

### 3.6. Fase 6: Demodulación y Decodificación (Semana 10)

#### Paso 6.1: Demodulador Suave (LLR)
```javascript
// demodulation.js
export class Demodulator {
    static computeLLRs(receivedSymbols, constellation, noiseVariance) {
        const llrs = [];
        
        for (const y of receivedSymbols) {
            const bitsPerSymbol = Math.log2(constellation.length);
            
            for (let bitIdx = 0; bitIdx < bitsPerSymbol; bitIdx++) {
                // Aproximación max-log
                const llr = this.computeBitLLR(y, constellation, bitIdx, noiseVariance);
                llrs.push(llr);
            }
        }
        
        return llrs;
    }
    
    static computeBitLLR(y, constellation, bitIdx, noiseVariance) {
        // Implementar fórmula max-log
    }
}
```

### 3.7. Fase 7: Visualizaciones (Semana 11)

#### Paso 7.1: Plotly.js para diagramas
```javascript
// visualization.js
export class Visualizer {
    static plotConstellation(symbols, elementId) {
        const real = symbols.map(s => s.real);
        const imag = symbols.map(s => s.imag);
        
        const trace = {
            x: real,
            y: imag,
            mode: 'markers',
            type: 'scatter',
            marker: { size: 4 }
        };
        
        const layout = {
            title: 'Diagrama de Constelación',
            xaxis: { title: 'In-Phase (I)' },
            yaxis: { title: 'Quadrature (Q)' }
        };
        
        Plotly.newPlot(elementId, [trace], layout);
    }
    
    static plotLLRHistogram(llrs, elementId) {
        // Histograma de LLRs
    }
    
    // Más funciones de visualización
}
```

### 3.8. Fase 8: Métricas y Teoría de la Información (Semana 12)

#### Paso 8.1: Métricas básicas
```javascript
// metrics.js
export class Metrics {
    static calculateBER(transmitted, received) {
        let errors = 0;
        for (let i = 0; i < transmitted.length; i++) {
            if (transmitted[i] !== received[i]) errors++;
        }
        return errors / transmitted.length;
    }
    
    static calculatePSNR(original, reconstructed) {
        const mse = this.calculateMSE(original, reconstructed);
        if (mse === 0) return Infinity;
        const maxPixel = 255;
        return 10 * Math.log10((maxPixel * maxPixel) / mse);
    }
    
    static calculateSSIM(img1, img2) {
        // Implementar SSIM según fórmula
    }
}
```

#### Paso 8.2: Teoría de la información
```javascript
// info-theory.js
export class InformationTheory {
    static calculateEntropy(data) {
        const freq = {};
        for (const symbol of data) {
            freq[symbol] = (freq[symbol] || 0) + 1;
        }
        
        let entropy = 0;
        const total = data.length;
        
        for (const count of Object.values(freq)) {
            const p = count / total;
            if (p > 0) {
                entropy -= p * Math.log2(p);
            }
        }
        
        return entropy;
    }
    
    static calculateMutualInformation(X, Y) {
        // Construir histograma 2D para p(x,y)
        // Calcular I(X;Y)
    }
}
```

### 3.9. Fase 9: Integración y Coordinación (Semana 13)

#### Paso 9.1: Main.js - Orquestador
```javascript
// main.js
import { SourceGenerator } from './source-generators.js';
import { HuffmanCoder, DCTCoder } from './source-coding.js';
import { LDPCCoder, PolarCoder } from './channel-coding.js';
import { Modulator } from './modulation.js';
import { AWGNChannel } from './channel.js';
import { Demodulator } from './demodulation.js';
import { Metrics } from './metrics.js';
import { Visualizer } from './visualization.js';

class Simulator {
    async runSimulation() {
        // 1. Generar/cargar fuente
        const sourceData = await this.generateSource();
        
        // 2. Codificación de fuente
        const encodedSource = this.encodeSource(sourceData);
        
        // 3. Codificación de canal
        const encodedChannel = this.encodeChannel(encodedSource);
        
        // 4. Modulación
        const modulatedSignal = this.modulate(encodedChannel);
        
        // 5. Canal AWGN
        const receivedSignal = this.addChannelNoise(modulatedSignal);
        
        // 6. Demodulación
        const llrs = this.demodulate(receivedSignal);
        
        // 7. Decodificación de canal
        const decodedChannel = this.decodeChannel(llrs);
        
        // 8. Decodificación de fuente
        const reconstructed = this.decodeSource(decodedChannel);
        
        // 9. Calcular métricas
        this.calculateMetrics(sourceData, reconstructed);
        
        // 10. Actualizar visualizaciones
        this.updateVisualizations();
    }
}

// Inicializar simulador
const simulator = new Simulator();
document.getElementById('runButton').addEventListener('click', () => {
    simulator.runSimulation();
});
```

### 3.10. Recomendaciones de Implementación

#### Priorización
1. **Primera Iteración**: Implementar flujo completo con versiones simplificadas
   - Texto como fuente
   - Sin codificación de fuente (o solo Huffman)
   - LDPC simple
   - QPSK
   - Visualizaciones básicas

2. **Segunda Iteración**: Expandir funcionalidades
   - Agregar soporte para imágenes
   - Implementar DCT
   - Agregar más esquemas de modulación

3. **Tercera Iteración**: Completar todas las características
   - Audio y video
   - Códigos Polares
   - Todas las métricas
   - Codificador aprendido conceptual

#### Consideraciones Técnicas
- **Performance**: Usar Web Workers para cálculos intensivos si es necesario
- **Async/Await**: Mantener UI responsiva durante procesamiento
- **Modularidad**: Cada módulo debe ser independiente y testeable
- **Visualización**: Actualizar visualizaciones progresivamente, no todas a la vez

#### Testing
- Validar cada algoritmo por separado con casos conocidos
- Comparar BER con curvas teóricas
- Verificar que las transformadas inversas reconstruyen correctamente

---

## 4. Recursos Útiles

### 4.1. Librerías JavaScript Recomendadas
- **Plotly.js**: Visualizaciones (ya especificado en README)
- **Math.js**: Operaciones matemáticas avanzadas (opcional)
- **JSZip**: Si se necesita compresión adicional

### 4.2. Referencias de Algoritmos
- Códigos LDPC: Implementaciones de referencia en papers académicos
- Códigos Polares: 3GPP TS 38.212 especificaciones 5G
- DCT: Algoritmos de JPEG como referencia
- MDCT: Implementaciones de códecs de audio (AAC, Vorbis)

### 4.3. Datos de Prueba
- Imágenes: Lena, Baboon (dominio público)
- Audio: Clips de voz cortos (Creative Commons)
- Texto: Lorem ipsum o extractos literarios de dominio público

---

## 5. Notas Importantes

### 5.1. Filosofía del Proyecto
El README enfatiza la reconciliación entre:
- **SSCC (Separate Source-Channel Coding)**: Modelo tradicional implementado
- **JSCC/DeepJSCC**: Paradigma moderno de 6G representado conceptualmente

El simulador sigue SSCC por requisitos académicos, pero incorpora principios de 6G mediante el "Codificador Aprendido".

### 5.2. Alcance Académico
Este es un proyecto **educativo**. Los algoritmos deben ser:
- **Correctos** pero no necesariamente optimizados al máximo
- **Comprensibles** con código claro y bien estructurado
- **Visuales** para facilitar el aprendizaje

### 5.3. Limitaciones Conocidas
- Video: Modelo simplificado (no códec completo)
- LDPC/Polar: Implementaciones básicas, no optimizadas para producción
- Codificador Aprendido: Pesos estáticos, no entrenamiento en tiempo real

---

## 6. Próximos Pasos Inmediatos

1. **Crear estructura de archivos básica** (index.html, CSS, JS modules)
2. **Implementar UI con layout de tres columnas**
3. **Desarrollar generador de fuente de texto** (el más simple)
4. **Implementar codificador Huffman** (base para otros)
5. **Crear visualización básica de bits**
6. **Integrar Plotly.js** para primeras gráficas

Una vez que el flujo básico texto→bits→visualización funcione, expandir gradualmente a:
- Modulación simple (QPSK)
- Canal AWGN básico
- Demodulación y cálculo de BER
- Y así sucesivamente según las fases descritas

---

## 7. Conclusión

El proyecto es **ambicioso pero factible** si se aborda de manera incremental y modular. La especificación técnica en el README es excepcionalmente detallada y proporciona todas las fórmulas y algoritmos necesarios.

**Estimación de tiempo**: 12-16 semanas para implementación completa con una persona trabajando a tiempo completo.

**Complejidad**: Media-Alta (requiere conocimientos de teoría de la información, procesamiento de señales, codificación de canal, y desarrollo web).

**Resultado esperado**: Una herramienta educativa interactiva de alta calidad que demuestra principios fundamentales de comunicación digital desde las técnicas clásicas hasta conceptos de 6G.

---

*Documento creado el 2025-10-29 por el agente de análisis inicial del proyecto.*
