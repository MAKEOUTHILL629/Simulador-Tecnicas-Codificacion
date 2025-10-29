# Arquitectura Funcional para un Simulador de Sistemas de Comunicación Multi-Generacional (5G/6G) con Análisis Integrado de Codificación Conjunta Fuente-Canal

## Sección 1: Marco Arquitectónico del Simulador de Red

Esta sección establece la estructura fundamental del simulador, definiendo el flujo de procesamiento central, la lógica para la configuración impulsada por el usuario y las rutas adaptativas para manejar diversos tipos de datos. Traduce los requisitos de alto nivel en un modelo arquitectónico concreto.

### 1.1. El Flujo de Simulación de Extremo a Extremo: Desde la Fuente hasta la Reconstrucción

El simulador se estructura en torno a un flujo modular y secuencial que refleja el proceso de comunicación física. Esta arquitectura de tubería (pipeline) se define como una serie de bloques funcionales interconectados, cada uno de los cuales representa una etapa discreta en la cadena de transmisión y recepción. Cada etapa está diseñada para ser un punto de captura de datos, permitiendo la visualización y el análisis en cada paso del proceso.

La secuencia de procesamiento es la siguiente:

1.  **Generación de Fuente**: El proceso comienza con la selección del tipo de datos (Texto, Audio, Imagen, Video) y el contenido específico que se va a transmitir.
2.  **Codificación de Fuente**: Se aplican algoritmos de compresión a la fuente de datos para reducir su redundancia intrínseca.
3.  **Codificación de Canal y Modulación**: Se introduce redundancia controlada en el flujo de bits comprimido para protegerlo contra errores, y luego se mapea a símbolos complejos adecuados para la transmisión.
4.  **Simulación de Canal**: Los símbolos modulados se transmiten a través de un modelo de canal que introduce degradaciones, como ruido (AWGN) y efectos de desvanecimiento.
5.  **Demodulación y Decodificación de Canal**: En el receptor, los símbolos corruptos se convierten de nuevo en un flujo de bits, idealmente utilizando decisiones blandas (soft decisions) para preservar la información probabilistica. Posteriormente, se utiliza la redundancia del código de canal para corregir errores.
6.  **Decodificación de Fuente**: El flujo de bits corregido se utiliza para reconstruir el tipo de datos original.
7.  **Análisis de Rendimiento**: Se calculan métricas cuantitativas y cualitativas en varias etapas del flujo para evaluar el rendimiento general del sistema.

### 1.2. Lógica de Configuración Impulsada por la Tecnología y Restricciones entre Parámetros

Un requisito funcional crítico es que el simulador limite las opciones de configuración de acuerdo con la tecnología seleccionada. La interfaz de usuario (UI) del simulador debe estar gobernada por un motor de reglas que imponga combinaciones tecnológicas válidas, evitando configuraciones incompatibles o sin sentido. La selección de una tecnología primaria (5G, 5G Avanzado, 6G) actuará como un filtro maestro. Esta elección habilitará o deshabilitará dinámicamente las opciones en los menús de configuración posteriores. Por ejemplo, la selección de "5G" habilitará los códigos de canal LDPC y Polar ¹y esquemas de modulación hasta 256-QAM.3 La selección de "6G" no solo habilitará estas opciones, sino que también introducirá alternativas especulativas de próxima generación, como QAM de orden superior o esquemas de codificación novedosos basados en los principios de codificación conjunta fuente-canal (JSCC).5

Este enfoque no es meramente una característica de la interfaz, sino un modelo funcional de los propios estándares 3GPP. Transforma el simulador de un simple procesador de señales en una herramienta que puede utilizarse tanto para validar la comprensión de los estándares actuales como para explorar el espacio de parámetros potenciales para estándares futuros. La arquitectura puede, por tanto, cargar diferentes conjuntos de reglas, como un conjunto "5G NR Rel-17" para el cumplimiento de estándares o un conjunto "6G Exploratorio" para la investigación, elevando el propósito del simulador a una plataforma de investigación estructurada.

### 1.3. Rutas de Procesamiento Diferenciadas para Fuentes de Datos Heterogéneas

La arquitectura del simulador debe admitir cadenas de procesamiento distintas y paralelas, adaptadas a las propiedades estadísticas de cada tipo de datos, ya que un algoritmo optimizado para video no es necesariamente adecuado para texto. La selección de un tipo de fuente activará una ruta de algoritmos predeterminada, que puede ser modificada por el usuario dentro de los límites permitidos por la tecnología seleccionada.

