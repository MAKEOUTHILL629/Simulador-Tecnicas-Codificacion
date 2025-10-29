# Manual de Usuario - Simulador de Cadena de Comunicación Digital

**Versión**: 1.0  
**Última actualización**: 2025-10-29

---

## 1. Introducción

Bienvenido al Simulador de Cadena de Comunicación Digital. Esta herramienta educativa interactiva permite visualizar y analizar el proceso completo de transmisión de información (texto, imagen, audio, video) a través de un canal ruidoso, implementando técnicas de codificación y modulación utilizadas en sistemas de comunicación modernos (5G/6G).

### 1.1. Propósito del Simulador

El simulador modela el flujo completo de una cadena de comunicación digital:
```
Fuente → Codificación de Fuente → Codificación de Canal → Modulación → 
Canal AWGN → Demodulación → Decodificación de Canal → Decodificación de Fuente → Salida
```

### 1.2. Usuarios Objetivo

- Estudiantes de ingeniería de telecomunicaciones
- Investigadores en teoría de la información
- Profesionales que desean comprender sistemas 5G/6G
- Educadores que necesitan herramientas de demostración interactivas

---

## 2. Interfaz del Usuario

### 2.1. Diseño General

La interfaz está organizada en **tres columnas**:

#### **Columna Izquierda: Panel de Control**
Aquí se configuran todos los parámetros de la simulación:
- Tipo de fuente de datos
- Algoritmos de codificación
- Parámetros del canal
- Esquemas de modulación

#### **Columna Central: Pipeline de Visualización**
Muestra el procesamiento paso a paso de la señal en 8 etapas:
1. Entrada Original
2. Datos Codificados de Fuente
3. Datos Codificados de Canal
4. Señal Modulada
5. Salida del Canal (con ruido)
6. Señal Demodulada
7. Datos Decodificados
8. Salida Final Reconstruida

#### **Columna Derecha: Análisis y Resultados**
Presenta métricas de rendimiento y comparaciones:
- Salida reconstruida vs. entrada original
- Métricas cuantitativas (BER, PSNR, etc.)
- Cálculos de teoría de la información

---

## 3. Guía de Uso Paso a Paso

### 3.1. Selección de Fuente de Datos

#### **Opción 1: Texto**
1. Seleccione "Texto" en el menú de tipo de fuente
2. Escriba su texto en el área de texto o use el botón "Cargar Texto de Muestra"
3. El texto se convertirá automáticamente a binario usando codificación UTF-8

**Consideraciones:**
- Textos más largos demoran más en procesarse
- Caracteres especiales y emojis están soportados
- Recomendado: 50-500 caracteres para visualización óptima

#### **Opción 2: Imagen**
1. Seleccione "Imagen" en el menú
2. Haga clic en "Cargar Imagen" y seleccione un archivo PNG o JPEG
3. O use las imágenes de muestra predefinidas (Lena, Baboon)

**Consideraciones:**
- Tamaño recomendado: 256×256 a 512×512 píxeles
- Imágenes más grandes requieren más tiempo de procesamiento
- Formatos soportados: PNG, JPEG
- Las imágenes se procesan en formato RGB

#### **Opción 3: Audio**
1. Seleccione "Audio" en el menú
2. Cargue un archivo WAV o use el audio de muestra
3. El audio se decodificará usando Web Audio API

**Consideraciones:**
- Formato: WAV (PCM)
- Duración recomendada: 1-5 segundos
- Frecuencia de muestreo: 44.1 kHz o menor
- Mono o estéreo soportado

#### **Opción 4: Video (Simplificado)**
1. Seleccione "Video" en el menú
2. Use la animación sintética predefinida (cuadrado en movimiento)
3. O cargue un video corto (primeros 10 fotogramas)

**Consideraciones:**
- Se procesan solo 10 fotogramas
- Resolución recomendada: 128×128 píxeles
- Este es un modelo simplificado para demostración educativa

### 3.2. Configuración de Codificación de Fuente

La codificación de fuente reduce la redundancia de los datos originales.

#### **Ninguno**
- Sin compresión
- Útil para ver el efecto de otros componentes sin compresión

#### **Huffman**
- Codificación de entropía clásica
- Reduce tamaño basándose en frecuencia de símbolos
- **Cuándo usar**: Para datos con distribución no uniforme (texto)
- **Resultado esperado**: Reducción de 10-40% en tamaño

