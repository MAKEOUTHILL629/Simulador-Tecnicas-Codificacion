# Especificación Técnica para el Desarrollo de un Simulador de Cadena de Comunicación Digital

## Preámbulo: Visión General del Proyecto y Filosofía Arquitectónica

Este documento constituye una especificación técnica exhaustiva para el desarrollo de un Simulador de Cadena de Comunicación Digital interactivo y basado en la web. El objetivo principal es crear una herramienta educativa que modele el proceso de extremo a extremo de la transmisión de diversas formas de información (texto, imagen, audio, video) a través de un canal ruidoso, implementando técnicas de codificación y modulación pertinentes a los sistemas 5G, 5G Avanzado y conceptualmente 6G. El simulador debe adherirse estrictamente al flujo de trabajo modular y secuencial especificado en los requisitos académicos del usuario, que representa una arquitectura clásica de Codificación Separada de Fuente y Canal (SSCC, por sus siglas en inglés).

Un análisis de los materiales de investigación proporcionados revela una dicotomía fundamental: el flujo de trabajo requerido sigue un modelo SSCC tradicional, mientras que la investigación de vanguardia, especialmente en el contexto de 6G, aboga firmemente por la Codificación Conjunta de Fuente y Canal (JSCC) y su variante basada en aprendizaje profundo, DeepJSCC, como un paradigma de mayor rendimiento. La literatura académica subraya que, aunque el Teorema de Separación de Shannon establece la optimalidad asintótica de SSCC, la JSCC ofrece un rendimiento superior en escenarios prácticos de longitud de bloque finita, y evita el "efecto acantilado" (cliff effect) característico de los sistemas digitales. El enfoque de este proyecto es, por lo tanto, reconciliar estas dos perspectivas. El simulador se construirá sobre la base del modelo SSCC para cumplir con los requisitos estructurales del curso, pero incorporará una representación conceptual de los principios de codificación de 6G. Esto se logrará mediante la abstracción del componente de compresión de un sistema DeepJSCC e implementándolo como un bloque discreto de "Codificación de Fuente". Esta estrategia demuestra una comprensión matizada del panorama teórico, al tiempo que se adhiere a las restricciones prácticas de la asignación académica.

## 1. Arquitectura General y Diseño de la Interfaz de Usuario (UI)

### 1.1. Objetivo y Alcance del Proyecto

El propósito del simulador es proporcionar un entorno configurable y práctico para visualizar y analizar el rendimiento de un sistema de comunicación digital. El sistema se implementará íntegramente en código del lado del cliente (HTML, CSS, JavaScript) para garantizar la portabilidad y la facilidad de uso sin dependencias del lado del servidor.

### 1.2. Especificación de Diseño de UI/UX

Se especifica un diseño de tres columnas para la interfaz principal, con el fin de organizar de manera lógica los controles, las visualizaciones y los resultados.

#### 1.2.1. Disposición Principal

* **Columna Izquierda (Panel de Control):** Contendrá todos los parámetros configurables por el usuario. Este panel será estático y estará siempre visible para permitir ajustes rápidos y la re-ejecución de la simulación. Los parámetros se agruparán en secciones lógicas, como se detalla en la Tabla 1.
* **Columna Central (Tubería de Visualización):** Una serie de paneles apilados verticalmente, cada uno correspondiendo a una etapa de la cadena de comunicación: Entrada, Datos Codificados de Fuente, Datos Codificados de Canal, Señal Modulada, Salida del Canal, Señal Demodulada, Datos Decodificados, Salida Final. Cada panel tendrá un encabezado claro y un área de contenido para mostrar gráficos o datos.
* **Columna Derecha (Análisis y Resultados):** Mostrará la salida final reconstruida para una comparación visual directa con la entrada, métricas de rendimiento cuantitativas (BER, SER, PSNR, SSIM, etc.), y los cálculos teóricos de la información.

#### 1.2.2. Interactividad

Todos los cambios de parámetros en el Panel de Control activarán una re-simulación y actualizarán todos los paneles de visualización y resultados en tiempo real. Un botón "Ejecutar Simulación" iniciará el proceso. La interfaz de usuario debe permanecer receptiva durante el cálculo; para ello, se utilizarán funciones asíncronas (async/await) para los pasos de procesamiento intensivo (por ejemplo, codificación de canal, decodificación) con el fin de evitar el bloqueo del navegador.

### 1.3. Tecnologías y Librerías Centrales