* **Video**: La ruta predeterminada utilizará codificación de fuente HEVC/VVC, codificación de canal LDPC y métricas de calidad como PSNR/SSIM.
* **Audio**: La ruta predeterminada empleará codificación de fuente EVS/IVAS, codificación de canal Polar/LDPC y métricas de calidad como PESQ/STOI.
* **Texto**: La ruta predeterminada utilizará codificación de entropía (por ejemplo, Huffman, Aritmética), codificación de canal Polar y métricas como la Tasa de Error de Bit (BER) y la Tasa de Error de Símbolo (SER).

Este diseño implementa directamente el concepto de explotación de la redundancia específica de la fuente, una piedra angular tanto de la codificación separada fuente-canal (SSCC) eficiente como de los paradigmas de JSCC.5 Además, la arquitectura del simulador puede modelar la dicotomía teórica entre SSCC y JSCC como dos "modos" de operación distintos. En el "Modo SSCC", el decodificador de fuente es independiente del decodificador de canal. En el "Modo JSCC", los bloques de demodulación, decodificación de canal y decodificación de fuente se reemplazan por un único bloque integrado de "Decodificador Conjunto" que recibe información blanda del canal y produce directamente símbolos de fuente reconstruidos. Esta elección arquitectónica hace que la comparación teórica sea explícita y comprobable dentro del simulador.

**Tabla 1: Mapeo de Parámetros Específicos de la Tecnología**

| Tipo de Parámetro | 5G | 5G Avanzado | 6G (Exploratorio) |
| :--- | :--- | :--- | :--- |
| **Códec de Fuente (Video)** | H.265 (HEVC) | H.266 (VVC) | H.266 (VVC), Codecs Semánticos/Basados en IA |
| **Códec de Fuente (Audio)** | EVS | IVAS | IVAS, Códecs Basados en Tareas |
| **Códec de Canal (Datos)** | LDPC | LDPC | LDPC, Códigos Novedosos |
| **Códec de Canal (Control)** | Polar | Polar | Polar, Códigos Optimizados para Latencia |
| **Modulación** | QPSK, 16-QAM, 64-QAM, 256-QAM | QPSK, 16-QAM, 64-QAM, 256-QAM | Hasta 1024-QAM, Modulación Adaptativa al Contenido |

## Sección 2: Modelado de la Información de Fuente y Técnicas de Codificación

Esta sección proporciona una definición granular de cada fuente de información y los algoritmos específicos de codificación de fuente (compresión) que se implementarán. Diferenciará entre los estándares establecidos para 5G/5G-A y los paradigmas más vanguardistas, impulsados por la IA, relevantes para 6G.

### 2.1. Caracterización de las Fuentes de Información

Para garantizar experimentos realistas y repetibles, el simulador incluirá conjuntos de datos representativos para cada tipo de fuente:

* **Texto**: Cuerpos de texto estándar (archivos ASCII/UTF-8) con diferentes niveles de redundancia.
* **Audio**: Señales de voz (por ejemplo, del conjunto de datos TIMIT) y clips de música, muestreados a velocidades estándar (por ejemplo, 16 kHz para voz de banda ancha, 48 kHz para música).
* **Imagen**: Imágenes de prueba estándar (por ejemplo, Lena, Baboon) y conjuntos de datos modernos (por ejemplo, el conjunto de imágenes Kodak), almacenados en formatos sin pérdida como PNG o BMP.
* **Video**: Secuencias de video de prueba estándar (por ejemplo, Foreman, Flower Garden) en varias resoluciones (HD, 4K) y velocidades de fotogramas.

### 2.2. Estándares de Codificación de Fuente para 5G y 5G Avanzado

Esta subsección detalla los códecs estandarizados específicos que forman la linea base para las comunicaciones de la era 5G.

#### 2.2.1. Codificación de Voz y Audio

* **El simulador implementará el códec Enhanced Voice Services (EVS)**, el estándar para VoLTE y Vo5G, conocido por su alta calidad y flexibilidad.
* **Para 5G Avanzado y más allá, incluirá el códec Immersive Voice and Audio Services (IVAS)**, diseñado para experiencias de audio espaciales e inmersivas, que es un componente clave para futuras aplicaciones de realidad virtual y aumentada."

#### 2.2.2. Codificación de Imagen y Video