#### **Basado en DCT** (para Imagen/Video)
- Transformada de Coseno Discreta
- Modela códecs como JPEG, HEVC
- **Parámetro**: Factor de Calidad (1-100)
  - **100**: Máxima calidad, mínima compresión
  - **50**: Balance entre calidad y compresión
  - **10**: Máxima compresión, calidad reducida
- **Resultado esperado**: Compresión 5:1 a 20:1 dependiendo del factor

#### **Basado en MDCT** (para Audio)
- Transformada de Coseno Discreta Modificada
- Modela códecs como AAC, Vorbis
- **Parámetro**: Tasa de bits
- **Resultado esperado**: Compresión de 5:1 a 12:1

#### **Codificador Aprendido** (Concepto 6G)
- Simula un autoencoder neuronal
- Representa paradigma de codificación conjunta fuente-canal
- **Cuándo usar**: Para explorar conceptos avanzados de 6G
- **Nota**: Los pesos son estáticos (no se entrena en tiempo real)

### 3.3. Configuración de Codificación de Canal

La codificación de canal añade redundancia para proteger contra errores.

#### **Ninguno**
- Sin protección contra errores
- Útil para ver el impacto del ruido sin corrección

#### **LDPC (Low-Density Parity-Check)**
- Estándar 5G para canales de datos
- Rendimiento cercano a la capacidad de Shannon
- **Tasas disponibles**: 1/2, 2/3, 3/4
  - **1/2**: Máxima protección, menor velocidad de datos
  - **3/4**: Menor protección, mayor velocidad de datos
- **Cuándo usar**: Para SNR medio a alto (>5 dB)

#### **Polar**
- Estándar 5G para canales de control
- Excelente rendimiento en bloques cortos
- **Tasas disponibles**: 1/2, 2/3, 3/4
- **Cuándo usar**: Para bloques de datos pequeños o SNR bajo

### 3.4. Configuración de Modulación

La modulación mapea bits a símbolos complejos para transmisión.

| Esquema | Bits/Símbolo | Robustez | Velocidad | Uso Recomendado |
|---------|--------------|----------|-----------|-----------------|
| **QPSK** | 2 | Alta | Baja | SNR < 10 dB |
| **16-QAM** | 4 | Media | Media | SNR 10-15 dB |
| **64-QAM** | 6 | Baja | Alta | SNR 15-20 dB |
| **256-QAM** | 8 | Muy Baja | Muy Alta | SNR > 20 dB |

**Principio**: Mayor orden de modulación = más bits por símbolo = mayor velocidad pero más susceptible al ruido

### 3.5. Configuración del Canal

#### **SNR (Signal-to-Noise Ratio)**
- Mide la relación entre potencia de señal y potencia de ruido
- **Rango típico**: -5 dB a 30 dB
- **Interpretación**:
  - **< 0 dB**: Ruido más fuerte que la señal (condiciones muy malas)
  - **5-10 dB**: Comunicación básica posible
  - **15-20 dB**: Buena calidad de comunicación
  - **> 25 dB**: Excelente calidad, casi sin errores

#### **Eb/N0 (Energy per Bit to Noise)**
- Métrica normalizada independiente de la modulación
- **Rango típico**: 0 dB a 15 dB
- **Relación**: Eb/N0 = SNR / (log₂(M) × Rc)
  - M = orden de modulación
  - Rc = tasa de código

### 3.6. Ejecutar la Simulación

1. Configure todos los parámetros deseados
2. Haga clic en el botón **"Ejecutar Simulación"**
3. La interfaz se actualizará mostrando:
   - Visualizaciones en cada etapa del pipeline
   - Métricas de rendimiento en la columna derecha
4. La simulación es **asíncrona** - la interfaz permanece responsive

**Tiempo de procesamiento típico**:
- Texto: 0.5-2 segundos
- Imagen: 2-10 segundos
- Audio: 3-8 segundos
- Video: 10-30 segundos

---

## 4. Interpretación de Resultados

### 4.1. Visualizaciones

#### **Diagrama de Constelación (Pre-Canal)**
- Muestra símbolos modulados ideales
- **Interpretación**: Puntos perfectamente espaciados en el plano I/Q

#### **Diagrama de Constelación (Post-Canal)**
- Muestra símbolos recibidos con ruido
- **Interpretación**:
  - Dispersión pequeña alrededor de puntos ideales = bajo ruido
  - Gran dispersión = alto ruido, más errores esperados
  - Nube que solapa con símbolos adyacentes = alta probabilidad de error