* **Lógica:** Se utilizará JavaScript puro (ES6+). No se emplearán frameworks como React o Vue, para centrar el desarrollo en la implementación de los algoritmos fundamentales.
* **Estructura:** HTML5 para la estructura semántica del documento.
* **Estilo:** CSS3 para la presentación, con una estética limpia y profesional adecuada para una aplicación técnica.
* **Visualización:** Se exige el uso de Plotly.js para toda la representación gráfica debido a su amplio conjunto de características para el trazado científico, incluyendo diagramas de constelación, gráficos de líneas, histogramas y mapas de calor (para espectrogramas).

### 1.4. Parámetros de Configuración del Simulador

La siguiente tabla resume los parámetros configurables por el usuario que deben estar disponibles en el Panel de Control. Esta tabla sirve como una lista de verificación de alto nivel para los elementos de la interfaz de usuario y las variables de simulación requeridas.

**Tabla 1: Parámetros de Configuración del Simulador**

| Categoría de Parámetro | Nombre del Parámetro | Opciones Seleccionables |
| :--- | :--- | :--- |
| Fuente | Tipo de Fuente | Texto, Imagen, Audio, Video (Simplificado) |
| Codificación de Fuente | Algoritmo | Ninguno, Huffman, Basado en DCT (para Imagen/Video), Basado en MDCT (para Audio), Codificador Aprendido (6G) |
| Codificación de Canal | Algoritmo | Ninguno, LDPC, Polar |
| | Tasa de Código | $1/2$, $2/3$, $3/4$ |
| Modulación | Esquema | QPSK, 16-QAM, 64-QAM, 256-QAM |
| Canal | Parámetro | SNR (dB), $Eb/N_{0}$ (dB) |
| | Valor | Entrada numérica definida por el usuario |

## 2. Generación y Preprocesamiento de Datos de Fuente

Esta sección detalla cómo el simulador manejará los cuatro tipos de datos de fuente requeridos, desde la entrada del usuario hasta la representación binaria unificada que alimenta la cadena de codificación.

### 2.1. Fuente de Texto

Se implementará un elemento `<textarea>` de HTML para permitir a los usuarios introducir texto personalizado. Un botón "Cargar Texto de Muestra" poblará el área de texto con un párrafo predeterminado para facilitar las pruebas. La lógica de JavaScript convertirá la cadena de entrada en un flujo binario utilizando la API `TextEncoder` para la codificación UTF-8. Este flujo binario, una secuencia de ceros y unos, constituirá la entrada $X$ para la etapa de codificación de fuente.

### 2.2. Fuente de Imagen

Se utilizará un elemento `<input type="file" accept="image/png, image/jpeg">` para la carga de archivos de imagen. Se incluirán imágenes de muestra predeterminadas (por ejemplo, Lena, Baboon) que podrán ser seleccionadas por el usuario. Al cargar una imagen, esta se dibujará en un elemento `<canvas>` de HTML. Se utilizará el método `CanvasRenderingContext2D.getImageData()` para extraer los datos brutos de los píxeles como un `Uint8ClampedArray`. Este array, que representa los valores RGBA, se procesará para convertirlo en un array tridimensional de la forma [alto][ancho] para los componentes RGB, que servirá como la entrada $X$.

### 2.3. Fuente de Audio

Se proporcionará un elemento `<input type="file" accept="audio/wav">` para la carga de archivos de audio. Se incluirá un archivo de audio de muestra predeterminado (por ejemplo, un clip de voz corto). Se utilizará la Web Audio API (específicamente, `AudioContext` y `decodeAudioData`) para decodificar el archivo WAV en un `AudioBuffer`. Los datos de muestra PCM brutos (un `Float32Array`) se extraerán del búfer para servir como el array de entrada unidimensional $X$.

### 2.4. Fuente de Video (Modelo Simplificado)

La implementación de un códec de video completo excede el alcance de este proyecto. El objetivo pedagógico es demostrar el principio de explotación de la redundancia temporal. Para ello, el modelo de video procesará una secuencia corta de fotogramas (por ejemplo, 10 fotogramas). El primer fotograma se tratará como un I-frame (codificado intra-fotograma), y los fotogramas subsiguientes como P-frames (codificados predictivamente). Se proporcionarán dos opciones de implementación:

1.  **Video Sintético:** Generar una animación simple en un `<canvas>`, como un pequeño cuadrado moviéndose sobre un fondo estático. El simulador capturará 10 fotogramas consecutivos de esta animación.
2.  **Carga de Clip Corto (Opcional):** Permitir la carga de un archivo de video muy corto y utilizar una librería auxiliar de JavaScript para extraer los primeros 10 fotogramas.