* **High Efficiency Video Coding (HEVC/H.265)** será el códec principal para 5G, ofreciendo ganancias de compresión significativas sobre su predecesor, AVC/H.264. Es la linea base para la transmisión de 4K.
* **Versatile Video Coding (VVC/H.266)** se incluirá como el códec para 5G Avanzado y las primeras etapas de 6G, proporcionando mejoras de eficiencia adicionales necesarias para video 8K y aplicaciones inmersivas.

La elección de un códec no se trata solo de cuál es "mejor", sino de equilibrar la eficiencia de compresión (tasa de bits) con la complejidad computacional y las restricciones de licencia. 14 Por lo tanto, el simulador asociará un "factor de complejidad" o un parámetro de "retraso de procesamiento" a cada opción de códec. Esto permite comparaciones más matizadas, donde un códec ligeramente menos eficiente podría ser preferible en un escenario de baja latencia (URLLC), proporcionando un espacio de análisis multidimensional más rico.

### 2.3. Paradigmas Exploratorios de Codificación de Fuente para 6G: Compresión Semántica y Orientada a Objetivos

Esta subsección va más allá de la compresión tradicional para modelar el futuro de 6G. La comunicación semántica y orientada a tareas es un motor clave para 6G, donde el objetivo no es la reconstrucción perfecta de la señal, sino transmitir el significado o la información relevante para una tarea. Esto representa un cambio de paradigma fundamental: los códecs 5G (HEVC, EVS) están diseñados para engañar la percepción humana eliminando información que no podemos ver o escuchar, mientras que los códecs 6G están diseñados para preservar el significado semántico para tareas de máquina a máquina.

El simulador modelará esto incluyendo un bloque de "Codificador Semántico Basado en IA". En lugar de un códec estándar, este bloque simulará el comportamiento de un codificador basado en redes neuronales (parte de una arquitectura DeepJSCC) que mapea la fuente directamente a una representación latente optimizada para el canal, omitiendo la generación tradicional de un flujo de bits. Para las simulaciones de 6G, esto requiere dos tipos diferentes de "verdad fundamental" (ground truth). Para una tarea centrada en el ser humano, la verdad fundamental es el video original. Para una tarea centrada en la máquina (por ejemplo, detección de objetos), la verdad fundamental podría ser un conjunto de cuadros delimitadores. El "Codificador Semántico" en el simulador será configurable para optimizar diferentes "objetivos", lo que a su vez requerirá diferentes métricas de rendimiento en la Sección 5 (por ejemplo, precisión de la detección de objetos frente a PSNR).

### 2.4. Visualización de la Señal Post-Codificación de Fuente

El simulador debe generar una representación visual de los datos después de la codificación de fuente:

* **Para todos los tipos de datos**, se mostrará un gráfico binario del flujo de bits resultante.
* **Para imágenes/videos**, el simulador también mostrará la imagen/cuadro comprimido y reconstruido (antes de la transmisión por el canal) para visualizar los artefactos de compresión.
* **Para el audio**, se mostrarán la forma de onda y el espectrograma de la señal comprimida.

## Sección 3: Codificación de Canal, Modulación y Transmisión sobre Canales con Degradación

Esta sección define el proceso de preparación del flujo de bits comprimido para la transmisión inalámbrica. Cubre los esquemas estandarizados de codificación de canal y modulación para 5G y discute cómo se modela el propio canal físico.

### 3.1. Esquemas de Codificación de Canal en Sistemas Inalámbricos Modernos

La codificación de canal agrega redundancia estructurada al flujo de bits para protegerlo de errores durante la transmisión. 16 5G NR reemplazó los antiguos códigos convolucionales y turbo con esquemas más avanzados, una decisión de ingeniería altamente optimizada basada en los diferentes requisitos (tamaño de bloque, latencia, complejidad) de la información de datos frente a la de control.

#### 3.1.1. Códigos LDPC para Canales de Datos

El simulador implementará códigos de Verificación de Paridad de Baja Densidad (LDPC) para los canales de datos (DL-SCH/UL-SCH). Estos fueron elegidos en 5G por su excelente rendimiento con bloques de gran tamaño y alto rendimiento, y su estructura de decodificación paralelizable es ideal para escenarios de banda ancha móvil mejorada (eMBB). El simulador permitirá a los usuarios seleccionar diferentes grafos base y tasas de código.

#### 3.1.2. Códigos Polares para Canales de Control