#### **Histograma de LLR**
- Muestra la confianza de las decisiones suaves del demodulador
- **Interpretación**:
  - Valores altos (positivos/negativos) = alta confianza
  - Valores cerca de 0 = baja confianza (bit incierto)
  - Distribución bimodal = buena separación

#### **Comparación Entrada vs. Salida**
- Visualización lado a lado del original y reconstruido
- **Para texto**: Comparación carácter por carácter
- **Para imagen**: Comparación visual de calidad
- **Para audio**: Forma de onda temporal

### 4.2. Métricas de Rendimiento

#### **BER (Bit Error Rate)**
- **Definición**: Proporción de bits erróneos
- **Rango**: 0 (sin errores) a 1 (todos erróneos)
- **Interpretación**:
  - **< 10⁻⁶**: Excelente (prácticamente sin errores)
  - **10⁻⁴ a 10⁻³**: Aceptable para voz
  - **10⁻² a 10⁻¹**: Mala calidad, errores visibles
  - **> 0.1**: Comunicación severamente degradada

#### **SER (Symbol Error Rate)**
- Similar a BER pero a nivel de símbolo
- **Relación aproximada**: BER ≈ SER / log₂(M) para SNR alto con Gray coding

#### **PSNR (Peak Signal-to-Noise Ratio)** - Para Imagen/Video
- **Definición**: Mide calidad de reconstrucción en dB
- **Interpretación**:
  - **> 40 dB**: Excelente calidad (errores imperceptibles)
  - **30-40 dB**: Buena calidad
  - **20-30 dB**: Calidad aceptable (errores visibles)
  - **< 20 dB**: Mala calidad (degradación severa)

#### **SSIM (Structural Similarity Index)** - Para Imagen/Video
- **Definición**: Métrica perceptual de similitud estructural
- **Rango**: 0 (completamente diferente) a 1 (idéntico)
- **Interpretación**:
  - **> 0.95**: Perceptualmente idéntico
  - **0.90-0.95**: Muy similar
  - **0.80-0.90**: Similar
  - **< 0.80**: Diferencias notables

#### **SNR Segmental** - Para Audio
- **Definición**: SNR promediado sobre tramas cortas
- **Interpretación**: Similar a SNR pero más representativo de percepción auditiva

#### **EVM (Error Vector Magnitude)**
- **Definición**: Calidad de la modulación (%)
- **Interpretación**:
  - **< 3%**: Excelente
  - **3-8%**: Buena
  - **> 8%**: Requiere atención

#### **BLER (Block Error Rate)**
- **Definición**: Tasa de bloques con al menos un error
- **Uso**: Métrica práctica para retransmisiones

#### **Distancia de Levenshtein** - Para Texto
- **Definición**: Número de ediciones (inserción/eliminación/sustitución) necesarias
- **Interpretación**: 0 = texto idéntico, valores altos = texto muy diferente

### 4.3. Métricas de Teoría de la Información

#### **Entropía H(X)**
- **Definición**: Contenido de información promedio (bits/símbolo)
- **Interpretación**:
  - Entropía alta = fuente muy aleatoria, difícil de comprimir
  - Entropía baja = fuente predecible, fácil de comprimir
- **Máximo teórico**: log₂(|alfabeto|)

#### **Información Mutua I(X;Y)**
- **Definición**: Información compartida entre entrada y salida
- **Interpretación**:
  - I(X;Y) ≈ H(X) = comunicación casi perfecta
  - I(X;Y) << H(X) = pérdida significativa de información
  - I(X;Y) / H(X) = eficiencia de transmisión

### 4.4. ¿Cómo Saber si los Resultados son Correctos?

#### **Para Simulación de Texto (sin codificación, SNR alto)**

**Configuración típica de prueba**: Texto "Hola mundo", sin codificación de fuente, sin codificación de canal, QPSK, SNR = 15 dB

**Resultados esperados buenos** ✅:
- **BER**: 0.00e+0 o muy cerca de 0 (10⁻⁶ o menor)
- **SER**: 0.00e+0 o muy cerca de 0
- **Errores de bits**: 0 de X bits (donde X depende del texto)
- **H(X) Entropía Entrada**: ~1.000 bits/símbolo (para bits binarios equiprobables)
- **H(Y) Entropía Salida**: ~1.000 bits/símbolo (debe ser similar a entrada)
- **I(X;Y) Info. Mutua**: ~1.000 bits/símbolo (debe ser igual a H(X) si no hay errores)
- **C Capacidad (Shannon)**: Valor que depende del SNR
  - Para SNR = 15 dB: C ≈ 5.0 bits/canal use
  - Para SNR = 20 dB: C ≈ 6.7 bits/canal use