La secuencia de fotogramas, representada como un array 4D de la forma [fotograma][alto][ancho], constituirá la entrada $X$.

## 3. Algoritmos de Codificación de Fuente

Esta sección define los algoritmos de compresión, abarcando desde técnicas fundamentales hasta conceptos avanzados que representan los principios de los sistemas de comunicación de próxima generación.

### 3.1. Codificador de Entropía de Base: Codificación Huffman

Se implementará un algoritmo clásico de codificación Huffman. La función tomará un flujo de datos, calculará las frecuencias de los símbolos (por ejemplo, a nivel de byte), construirá el árbol de Huffman, generará la tabla de códigos de prefijo y codificará el flujo. La tabla de códigos debe ser antepuesta a los datos codificados para que el decodificador pueda reconstruir el árbol. Este algoritmo sirve como un ejemplo fundamental de Código de Longitud Variable (VLC), una técnica cuya decodificación en canales ruidosos se discute ampliamente en la literatura.¹

### 3.2. Códecs 5G/5G Avanzado (Abstracción Basada en Principios)

Los estándares 3GPP para medios en 5G especifican codecs complejos como HEVC (High Efficiency Video Coding), VVC (Versatile Video Coding), EVS (Enhanced Voice Services) e IVAS (Immersive Voice and Audio Services).² Una implementación directa es inviable. Por lo tanto, el simulador modelará su principio fundamental compartido: la **Codificación por Transformada**. Este enfoque transforma la señal del dominio temporal/espacial al dominio de la frecuencia, donde la energía tiende a concentrarse en unos pocos coeficientes, lo que permite una compresión eficiente.

#### 3.2.1. Implementación para Imagen/Video (Emulando HEVC/VVC)

* **Transformada:** Se aplicará una Transformada de Coseno Discreta (DCT) 2D a bloques de $8 \times 8$ del componente de luminancia de la imagen (y opcionalmente a la crominancia).
* **Cuantificación:** Los coeficientes de la DCT se dividirán por una matriz de cuantificación, controlada por un "Factor de Calidad" ajustable por el usuario (1-100). Una mayor calidad implica pasos de cuantificación más pequeños (menos división).
* **Codificación de Entropía:** Los coeficientes cuantificados se escanearán en un patrón de zigzag para agrupar los coeficientes de baja frecuencia (generalmente más grandes) primero. El flujo resultante de coeficientes se codificará utilizando el codificador Huffman implementado en la sección 3.1.
* **Para Video:** El primer fotograma será un I-frame, codificado como se describió anteriormente. Para los P-frames subsiguientes, se realizará una estimación de movimiento simple basada en bloques (por ejemplo, utilizando la Suma de Diferencias Absolutas) para encontrar vectores de movimiento. Se transmitirán los vectores de movimiento y el residuo (la diferencia entre la predicción compensada por movimiento y el fotograma real) codificado con DCT, cuantificación y Huffman.

#### 3.2.2. Implementación para Audio (Emulando EVS/IVAS)

* **Transformada:** Se aplicará la Transformada de Coseno Discreta Modificada (MDCT) en ventanas superpuestas de la señal de audio. La MDCT es fundamental en códecs de audio modernos por su capacidad para manejar el solapamiento de bloques sin introducir artefactos.
* **Cuantificación y Codificación:** Se aplicará una cuantificación escalar a los coeficientes de la MDCT y el resultado se codificará por entropía con el codificador Huffman.

### 3.3. Códec 6G (Modelo Conceptual de DeepJSCC)

Este módulo representa conceptualmente el componente de compresión de un sistema DeepJSCC, adaptado para encajar en la arquitectura SSCC. La idea es simular un codificador que ha "aprendido" a representar la fuente de manera eficiente.

* **Implementación ("Codificador Aprendido"):**
    * Se proporcionará la estructura y los pesos predefinidos de un autoencoder convolucional simple en JavaScript. Este modelo no se entrenará en el simulador, sino que se definirá estáticamente.
    * **Codificador:** Una pequeña Red Neuronal Convolucional (CNN) que toma un parche de imagen (por ejemplo, $32 \times 32$) como entrada y produce un vector latente de baja dimensión (por ejemplo, 16 valores de punto flotante).
    * **"Cuello de Botella Digital":** Este vector latente se cuantifica (por ejemplo, 8 bits por valor) y se serializa en un flujo binario. Este paso es crucial, ya que convierte la representación analógica del espacio latente en un formato digital que puede ser procesado por el codificador de canal, cumpliendo así con el paradigma SSCC.
    * **Decodificador:** La parte correspondiente del decodificador del autoencoder se utilizará en la etapa de Decodificación de Fuente (Sección 5.4) para reconstruir el parche de la imagen a partir del vector latente recibido.