El simulador implementará Códigos Polares para los canales de control (BCH, DCI, UCI). Estos códigos alcanzan la capacidad teórica y tienen un rendimiento excepcional para los tamaños de bloque cortos a medianos típicos de la información de control.¹

### 3.2. Esquemas de Modulación Digital

Los bits codificados por el canal se mapearán a símbolos complejos utilizando esquemas de modulación digital estándar. El simulador admitirá QPSK, 16-QAM, 64-QAM y 256-QAM, como se especifica para 5G NR.3 Para la exploración de 6G, el simulador incluirá opciones para modulaciones de orden superior como 1024-QAM³, permitiendo la investigación del rendimiento en condiciones de SNR muy altas. La elección del esquema de modulación estará vinculada a los parámetros de calidad del canal, simulando el proceso de Modulación y Codificación Adaptativa (AMC).

### 3.3. Modelado del Canal Inalámbrico

Este bloque simula el medio de transmisión físico. Toma los símbolos modulados como entrada y produce una versión corrupta. El modelo de canal no es solo un bloque pasivo; es el motor principal para demostrar el valor de JSCC.

* **Modelo de Ruido**: La degradación principal será el Ruido Gaussiano Blanco Aditivo (AWGN). El nivel de ruido será configurable por el usuario a través de dos parámetros clave: Relación Señal a Ruido (SNR) y $E_{b}/N_{0}$ (Energía por bit a la densidad espectral de potencia de ruido).
* **Modelo de Desvanecimiento**: Para simular condiciones inalámbricas realistas, el simulador debe incluir modelos de desvanecimiento estándar (por ejemplo, Rayleigh, Rician). Esto es crucial, ya que los sistemas SSCC sufren de un "efecto acantilado" en canales que varían en el tiempo, mientras que JSCC proporciona una "degradación gradual". El simulador debe permitir a los usuarios cambiar fácilmente entre un canal AWGN estático (donde un SSCC bien diseñado funciona casi de manera óptima) y un canal de desvanecimiento dinámico (donde los beneficios de JSCC se vuelven inmediatamente evidentes en los gráficos comparativos).

### 3.4. Visualización de la Señal: Formas de Onda Moduladas y Corruptas por el Canal

* **Diagrama de Constelación**: El simulador mostrará el diagrama de constelación de los símbolos modulados antes y después de pasar por el canal. Esto proporciona una visualización intuitiva del impacto del ruido y el desvanecimiento.
* **Forma de Onda en el Dominio del Tiempo**: Se trazarán los componentes I/Q de la señal en función del tiempo, mostrando las formas de onda transmitidas y recibidas.

## Sección 4: Recepción de la Señal, Demodulación y Decodificación Avanzada

Esta sección detalla las operaciones del lado del receptor, centrándose en el paso crítico de la decodificación. Se basará directamente en la investigación proporcionada para definir un módulo de decodificación sofisticado capaz de realizar tanto la decodificación separada tradicional como la decodificación conjunta fuente-canal avanzada.

### 4.1. Demodulación y Generación de Información de Decisión Blanda

El primer paso en el receptor es convertir la forma de onda ruidosa recibida de nuevo en un flujo de bits. De manera crucial, en lugar de tomar una decisión "dura" (0 1), el demodulador calculará Log-Likelihood Ratios (LLRs) para cada bit. Estos LLRs representan la "información blanda", una medida de confianza sobre si un bit es un O o un 1. Esta información es la moneda de cambio de los sistemas de decodificación modernos y es esencial para el alto rendimiento de los decodificadores iterativos y los enfoques JSCC.5 La conexión entre el demodulador y el decodificador no es solo un cable que transporta bits; es un bus que transporta distribuciones de probabilidad.

### 4.2. El Paradigma de la Decodificación Conjunta Fuente-Canal (JSCD)

Esta subsección es el núcleo teórico de las capacidades avanzadas del simulador, basada directamente en la investigación proporcionada. El simulador implementará un bloque JSCD que explota tanto la redundancia inducida por el canal como la redundancia residual de la fuente.

#### 4.2.1. Explotación de la Redundancia Residual con Modelos Ocultos de Markov (HMMs)