- **Texto Reconstruido**: Debe ser **idéntico** al original
- **Distancia de Levenshtein**: 0 (sin diferencias)

#### **Indicadores de problemas** ❌:
- BER > 0.01 con SNR alto (>15 dB) y modulación simple (QPSK)
- Texto reconstruido diferente al original con configuración conservadora
- Entropía de salida H(Y) significativamente mayor que H(X) (señal de ruido excesivo)
- Información Mutua I(X;Y) < 0.5 × H(X) (pérdida severa de información)

#### **Rangos típicos según condiciones**

| SNR (dB) | Modulación | Código Canal | BER Esperado | Calidad |
|----------|-----------|-------------|--------------|---------|
| 20+ | QPSK | LDPC/Polar | < 10⁻⁶ | Excelente |
| 15-20 | 16-QAM | LDPC/Polar | 10⁻⁵ - 10⁻⁴ | Muy buena |
| 10-15 | QPSK | LDPC | 10⁻⁴ - 10⁻³ | Buena |
| 5-10 | QPSK | Ninguno | 10⁻² - 10⁻¹ | Aceptable |
| < 5 | Cualquiera | Cualquiera | > 10⁻¹ | Mala |

#### **Relación entre métricas (valores típicos)**
- **Con SNR = 15 dB, QPSK, LDPC 1/2**: BER ≈ 10⁻⁵, I(X;Y) ≈ 0.99 × H(X)
- **Con SNR = 10 dB, 16-QAM, sin código**: BER ≈ 10⁻³, I(X;Y) ≈ 0.95 × H(X)
- **Con SNR = 5 dB, cualquiera, sin código**: BER ≈ 10⁻², I(X;Y) ≈ 0.80 × H(X)

#### **Validación rápida de resultados**
1. ✅ **Test básico**: Con SNR ≥ 15 dB y QPSK, el texto debe reconstruirse perfectamente
2. ✅ **Test de ruido**: Disminuir SNR debe aumentar BER de forma exponencial
3. ✅ **Test de código**: Agregar LDPC debe mejorar BER en ~3-6 dB
4. ✅ **Test de modulación**: Mayor orden (256-QAM) debe tener peor BER que QPSK al mismo SNR

---

## 5. Casos de Uso y Experimentos Sugeridos

### 5.1. Experimento 1: Efecto del Ruido

**Objetivo**: Observar cómo el ruido degrada la comunicación

**Pasos**:
1. Configure: Texto, Sin codificación de fuente, Sin codificación de canal, QPSK
2. Ejecute con SNR = 20 dB (observe BER, casi sin errores)
3. Ejecute con SNR = 10 dB (observe incremento en BER)
4. Ejecute con SNR = 0 dB (observe degradación severa)

**Observación esperada**: Relación exponencial entre SNR y BER

### 5.2. Experimento 2: Beneficio de la Codificación de Canal

**Objetivo**: Demostrar ganancia de codificación

**Pasos**:
1. Configure: Imagen, DCT (calidad 70), Sin codificación de canal, 16-QAM, SNR = 10 dB
2. Anote el PSNR obtenido
3. Repita con LDPC (tasa 1/2)
4. Compare los resultados

**Observación esperada**: LDPC proporciona ~3-6 dB de ganancia (mejor PSNR a mismo SNR)

### 5.3. Experimento 3: Compromiso Modulación

**Objetivo**: Entender el trade-off velocidad vs. robustez

**Pasos**:
1. Configure: Texto, Huffman, Polar (2/3), SNR = 15 dB
2. Pruebe con QPSK, 16-QAM, 64-QAM, 256-QAM
3. Compare BER para cada esquema

**Observación esperada**: 
- QPSK: Menor BER pero más símbolos transmitidos
- 256-QAM: Menor número de símbolos pero mayor BER

### 5.4. Experimento 4: Capacidad del Canal

**Objetivo**: Explorar el límite de Shannon

**Pasos**:
1. Configure varios SNR y modulaciones
2. Calcule tasa de información mutua I(X;Y)
3. Compare con capacidad teórica: C = log₂(1 + SNR)

**Observación esperada**: I(X;Y) se aproxima pero no excede C

### 5.5. Experimento 5: Compresión vs. Calidad

