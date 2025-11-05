# Notebooks Educativos - Simulador 5G/6G

Este directorio contiene notebooks Jupyter educativos para aprender a usar el simulador de sistemas de comunicación.

## 📚 Notebooks Disponibles

### 1. Introducción al Simulador (`01_Introduccion_Simulador.ipynb`)
**Nivel:** Principiante  
**Duración:** 15-20 minutos  
**Contenido:**
- Instalación y configuración
- Primera simulación simple
- Interpretación de métricas básicas
- Visualización de resultados

### 2. Comparación de Tecnologías (`02_Comparacion_Tecnologias.ipynb`)
**Nivel:** Intermedio  
**Duración:** 25-30 minutos  
**Contenido:**
- Diferencias entre 5G, 5G-Advanced y 6G
- Análisis de throughput vs robustez
- Trade-offs de diseño
- Casos de uso por tecnología

### 3. Análisis de Códigos de Canal (`03_Analisis_Codigos_Canal.ipynb`)
**Nivel:** Intermedio-Avanzado  
**Duración:** 30-35 minutos  
**Contenido:**
- Comparación detallada LDPC vs Polar
- Efecto de diferentes tasas de código
- Análisis de convergencia
- Waterfall curves

### 4. JSCC vs SSCC (`04_JSCC_vs_SSCC.ipynb`)
**Nivel:** Avanzado  
**Duración:** 35-40 minutos  
**Contenido:**
- Fundamentos teóricos de JSCC
- Cliff effect vs graceful degradation
- Análisis cuantitativo comparativo
- Visualizaciones interactivas

## 🚀 Instalación

1. Instalar dependencias básicas del simulador:
```bash
pip install -r ../requirements.txt
```

2. Instalar dependencias para notebooks:
```bash
pip install -r ../requirements-notebooks.txt
```

3. Iniciar Jupyter:
```bash
jupyter notebook
```

## 📖 Orden Recomendado de Lectura

Para obtener el máximo beneficio educativo, recomendamos seguir este orden:

1. **Principiantes**: Empezar con el Notebook 1
2. **Usuarios con conocimientos básicos**: Notebooks 1 → 2 → 3
3. **Usuarios avanzados**: Todos los notebooks en orden
4. **Investigadores**: Enfocarse en Notebooks 3 y 4

## 🎯 Objetivos de Aprendizaje

Al completar todos los notebooks, serás capaz de:

- ✅ Configurar y ejecutar simulaciones de sistemas de comunicación
- ✅ Interpretar métricas de rendimiento (BER, PSNR, SSIM, etc.)
- ✅ Comparar diferentes tecnologías y esquemas
- ✅ Analizar códigos de canal y modulaciones
- ✅ Entender conceptos avanzados como JSCC
- ✅ Generar visualizaciones profesionales
- ✅ Exportar y analizar resultados

## 💡 Requisitos Previos

### Para Notebook 1:
- Conocimientos básicos de Python
- Conceptos básicos de comunicaciones digitales

### Para Notebooks 2-3:
- Todo lo anterior +
- Familiaridad con modulación digital
- Conocimientos de teoría de la información

### Para Notebook 4:
- Todo lo anterior +
- Conocimientos avanzados de codificación
- Familiaridad con teoría de la información avanzada

## 🛠️ Solución de Problemas

### Jupyter no inicia
```bash
# Verificar instalación
jupyter --version

# Reinstalar si es necesario
pip install --upgrade jupyter
```

### Kernel no encontrado
```bash
# Instalar kernel de Python
python -m ipykernel install --user
```

### Importaciones fallan
```bash
# Asegurarse de estar en el directorio correcto
cd /path/to/Simulador-Tecnicas-Codificacion

# Verificar que todos los módulos estén instalados
pip install -r requirements.txt
pip install -r requirements-notebooks.txt
```

## 📊 Datos de Ejemplo

Los notebooks utilizan los datasets de ejemplo en el directorio `../data/`:
- Texto: `data/text/sample_text.txt`
- Imagen: `data/image/sample_image.npy`
- Audio: `data/audio/sample_audio.npy`
- Video: `data/video/sample_video.npy`

## 🤝 Contribuciones

Si deseas contribuir con nuevos notebooks educativos:

1. Seguir el formato numerado existente
2. Incluir objetivos de aprendizaje claros
3. Proporcionar código ejecutable con explicaciones
4. Agregar visualizaciones interactivas
5. Actualizar este README

## 📞 Soporte

Para preguntas o problemas:
- Ver documentación principal en `../manual-user.md`
- Consultar guía de desarrollador en `../manual-dev.md`
- Revisar ejemplos en `../main.py` y `../examples_advanced.py`

## 📝 Notas

- Los notebooks están diseñados para ejecutarse en orden
- Cada notebook tarda 15-40 minutos en completarse
- Se recomienda ejecutar las celdas en orden secuencial
- Algunas simulaciones pueden tardar varios minutos
- Los resultados pueden variar ligeramente debido a la aleatoriedad

---

**¡Disfruta aprendiendo sobre sistemas de comunicación 5G/6G!** 🎓