Como se describe en la literatura 5, la suboptimidad de los codificadores de fuente deja una correlación residual (redundancia) en el flujo de bits. El simulador modelará el flujo codificado por la fuente como una función de un HMM. Este modelo estadístico es la clave para permitir la decodificación conjunta. El problema se convierte en uno de estimación de los estados ocultos (los símbolos originales de la fuente) a partir de las observaciones ruidosas (los LLRS recibidos). Para los códigos de longitud variable (VLC), esto aborda el "problema conjunto de segmentación y estimación", que es una de las principales dificultades de la decodificación de VLC en canales ruidosos.5

#### 4.2.2. Decodificación Iterativa mediante el Principio Turbo

El bloque JSCD se implementará como un decodificador iterativo, intercambiando información extrínseca entre un componente de decodificador de canal y un componente de decodificador de fuente. Esto evita la "explosión de estados" de un modelo completamente unificado. El simulador admitirá algoritmos clave para este proceso:

* **Algoritmo BCJR**: Un algoritmo óptimo de decodificación MAP símbolo por símbolo.
* **Algoritmo Viterbi de Salida Blanda (SOVA)**: Una aproximación menos compleja al BCJR.

### 4.3. Flujos de Decodificación Específicos de la Tecnología

El simulador contará con distintos flujos de decodificación basados en la configuración del usuario:

* **Flujo SSCC (Linea Base 5G)**: Un flujo estándar que consiste en un decodificador LDPC o Polar seguido de un decodificador de fuente separado (por ejemplo, HEVC, EVS). El decodificador de canal emite decisiones duras que se alimentan al decodificador de fuente. Este flujo es propenso al "efecto acantilado", donde un solo error de bit en un flujo VLC puede desincronizar el resto del flujo, lo que lleva a un fallo catastrófico.
* **Flujo JSCD Clásico (Exploración 5G-A/6G)**: Una estructura iterativa tipo turbo como se describe en 4.2. Este flujo es particularmente relevante para los VLC, donde puede recuperarse de errores de sincronización al encontrar la ruta más probable (secuencia de símbolos) a través del trellis del HMM, incluso si eso significa reevaluar los límites de los símbolos.
* **Modelo de Rendimiento DeepJSCC (Exploración 6G)**: Esto no será una implementación completa de una red neuronal, sino un modelo funcional basado en las características descritas en la investigación. Tomará las salidas del canal y producirá directamente una fuente reconstruida, con su rendimiento (por ejemplo, PSNR) variando suavemente en función del SNR del canal, modelando así la "degradación gradual" sin la sobrecarga de entrenar una red real.

### 4.4. Visualización de la Señal en las Etapas de Demodulación y Decodificación

* El simulador visualizará los valores de LLR después de la demodulación.
* **Para los decodificadores iterativos**, trazará la evolución de las tasas de error de bit o los valores de información extrínseca a lo largo de las iteraciones, proporcionando una visión del comportamiento de convergencia del decodificador.

## Sección 5: Evaluación del Rendimiento y Análisis Gráfico Comparativo

Esta sección define las métricas cuantitativas y las salidas gráficas que el simulador debe producir. Aborda directamente la solicitud central del usuario de "mostrar graficas comparativas" y calcular cantidades específicas de la teoría de la información. La "integridad" de la información se operacionalizará en tres niveles: integridad de la capa física (BER), integridad de la reconstrucción (PSNR/SSIM/PESQ) e integridad teórica de la información (información mutua).

### 5.1. Métricas Fundamentales de la Teoría de la Información

El simulador calculará estas métricas para proporcionar una comprensión teórica profunda del proceso de comunicación, basándose en la teoría clásica de Shannon. 16

#### 5.1.1. Cuantificación del Contenido de Información

* **Cantidad de Información (Autoinformación)**: Para un símbolo de fuente dado $s$ con probabilidad $p(s)$ el simulador calculará $l(s)=-log_{2}(p(s))$ bits. Esto mide la "sorpresa" de observar ese simbolo.21
* **Información Promedio (Entropía)**: Para todo el alfabeto de la fuente, el simulador calculará la entropia $H(X) = -\sum p(x)\log_{2}(p(x))$ bits/simbolo. Esta es la cota inferior fundamental para la compresión de una fuente sin memoria y mide la incertidumbre promedio de la fuente. 23

#### 5.1.2. Medición de la Transferencia de Información

* **Información Mutua**: El simulador calculará la información mutua $l(X;Y)=H(X)-H(X|Y)$ entre la fuente transmitida $X$ y la salida reconstruida $Y$. Esta métrica mide la cantidad de información sobre la entrada que se transmite con éxito a la salida, proporcionando una medida de la eficiencia del sistema de extremo a extremo. 25