**Objetivo**: Analizar trade-off en codificación de fuente

**Pasos**:
1. Configure: Imagen, DCT, calidad 90, resto óptimo
2. Observe tamaño de datos codificados y PSNR
3. Repita con calidad 50, 20
4. Grafique relación tamaño vs. PSNR

**Observación esperada**: Curva de compresión típica (rodilla alrededor de calidad 60-70)

---

## 6. Consideraciones Técnicas

### 6.1. Limitaciones del Simulador

#### **Rendimiento**
- El simulador corre en el navegador (JavaScript)
- Procesamiento intensivo puede ser lento en dispositivos móviles
- Recomendado: Computadora de escritorio con navegador moderno

#### **Modelo Simplificado**
- Video: Solo 10 fotogramas, no es un códec completo
- Codificador Aprendido: Pesos estáticos, no hay entrenamiento
- Canal: Solo AWGN (no desvanecimiento, no interferencia multi-trayecto)

#### **Exactitud Numérica**
- Precisión de punto flotante de JavaScript (64 bits)
- Algoritmos iterativos tienen límite de iteraciones
- Pequeñas diferencias con implementaciones de referencia son normales

### 6.2. Requisitos del Sistema

#### **Navegador**
- Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- JavaScript habilitado
- No requiere instalación de plugins

#### **Hardware**
- RAM: Mínimo 4 GB (8 GB recomendado)
- CPU: Procesador dual-core o superior
- Pantalla: Resolución mínima 1280×720

#### **Conectividad**
- No requiere conexión a internet después de cargar la página
- Plotly.js se carga desde CDN (requiere internet inicial)

### 6.3. Solución de Problemas

#### **La simulación es muy lenta**
- **Solución**: Reduzca el tamaño de los datos de entrada
- Use imágenes más pequeñas (< 256×256)
- Use textos más cortos (< 200 caracteres)
- Cierre otras pestañas del navegador

#### **Errores al cargar archivos**
- **Solución**: Verifique el formato del archivo
- Imágenes: Solo PNG/JPEG
- Audio: Solo WAV
- Verifique el tamaño del archivo (< 5 MB)

#### **Visualizaciones no se muestran**
- **Solución**: Verifique la consola del navegador (F12)
- Recargue la página
- Verifique conexión a internet (para cargar Plotly.js)

#### **Resultados inesperados**
- **Solución**: Verifique que los parámetros sean compatibles
- Algunas combinaciones pueden no ser óptimas
- Revise las sugerencias de "Cuándo usar" para cada parámetro

---

## 7. Interpretación Pedagógica

### 7.1. Conceptos Clave Demostrados

#### **Separación Fuente-Canal (Teorema de Shannon)**
El simulador implementa arquitectura SSCC donde:
- Codificación de fuente elimina redundancia (compresión)
- Codificación de canal añade redundancia controlada (protección)
- Estos procesos son independientes

**Observación**: Funciona bien en la práctica, pero JSCC (6G) puede superar en casos de bloque finito

#### **Compromiso Velocidad-Confiabilidad**
En todos los niveles:
- **Modulación**: Más bits/símbolo = más velocidad pero más errores
- **Codificación de Canal**: Más protección = menos errores pero menor tasa efectiva
- **Codificación de Fuente**: Más compresión = archivos pequeños pero menor calidad

#### **Capacidad de Canal**
La información mutua I(X;Y) nunca excede la capacidad de Shannon:
```
C = B × log₂(1 + SNR)
```
donde B es el ancho de banda (normalizado a 1 en este simulador)

#### **Decisiones Duras vs. Suaves**
Los decodificadores modernos usan LLRs (decisión suave) que proporcionan ~2-3 dB de ganancia sobre decisión dura.

### 7.2. Conexión con Sistemas Reales

#### **5G New Radio (NR)**
- LDPC: Usado en eMBB (Enhanced Mobile Broadband)
- Polar: Usado en canales de control
- 256-QAM: Soportado en condiciones favorables
- Arquitectura similar a este simulador

#### **6G (Futuro)**
- Codificación Conjunta Fuente-Canal (JSCC)
- Deep Learning en la capa física (DeepJSCC)
- El "Codificador Aprendido" representa este concepto

---

## 8. Recursos Adicionales

### 8.1. Referencias Teóricas

1. **Teoría de la Información**: "Elements of Information Theory" - Cover & Thomas
2. **Comunicaciones Digitales**: "Digital Communications" - Proakis & Salehi
3. **Codificación de Canal**: "Error Control Coding" - Lin & Costello
4. **5G**: 3GPP TS 38.211-214 (especificaciones NR PHY)