## 4. Codificación de Canal y Esquemas de Modulación

Esta sección especifica los esquemas de codificación de canal y modulación estandarizados por el 3GPP para 5G New Radio (NR).

### 4.1. Codificación de Canal (Estándares 5G NR)

La estandarización de 5G NR adoptó los códigos LDPC para los canales de datos (eMBB) y los códigos Polares para los canales de control, debido a su rendimiento cercano a la capacidad de Shannon en sus respectivos regímenes de operación. El simulador implementará ambos.

#### 4.1.1. Códigos LDPC (Low-Density Parity-Check)

* **Codificador:** Se implementará un codificador LDPC Quasi-Cíclico (QC-LDPC). Se proporcionará un pequeño grafo base (protograph) predefinido y un factor de expansión (lifting factor) $Z$ para construir la matriz de verificación de paridad completa $H$. La estructura QC-LDPC es estándar en 5G por permitir una implementación paralela y de alto rendimiento. La codificación será sistemática, donde los bits de paridad se calculan y se añaden a los bits de información.
* **Decodificador:** Se implementará el decodificador de Propagación de Creencias (Belief Propagation), específicamente el Algoritmo Suma-Producto. Este operará sobre Log-Likelihood Ratios (LLRs) provenientes del demodulador. Se establecerá un número máximo de iteraciones (por ejemplo, 50) para garantizar la terminación del algoritmo.

#### 4.1.2. Códigos Polares

* **Codificador:** Se implementará un codificador Polar. La construcción se basará en un método independiente del SNR donde las fiabilidades de los subcanales se precalculan (como se menciona en [9]). Se especificará la construcción de la matriz generadora. Se antepondrá un CRC (Cyclic Redundancy Check) a los bits del mensaje, creando un código Polar Asistido por CRC (CA-Polar), una práctica estándar en 5G para mejorar el rendimiento de la decodificación por lista.
* **Decodificador:** Se implementará un decodificador de Cancelación Sucesiva por Lista (SCL). Se utilizará un tamaño de lista $L$ pequeño (por ejemplo, 4 u 8) para equilibrar el rendimiento y la complejidad computacional. El decodificador utilizará el CRC para seleccionar la ruta más probable de la lista, descartando las rutas que no satisfacen la verificación del CRC.

### 4.2. Esquemas de Modulación

5G NR utiliza una variedad de esquemas de modulación para adaptarse a las condiciones del canal, permitiendo un equilibrio entre la velocidad de datos y la robustez."

* **Implementación:**
    * Se creará una función de mapeo que tome un bloque de $k$ bits y lo asigne a uno de los $M=2^{k}$ símbolos complejos de la constelación.
    * Se implementarán mapeadores para QPSK ($k=2$), 16-QAM ($k=4$), 64-QAM ($k=6$) y 256-QAM ($k=8$).¹³
    * Los símbolos de salida deben ser normalizados para tener una potencia media unitaria, asegurando que la potencia de la señal transmitida sea consistente independientemente del esquema de modulación.

## 5. Canal, Demodulación y Decodificación

### 5.1. Modelo de Canal

Se implementará un canal de Ruido Blanco Gaussiano Aditivo (AWGN). La función tomará los símbolos complejos modulados y añadirá ruido complejo $n = n_I + j \cdot n_Q$, donde $n_I$ y $n_Q$ son variables aleatorias gaussianas reales, independientes, con media cero y varianza $\sigma^2$. La varianza del ruido $\sigma^2$ se calculará a partir del parámetro especificado por el usuario (SNR o Eb/No) utilizando las siguientes relaciones:

* Para una señal de potencia unitaria, la relación señal/ruido (SNR) se define como $SNR = \frac{1}{2\sigma^2}$.
* La relación energía por bit a densidad espectral de potencia de ruido ($E_b/N_0$) se relaciona con el SNR mediante la expresión:
    $$\frac{E_b}{N_0} = \frac{SNR}{k \cdot R_c}$$
    donde $k$ es el número de bits por símbolo (dependiente de la modulación) y $R_c$ es la tasa del código de canal.

### 5.2. Demodulación

Los decodificadores de canal modernos, como los de LDPC y Polares, requieren información "suave" (soft information) en lugar de decisiones binarias "duras" para lograr un rendimiento óptimo.