### 5.2. Métricas de Calidad Objetivas y Perceptuales para la Integridad de la Información

Estas métricas responden a la pregunta "¿Qué tan buena es la salida reconstruida?" y abordan el requisito del usuario de "Verificar la claridad e integridad de la información resultante".

#### 5.2.1. Evaluación de la Calidad de Imagen y Video

* **Relación Señal a Ruido de Pico (PSNR)**: Una métrica clásica, fácil de calcular, basada en el Error Cuadrático Medio (MSE).
* **Índice de Similitud Estructural (SSIM)**: Una métrica perceptual más avanzada que compara luminancia, contraste y estructura, que a menudo se correlaciona mejor con la percepción de calidad humana.

#### 5.2.2. Evaluación de la Calidad de Voz y Audio

* **Evaluación Perceptual de la Calidad del Habla (PESQ)**: Un estándar de la UIT-T para la evaluación objetiva de la calidad de la voz, que produce una puntuación que se correlaciona con las Puntuaciones de Opinión Media (MOS) subjetivas. 29
* **Inteligibilidad Objetiva a Corto Plazo (STOI)**: Una métrica que mide específicamente la inteligibilidad del habla en condiciones de ruido. 32

### 5.3. Marco para la Generación de Análisis Comparativos y Visualizaciones

Esta es la característica principal del simulador. Los gráficos comparativos sirven como una herramienta de prueba de hipótesis para validar visualmente las afirmaciones centrales hechas en los artículos de investigación. El simulador debe ser capaz de generar los siguientes gráficos:

* **BER vs. $E_{b}/N_{0}$**: La curva clásica de rendimiento del canal, que muestra la tasa de error de bit en función de la relación señal a ruido normalizada para diferentes esquemas de codificación de canal y modulación.
* **PSNR/SSIM/PESQ vs. SNR del Canal**: Este es el gráfico clave para comparar SSCC y JSCC. Se utilizará para demostrar explícitamente el "efecto acantilado" de SSCC (una caída brusca de la calidad por debajo de un cierto SNR) frente a la "degradación gradual" de JSCC/DeepJSCC (una disminución suave y monotónica de la calidad), como se destaca en la investigación.5
* **Curvas de Tasa-Distorsión**: Gráficos de calidad (por ejemplo, PSNR) frente a la tasa de bits para diferentes códecs de fuente, permitiendo una comparación directa de su eficiencia de compresión.
* **Información Mutua vs. SNR del Canal**: Un gráfico que muestra cuánta información se transfiere con éxito en función de la calidad del canal.

**Tabla 2: Métricas de Rendimiento e Integridad Completas**

| Nombre de la Métrica | Definición/Fórmula | Etapa Medida | Tipo(s) de Datos | Mide (Integridad de...) |
| :--- | :--- | :--- | :--- | :--- |
| **Entropía** | $H(X)=-\sum p(x)log_{2}(p(x))$ | Salida de la Fuente | Todos | Incertidumbre de la fuente |
| **Información Mutua** | $l(X;Y)=H(X)-H(X|Y)$ | Extremo a Extremo | Todos | Transferencia de información |
| **BER** | (Bits erróneos) / (Total de bits) | Salida del Dec. de Canal | Todos | Capa física |
| **PSNR** | $10\log_{10}(MAX_1^2/MSE)$ | Extremo a Extremo | Imagen, Video | Reconstrucción (fidelidad) |
| **SSIM** | Función de $l(x,y)$, $c(x,y)$, $s(x,y)$ | Extremo a Extremo | Imagen, Video | Reconstrucción (perceptual) |
| **PESQ** | Algoritmo ITU-T P.862 | Extremo a Extremo | Audio (Voz) | Reconstrucción (perceptual) |

## Sección 6: Síntesis y Direcciones de Investigación Futuras para la Simulación 6G

Esta sección final resume las capacidades del simulador como una herramienta poderosa para unir la teoría y la práctica. Delinea cómo la arquitectura diseñada puede ser aprovechada para explorar preguntas de investigación abiertas en las comunicaciones 6G, posicionando al simulador no solo como una herramienta de aprendizaje, sino como un motor para la innovación futura.

### 6.1. Síntesis del Rol del Simulador en el Análisis de Sistemas de Comunicación

