# Guía de Instalación

## Instalación Básica

### 1. Instalar Dependencias Core (Recomendado)

Estas son las dependencias esenciales para ejecutar el simulador:

```bash
pip install -r requirements.txt
```

### 2. Instalar Interfaz Web (Opcional)

La interfaz web Streamlit es opcional. Si deseas usarla:

#### En Linux/Mac:
```bash
pip install streamlit
```

#### En Windows:

Si encuentras errores de compilación con PyArrow (dependencia de Streamlit), prueba:

**Opción A - Actualizar pip y usar pre-built wheels:**
```bash
python -m pip install --upgrade pip
pip install streamlit --no-build-isolation
```

**Opción B - Instalar PyArrow pre-compilado primero:**
```bash
pip install pyarrow --only-binary=:all:
pip install streamlit
```

**Opción C - Si aún tienes problemas, usa una versión específica:**
```bash
pip install pyarrow==10.0.1
pip install streamlit==1.28.0
```

### 3. Dependencias Opcionales Adicionales

Para características avanzadas (procesamiento de audio/video/imágenes):

```bash
pip install -r requirements-optional.txt
```

## Solución de Problemas Comunes

### Error: "Microsoft Visual C++ is required"

Este error ocurre en Windows cuando se intenta compilar paquetes desde el código fuente.

**Solución 1:** Instalar pre-built wheels (recomendado)
```bash
pip install --upgrade pip wheel setuptools
pip install --only-binary=:all: streamlit
```

**Solución 2:** Instalar Microsoft C++ Build Tools
1. Descargar de: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Instalar "Desktop development with C++"
3. Reiniciar y ejecutar pip install nuevamente

### Error: "cmake not found"

**Solución:** No instalar streamlit, el simulador funciona sin interfaz web
```bash
# Solo dependencias core
pip install -r requirements.txt

# Usar el simulador desde línea de comandos
python main.py
```

### Error: "No module named 'numpy'"

**Solución:** Asegurar que pip está actualizado
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Verificar Instalación

### Verificar Instalación Core:
```bash
python -c "import numpy; import scipy; import matplotlib; print('✓ Core instalado correctamente')"
```

### Verificar Streamlit (si fue instalado):
```bash
python -c "import streamlit; print('✓ Streamlit instalado')"
```

### Ejecutar Tests:
```bash
pytest tests/ -v
```

## Uso Sin Interfaz Web

Si no puedes instalar Streamlit, el simulador funciona perfectamente desde línea de comandos:

```bash
# Ejecutar ejemplos predefinidos
python main.py

# Usar el simulador en tu código Python
python
>>> from src.simulator import CommunicationSimulator
>>> # ... tu código aquí
```

## Instalación en Entorno Virtual (Recomendado)

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Requisitos del Sistema

- **Python:** 3.7 o superior (recomendado 3.8+)
- **RAM:** Mínimo 2GB (recomendado 4GB+)
- **Disco:** 500MB libres para dependencias

## Plataformas Soportadas

- ✅ Linux (todas las distribuciones)
- ✅ macOS (10.14+)
- ✅ Windows 10/11 (con limitaciones en Streamlit)

## Contacto

Si tienes problemas de instalación, consulta:
- `manual-user.md` - Manual de usuario
- `RUNNING.md` - Guía de ejecución
- Issues en GitHub

## Resumen de Comandos

```bash
# Instalación mínima (funciona en todos los sistemas)
pip install -r requirements.txt

# Instalación con interfaz web (puede requerir build tools en Windows)
pip install -r requirements.txt
pip install streamlit

# Instalación completa (todas las características)
pip install -r requirements.txt
pip install -r requirements-optional.txt
```