* **Implementación:**
    * **Demodulador de Decisión Dura:** Para fines de comparación, se implementará un detector de distancia euclidiana mínima que mapea cada símbolo ruidoso recibido al punto más cercano de la constelación y emite la secuencia de bits correspondiente.
    * **Demodulador de Decisión Suave:** Este será el demodulador principal. Se implementará una función para calcular el Log-Likelihood Ratio (LLR) para cada bit. Para un canal AWGN, el LLR de un bit $b_i$ se puede aproximar con la fórmula max-log para simplificar el cálculo:
        $$LLR(b_i) \approx \frac{1}{2\sigma^2} \left(\min_{s \in S_O} |y-s|^2 - \min_{s \in S_1} |y-s|^2 \right)$$
        donde $y$ es el símbolo recibido, y $S_0$ y $S_1$ son los conjuntos de símbolos de la constelación donde el bit $b_i$ es 0 y 1, respectivamente.

### 5.3. Decodificación de Canal

Este bloque contendrá los decodificadores LDPC (Propagación de Creencias) y Polar (SCL) especificados en la Sección 4.1. Tomarán los LLRs como entrada y producirán una estimación de decisión dura del flujo de bits transmitido.

### 5.4. Decodificación de Fuente

Se implementarán las operaciones inversas para cada algoritmo de la Sección 3: decodificación Huffman (utilizando la tabla de códigos recibida), de-cuantificación, transformada inversa (IDCT/IMDCT) y la parte del decodificador del autoencoder aprendido.

## 6. Visualizaciones Requeridas

Esta sección exige salidas gráficas específicas para cada etapa, con el fin de cumplir con el requisito de visualización del proyecto.

* **Fuente de Entrada:** Mostrar el texto, la imagen o un gráfico de la forma de onda del audio.
* **Datos Codificados de Fuente:** Mostrar los primeros N bits del flujo binario y su longitud total.
* **Señal Modulada (Pre-Canal):** Un diagrama de dispersión de los puntos de la constelación (gráfico I/Q).
* **Salida del Canal (Post-Canal):** Un diagrama de dispersión de los símbolos ruidosos recibidos, superpuestos a los puntos ideales de la constelación. Esta es una visualización crucial para entender el efecto del ruido.
* **Salida del Demodulador:** Un histograma de los valores LLR calculados. Esto ayuda a visualizar la confianza de las decisiones suaves.
* **Salida Final:** Mostrar el texto, la imagen o la forma de onda de audio reconstruidos para una comparación directa con la entrada.

## 7. Métricas de Rendimiento y Cálculos Teórico-Informativos

Esta sección detalla el análisis cuantitativo requerido por el usuario, abordando la verificación de la integridad y el cálculo de métricas de la teoría de la información.

### 7.1. Métricas de Integridad y Calidad de la Información

* **Tasa de Error de Bit (BER) y Tasa de Error de Símbolo (SER):**
    * Se implementarán funciones para comparar los flujos de bits/símbolos transmitidos y recibidos y calcular las tasas de error.¹⁵ La relación $SER \approx \log_2(M) \cdot BER$ para SNR alto con codificación Gray se señalará como un concepto teórico importante.¹⁵
* **Relación Señal a Ruido de Pico (PSNR) (para Imágenes/Video):**
    * Se implementará el cálculo del PSNR basado en el Error Cuadrático Medio (MSE), según las definiciones estándar.¹⁸ Se proporcionará la fórmula:
        $$PSNR = 10 \cdot \log_{10}\left(\frac{MAX_I^2}{MSE}\right)$$
        donde $MAX_I$ es el valor máximo posible de un píxel (255 para imágenes de 8 bits) y el MSE se define como:
        $$MSE = \frac{1}{m \cdot n}\sum_{i=0}^{m-1}\sum_{j=0}^{n-1} [I(i, j) - K(i, j)]^2$$
        siendo $I$ la imagen original y $K$ la imagen reconstruida.²¹
* **Índice de Similitud Estructural (SSIM) (para Imágenes/Video):**
    * Se implementará la métrica SSIM. Esta es una métrica perceptual crucial que a menudo se correlaciona mejor con el juicio humano que el PSNR.²² Se proporcionará la fórmula general y sus componentes de luminancia ($l$), contraste ($c$) y estructura ($s$).²⁴
        $$SSIM(x,y) = \frac{(2\mu_x\mu_y + C_1)(2\sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)}$$