### 8.2. Para Profundizar

- **LDPC**: "Modern Coding Theory" - Richardson & Urbanke
- **Polar Codes**: Papers de Erdal Arıkan (inventor)
- **DeepJSCC**: "Deep Joint Source-Channel Coding" - Bourtsoulatze et al.
- **Procesamiento de Señales**: "Digital Signal Processing" - Oppenheim & Schafer

### 8.3. Tutoriales en Línea

- Khan Academy: Teoría de la Información
- MIT OCW: Digital Communication Systems
- Coursera: Wireless Communications (Stanford)

---

## 9. Glosario de Términos

| Término | Definición |
|---------|------------|
| **AWGN** | Additive White Gaussian Noise - Modelo de ruido térmico |
| **BER** | Bit Error Rate - Tasa de error de bit |
| **Codificación de Canal** | Añade redundancia para proteger contra errores |
| **Codificación de Fuente** | Elimina redundancia para comprimir datos |
| **Constelación** | Conjunto de puntos en el plano complejo (símbolos) |
| **DCT** | Discrete Cosine Transform - Base de JPEG/MPEG |
| **Eb/N0** | Energy per Bit to Noise Density - Métrica normalizada |
| **Gray Coding** | Mapeo donde símbolos adyacentes difieren en 1 bit |
| **JSCC** | Joint Source-Channel Coding - Codificación conjunta |
| **LDPC** | Low-Density Parity-Check - Código de canal 5G |
| **LLR** | Log-Likelihood Ratio - Información suave de bits |
| **MDCT** | Modified DCT - Usada en códecs de audio |
| **Modulación** | Mapeo de bits a símbolos complejos |
| **Polar** | Códigos Polar - Código de canal 5G para control |
| **PSNR** | Peak Signal-to-Noise Ratio - Métrica de calidad de imagen |
| **QAM** | Quadrature Amplitude Modulation - Modulación en I/Q |
| **QPSK** | Quadrature Phase Shift Keying - 4 símbolos |
| **SNR** | Signal-to-Noise Ratio - Relación señal/ruido |
| **SSCC** | Separate Source-Channel Coding - Arquitectura clásica |
| **SSIM** | Structural Similarity Index - Métrica perceptual |

---

## 10. Contacto y Soporte

### 10.1. Reporte de Problemas

Si encuentra errores o comportamientos inesperados:
1. Verifique que esté usando un navegador moderno actualizado
2. Revise la consola del navegador (F12) para mensajes de error
3. Documente los pasos para reproducir el problema
4. Incluya captura de pantalla si es posible

### 10.2. Sugerencias y Mejoras

Este es un proyecto educativo en evolución. Sugerencias bienvenidas para:
- Nuevas funcionalidades
- Algoritmos adicionales
- Mejoras en visualizaciones
- Clarificación de documentación

---

## Apéndice A: Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| **Enter** | Ejecutar simulación (si panel de control tiene foco) |
| **Ctrl/Cmd + R** | Recargar página |
| **F12** | Abrir consola del desarrollador |

---

## Apéndice B: Configuraciones Predefinidas

### Configuración "Principiante"
- Fuente: Texto corto
- Codificación de fuente: Ninguno
- Codificación de canal: LDPC 1/2
- Modulación: QPSK
- SNR: 15 dB
- **Resultado**: Transmisión confiable, fácil de entender

### Configuración "Compresión de Imagen"
- Fuente: Imagen Lena
- Codificación de fuente: DCT (calidad 60)
- Codificación de canal: LDPC 2/3
- Modulación: 16-QAM
- SNR: 12 dB
- **Resultado**: Balance entre compresión y calidad

### Configuración "Alta Velocidad"
- Fuente: Texto
- Codificación de fuente: Huffman
- Codificación de canal: LDPC 3/4
- Modulación: 64-QAM
- SNR: 20 dB
- **Resultado**: Máxima tasa de datos, requiere buen SNR

### Configuración "Condiciones Adversas"
- Fuente: Audio
- Codificación de fuente: MDCT
- Codificación de canal: Polar 1/2
- Modulación: QPSK
- SNR: 5 dB
- **Resultado**: Transmisión robusta en canal ruidoso

---

**Fin del Manual de Usuario**

*Versión 1.0 - Octubre 2025*
*Para más información, consulte el README.md y job.md del proyecto*