El simulador está diseñado para modelar y comparar rigurosamente los paradigmas SSCC y JSCC a través de múltiples generaciones tecnológicas (5G/6G) y tipos de datos. Su función principal es servir como una herramienta visual y cuantitativa para demostrar conceptos fundamentales, tales como el contraste entre el efecto acantilado y la degradación gradual, el valor de la información blanda en la decodificación moderna, y los compromisos inherentes entre tasa, distorsión y complejidad. Al hacer estos conceptos teóricos tangibles y observables, el simulador facilita una comprensión más profunda del diseño y las limitaciones de los sistemas de comunicación inalámbrica.

### 6.2. Un Banco de Pruebas para la Investigación y el Desarrollo de 6G

La arquitectura flexible y modular del simulador, particularmente sus bloques exploratorios para "Codificación Semántica" y "DeepJSCC", lo convierte en una plataforma ideal para la investigación en 6G. Dado que DeepJSCC es un campo prometedor pero aún en desarrollo 5, el simulador puede ser utilizado para:

* **Generar puntos de referencia de rendimiento**: Los nuevos modelos reales de DeepJSCC pueden ser comparados con los resultados del modelo funcional del simulador para validar su eficacia.
* **Investigar el impacto de condiciones de canal complejas**: Se puede estudiar el rendimiento de DeepJSCC bajo modelos de canal avanzados que incluyan desvanecimiento complejo, interferencia y movilidad, yendo más allá de los modelos AWGN simples.
* **Explorar sistemas híbridos SSCC/JSCC**: La arquitectura permite investigar esquemas donde la información crítica se envía a través de un robusto SSCC digital, mientras que los datos de mejora de calidad se transmiten a través de un JSCC de degradación gradual.
* **Modelar la comunicación orientada a tareas**: El simulador puede ser extendido para evaluar el éxito de tareas de máquina a máquina, donde la métrica de rendimiento no es el PSNR, sino la tasa de éxito de la tarea (por ejemplo, la precisión de la clasificación de objetos). Esto permite la investigación de sistemas de comunicación verdaderamente semánticos, donde el objetivo final no es la reconstrucción de píxeles, sino la preservación del significado para una aplicación específica.

## Obras citadas