* **Calidad Perceptual de Audio (Proxy):**
    * Implementar una métrica completa como PESQ (Perceptual Evaluation of Speech Quality)²⁶ es demasiado complejo. En su lugar, se calculará la **SNR Segmental**. Se calculará la SNR sobre tramas cortas y no superpuestas (por ejemplo, 20 ms) de la señal de audio y se promediarán los resultados en el dominio de dB. Esto refleja mejor la calidad percibida en presencia de ruido no estacionario.

### 7.2. Cálculos Teórico-Informativos

Las fórmulas para la entropía y la información mutua son teóricas. La clave es especificar cómo estimarlas a partir de las muestras de datos finitas disponibles en el simulador.

* **Entropía $H(X)$ y $H(Y)$:**
    * La entropía de una fuente discreta $X$ se define como $H(X) = -\sum_{x \in \mathcal{X}} p(x) \log_2 p(x)$.²⁸ Para estimar la distribución de probabilidad $p(x)$ a partir de los datos de la fuente (por ejemplo, los valores de intensidad de los píxeles de una imagen), se construirá un histograma de los valores de los símbolos. La probabilidad de cada símbolo $i$ se estimará como $p(i) = \frac{\text{frecuencia de } i}{\text{número total de símbolos}}$.³⁰ Se implementará una función que tome un array de datos, calcule el histograma para estimar $p(x)$ y luego calcule la entropía en bits/símbolo.
* **Información Mutua $I(X; Y)$:**
    * La información mutua entre la entrada $X$ y la salida $Y$ mide la reducción de la incertidumbre sobre $X$ que se obtiene al observar $Y$. Se calcula como $I(X;Y) = H(X) - H(X|Y)$ o, de forma equivalente, $I(X;Y) = H(X) + H(Y) - H(X,Y)$.³¹ La implementación utilizará la fórmula:
        $$I(X;Y) = \sum_{x \in \mathcal{X}}\sum_{y \in \mathcal{Y}} p(x,y) \log_2\left(\frac{p(x,y)}{p(x)p(y)}\right)$$
        donde la distribución de probabilidad conjunta $p(x,y)$ se estimará construyendo un histograma 2D de los pares de símbolos de entrada/salida co-ocurrentes y normalizándolo.³⁴

## 8. Parámetros Adicionales para la Integridad de la Información

Esta sección aborda directamente la solicitud de identificar otros parámetros relevantes para medir la integridad de la información.

### 8.1. Magnitud del Vector de Error (EVM)

* **Definición:** La EVM es una métrica estándar de la industria que mide la calidad de la señal modulada cuantificando la diferencia entre los puntos ideales de la constelación y los puntos recibidos.¹³
* **Cálculo:** Se calculará como $EVM (\%) = \sqrt{\frac{P_{\text{error}}}{P_{\text{referencia}}}} \times 100$, donde $P_{\text{error}}$ es la potencia media del vector de error (la diferencia entre los símbolos recibidos e ideales) y $P_{\text{referencia}}$ es la potencia media de los símbolos ideales.
* **Significado:** La EVM proporciona una medida integral de la calidad de todo el transmisor y el canal (incluyendo ruido de fase, desequilibrio de amplitud y no linealidades) antes de que se consideren los efectos de la codificación de canal. Impacta directamente en la calidad de la entrada al demodulador y, por lo tanto, en el rendimiento general del sistema.

### 8.2. Tasa de Error de Bloque (BLER) / Tasa de Error de Trama (FER)

* **Definición:** Mientras que BER/SER miden errores a nivel de bit/símbolo, BLER/FER miden errores a nivel de paquete o bloque de datos. Un bloque se considera erróneo si uno o más bits dentro de él son incorrectos.¹⁶
* **Cálculo:** $BLER = \frac{\text{Número de Bloques Erróneos}}{\text{Número Total de Bloques Transmitidos}}$.
* **Significado:** Esta métrica es a menudo más relevante para sistemas prácticos (como el streaming de video o la transferencia de archivos) donde la unidad de retransmisión es un bloque/paquete, no un solo bit. Proporciona una medida del "rendimiento útil" del sistema, ya que un solo error de bit puede hacer que un paquete entero sea descartado.

### 8.3. Distancia de Levenshtein (para Texto)

* **Definición:** Mide la diferencia entre dos secuencias contando el número mínimo de ediciones de un solo carácter (inserciones, eliminaciones o sustituciones) necesarias para cambiar una secuencia en la otra. Se menciona como una medida de rendimiento válida en la literatura.¹
* **Significado:** Para la transmisión de texto, el BER puede ser engañoso. Un solo error de bit podría causar una sustitución de caracteres semánticamente cercana, mientras que otro podría provocar una cascada de errores que haga que el texto sea ilegible. La distancia de Levenshtein proporciona una medida más práctica de la "legibilidad" del texto recibido, evaluando la integridad estructural a nivel de caracteres.

## Conclusión

La especificación detallada en este documento proporciona un plan completo para la creación de un simulador de comunicación digital robusto y pedagógicamente valioso. Al implementar una arquitectura SSCC modular y al mismo tiempo incorporar representaciones conceptuales de técnicas avanzadas de 6G, la herramienta resultante permitirá a los estudiantes explorar de manera interactiva las compensaciones fundamentales entre la eficiencia de la compresión, la robustez de la codificación, la eficiencia espectral de la modulación y el impacto del ruido del canal. Las visualizaciones en cada etapa y el conjunto completo de métricas de rendimiento, desde las tasas de error de bit hasta los cálculos de información mutua, ofrecerán una visión profunda del comportamiento del sistema, cerrando la brecha entre la teoría abstracta de la información y la ingeniería de comunicaciones práctica.

## Obras citadas

1.  Articulo 1.pdf
2.  3GPP 26-series: 3G to 5G CODECs - Tech-invite, fecha de acceso: octubre 29, 2025, <https://www.tech-invite.com/3m26/tinv-3gpp-26.html>
3.  3GPP specification series: 26series, fecha de acceso: octubre 29, 2R025, <https://www.3gpp.org/dynareport/26-series.htm>
4.  New Codecs for 5G, fecha de acceso: octubre 29, 2025, <https://dashif.org/docs/workshop-2019/04-thierry%20fautier%20-%20Harmonic%20Codec%20Comparison%205G%20Media%20Workshop%20Final%20v3.pdf>
5.  An overview of channel coding for 5G NR cellular communications | APSIPA Transactions on Signal and Information Processing - Cambridge University Press & Assessment, fecha de acceso: octubre 29, 2025, <https://www.cambridge.org/core/journals/apsipa-transactions-on-signal-and-information-processing/article/an-overview-of-channel-coding-for-5g-nr-cellular-communications/CF52C26874AF5E00883E00B6E1F907C7>
6.  The Development, Operation and Performance of the 5G Polar Codes - ePrints Soton - University of Southampton, fecha de acceso: octubre 29, 2025, <https://eprints.soton.ac.uk/436696/1/3GPP%20PAPER%20two%20column%2011.pdf>
7.  Full article: Overview of the challenges and solutions for 5G channel coding schemes, fecha de acceso: octubre 29, 2025, <https://www.tandfonline.com/doi/full/10.1080/24751839.2021.1954752>
8.  Demystifying 5G Polar and LDPC Codes: A Comprehensive Review and Foundations, fecha de acceso: octubre 29, 2025, <https://arxiv.org/html/2502.11053v2>
9.  5G New Radio Polar Coding - MATLAB & Simulink - MathWorks, fecha de acceso: octubre 29, 2025, <https://la.mathworks.com/help/5g/gs/polar-coding.html>
10. 5G/NR Channel Codes Evolution and Recommendation on Polar Codes - Techplayon, fecha de acceso: octubre 29, 2025, <https://www.techplayon.com/5gnr-channel-codes-evolution-consideration-3gpp-recommendation-polar-codes/>
11. 5G Waveforms & Modulation: CP-OFDM & DFT-s-OFDM - Electronics Notes, fecha de acceso: octubre 29, 2025, <https://www.electronics-notes.com/articles/connectivity/5g-mobile-wireless-cellular/waveforms-ofdm-modulation.php>
12. Understanding the 5G NR PHY - Tetcos, fecha de acceso: octubre 29, 2025, <https://www.tetcos.com/pdf/v13/Experiments/5G-NR-PHY.pdf>
13. TS 138 521-1-V15.1.0-5G; NR; User Equipment (UE) conformance specification - ETSI, fecha de acceso: octubre 29, 2025, <https://www.etsi.org/deliver/etsi_ts/138500_138599/13852101/15.01.00_60/ts_13852101v150100p.pdf>
14. Overcoming 5G NR mmWave Signal Quality Challenges | Keysight Blogs, fecha de acceso: octubre 29, 2025, <https://www.keysight.com/blogs/en/inds/2019/09/30/overcoming-5g-nr-mmwave-signal-quality-challenges>
15. Bit Error Rate Vs Symbol Error Rate: Ratio Bits | PDF | Teaching Methods & Materials | Computers - Scribd, fecha de acceso: octubre 29, 2025, <https://www.scribd.com/doc/126542419/BERvsSER>
16. Bit error rate - Wikipedia, fecha de acceso: octubre 29, 2025, <https://en.wikipedia.org/wiki/Bit_error_rate>
17. Why is bit error rate = symbol error rate / number of bits per symbol in QPSK, fecha de acceso: octubre 29, 2025, <https://dsp.stackexchange.com/questions/58124/why-is-bit-error-rate-symbol-error-rate-number-of-bits-per-symbol-in-qpsk>
18. www.mathworks.com, fecha de acceso: octubre 29, 2025, <https://www.mathworks.com/help/images/ref/psnr.html#:~:text=%3D%20psnr(A%2C%20ref)%20calculates,value%20indicates%20better%20image%20quality.&text=peaksnr%20%3D%20psnr(%20A%20%2C%20ref%20%2C%20peakval%20)%20calculates,the%20peak%20signal%20value%20peakval%20.>
19. Peak signal-to-noise ratio - Wikipedia, fecha de acceso: octubre 29, 2025, <https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio>
20. PSNR - Compute peak signal-to-noise ratio (PSNR) between images - Simulink - MathWorks, fecha de acceso: octubre 29, 2025, <https://www.mathworks.com/help/vision/ref/psnr.html>
21. Peak Signal-to-Noise Ratio (PSNR) - Python - GeeksforGeeks, fecha de acceso: octubre 29, 2025, <https://www.geeksforgeeks.org/python/python-peak-signal-to-noise-ratio-psnr/>
22. Structural similarity index measure - Wikipedia, fecha de acceso: octubre 29, 2025, <https://en.wikipedia.org/wiki/Structural_similarity_index_measure>
23. SSIM: Structural Similarity Index - Imatest, fecha de acceso: octubre 29, 2025, <https://www.imatest.com/docs/ssim/>
24. Structural similarity index family for image quality assessment in radiological images - PMC, fecha de acceso: octubre 29, 2025, <https://pmc.ncbi.nlm.nih.gov/articles/PMC5527267/>
25. Image Quality Assessment through FSIM, SSIM, MSE and PSNR-A Comparative Study, fecha de acceso: octubre 29, 2025, <https://www.scirp.org/journal/paperinformation?paperid=90911>
26. Perceptual Evaluation of Speech Quality - Wikipedia, fecha de acceso: octubre 29, 2025, <https://en.wikipedia.org/wiki/Perceptual_Evaluation_of_Speech_Quality>
27. ITU-T Rec. P.862 (02/2001) Perceptual evaluation of speech quality (PESQ), fecha de acceso: octubre 29, 2025, <http://moodle.eece.cu.edu.eg/pluginfile.php/2121/mod_resource/content/1/P.862.pdf>
28. www.machinelearningmastery.com, fecha de acceso: octubre 29, 2025, <https://www.machinelearningmastery.com/what-is-information-entropy/#:~:text=Entropy%20can%20be%20calculated%20for,*%20log(p(k)))>
29. Entropy (information theory) - Wikipedia, fecha de acceso: octubre 29, 2025, <https://en.wikipedia.org/wiki/Entropy_(information_theory)>
30. How to calculate entropy from a set of samples? - Math Stack Exchange, fecha de acceso: octubre 29, 2025, <https://math.stackexchange.com/questions/1369743/how-to-calculate-entropy-from-a-set-of-samples>
31. www.math.tecnico.ulisboa.pt, fecha de acceso: octubre 29, 2025, <https://www.math.tecnico.ulisboa.pt/~pmartins/CTC/CTC21Notes6.pdf>
32. Unit of information Discrete memory less source-Conditional entropies and joint entropies - Basic r - Sathyabama, fecha de acceso: octubre 29, 2025, <https://www.sathyabama.ac.in/sites/default/files/course-material/2020-10/note_1474544598.PDF>
33. Channel Capacity of Discrete memoryless channel If the channel is noiseless, then the reception of some symbol y j uniquely dete, fecha de acceso: octubre 29, 2025, <https://www.uoanbar.edu.iq/eStoreImages/Bank/2669.pdf>
34. Mutual information - Scholarpedia, fecha de acceso: octubre 29, 2025, <http://www.scholarpedia.org/article/Mutual_information>
35. What is the difference between frame error rate (FER) and symbol error rate (SER)?, fecha de acceso: octubre 29, 2025, <https://dsp.stackexchange.com/questions/58035/what-is-the-difference-between-frame-error-rate-fer-and-symbol-error-rate-ser>