1.  A Comparison of 5G Channel Coding Techniques - ResearchGate, fecha de acceso: octubre 29, 2025, https://www.researchgate.net/publication/355234657 A Comparison of 5G Channel Coding Techniques
2.  Channel Coding Algorithms in NR - 5G | Share Technote, fecha de acceso: octubre 29, 2025, https://www.sharetechnote.com/html/5G/5G_ChannelCoding.html
3.  5G NR Modulation Schemes Guide | PDF - Scribd, fecha de acceso: octubre 29, 2025, https://www.scribd.com/document/669557549/5G-NR-Modulations
4.  5G Modulation and Coding Scheme | 5G MCS - Techplayon, fecha de acceso: octubre 29, 2025, https://www.techplayon.com/5g-nr-modulation-and-coding-scheme-modulation-and-code-rate/
5.  Articulo 1.pdf
6.  Codecs (audio and video encoding) in Mobile Networks, fecha de acceso: octubre 29, 2025, https://mobilepacketcore.com/glossary/codecs-audio-and-video-encoding-in-mobile-networks/
7.  IVAS Codec for the NG 3GPP Voice and Audio Services, fecha de acceso: octubre 29, 2025, https://www.3gpp.org/technologies/ivas-2023
8.  La voz sobre la red móvil 5G o Vo5G (Voice over 5G), fecha de acceso: octubre 29, 2025, https://www.ramonmillan.com/tutoriales/vo5g.php
9.  Versatile Video Coding explained - the future of video in a 5G world - Ericsson, fecha de acceso: octubre 29, 2025, https://www.ericsson.com/en/reports-and-papers/ericsson-technology-review/articles/versatile-video-coding-explained
10. TR 126 955-V17.0.0-5G; Video codec characteristics for 5G-based services and applications (3GPP TR 26.955 version 17.0.0 R - ETSI, fecha de acceso: octubre 29, 2025, https://www.etsi.org/deliver/etsi_tr/126900 126999/126955/17.00.00 60/tr 126955v170000p.pdf
11. ¿Qué es el códec de video HEVC (H.265) y cuáles son sus ventajas? - Dacast, fecha de acceso: octubre 29, 2025, https://www.dacast.com/es/blog-es/hevc-video-codec/
12. How 5G and Advanced Codecs Are Transforming IPTV Users' Experience in the world | by Xtream Online | Sep, 2025 | Medium, fecha de acceso: octubre 29, 2025, https://medium.com/@XtreamOnline/how-5g-and-advanced-codecs-are-transforming-iptv-users-experience-in-the-world-6056ff36e3f1
13. FORMATOS Y CODECS DE VIDEO, BITRATE, RESOLUCION - elitevisión, fecha de acceso: octubre 29, 2025, https://elitevision.es/formatos-codecs-bitrate/
14. New Codecs for 5G, fecha de acceso: octubre 29, 2025, https://dashif.org/docs/workshop-2019/04-thierry%20fautier%20-%20Harmonic%20Codec%20Comparison%205G%20Media%20Workshop Final%20v3.pdf
15. The State of Video Codecs in 2024-Gumlet, fecha de acceso: octubre 29, 2025, https://www.gumlet.com/learn/video-codec/
16. ¿Qué es la teoría de la información? - YouTube, fecha de acceso: octubre 29, 2025, https://www.youtube.com/watch?v=vVokVFHz8uA
17. 5G NR Channel Codes - Article by TELCOMA, fecha de acceso: octubre 29, 2025, https://www.telcomaglobal.com/p/5g-nr-channel-codes
18. 5G New Radio Polar Coding - MATLAB & Simulink - MathWorks, fecha de acceso: octubre 29, 2025, https://www.mathworks.com/help/5g/gs/polar-coding.html
19. 5G/NR Channel Codes Evolution and Recommendation on Polar Codes Techplayon, fecha de acceso: octubre 29, 2025, https://www.techplayon.com/5gnr-channel-codes-evolution-consideration-3gpp-recommendation-polar-codes/
20. Understanding the 5G NR PHY - Tetcos, fecha de acceso: octubre 29, 2025, https://www.tetcos.com/pdf/v13/Experiments/5G-NR-PHY.pdf
21. Teoría de la Información - Modelo de comunicación, fecha de acceso: octubre 29, 2025, https://www.profesores.frc.utn.edu.ar/sistemas/ingcura/Archivos COM/Filminasteorialnfo.pdf
22. Información - Wikipedia, la enciclopedia libre, fecha de acceso: octubre 29, 2025, https://es.wikipedia.org/wiki/Informaci%C3%B3n
23. entropía - Bilateria, fecha de acceso: octubre 29, 2025, https://educacion.bilateria.org/tag/entropia
24. Entropía (información) - Wikipedia, la enciclopedia libre, fecha de acceso: octubre 29, 2025, https://es.wikipedia.org/wiki/Entrop%C3%ADa_(informaci%C3%B3n)
25. www.manuduque.com, fecha de acceso: octubre 29, 2025, https://www.manuduque.com/enciclopedia-ia/informacion-mutua/#:~:text=Definici%C3%B3n%20Formal, X%20y%20YYY%20respectivamente.
26. 9. Teoría de la Información - Parte 2 - INFO239 Comunicaciones, fecha de acceso: octubre 29, 2025, https://phuijse.github.io/UACH-INFO185/clases/unidad1/10 codificaci%C3%B3n_de canal.html
27. Información Mutua - Manu Duque, fecha de acceso: octubre 29, 2025, https://www.manuduque.com/enciclopedia-ia/informacion-mutua/
28. Información mutua - Wikipedia, la enciclopedia libre, fecha de acceso: octubre 29, 2025, https://es.wikipedia.org/wiki/Informaci%C3%B3n_mutua
29. PESQ - Perceptual Evaluation Speech Quality - Opale Systems, fecha de acceso: octubre 29, 2025, https://www.opalesystems.com/Tech-Blog/2-PESQ-Perceptual-Evaluation-Speech-Quality.en.htm
30. Perceptual Audio Testing: Evaluating Voice Quality in APx, fecha de acceso: octubre 29, 2025, https://www.ap.com/news/pesq-perceptual-audio-testing-with-apx
31. Objective Measures of Perceptual Audio Quality Reviewed: An Evaluation of Their Application Domain Dependence - arXiv, fecha de acceso: octubre 29, 2025, https://arxiv.org/pdf/2110.11438
32. 6.2. Objective quality evaluation - Introduction to Speech Processing, fecha de acceso: octubre 29, 2025, https://speechprocessingbook.aalto.fi/Evaluation/Objective_quality_evaluation.html