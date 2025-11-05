# Guía de Instalación

## ⚠️ IMPORTANTE para Windows

Si estás en Windows y **no tienes Visual Studio o compilador C instalado**, usa este comando:

```bash
pip install --only-binary=:all: -r requirements.txt
```

Esto asegura que solo se instalen versiones pre-compiladas (wheels) que no requieren compilación.

## Instalación Básica

### 1. Instalar Dependencias Core (Recomendado)

Estas son las dependencias esenciales para ejecutar el simulador:

#### Linux/Mac:
```bash
pip install -r requirements.txt
```

#### Windows (sin compilador C):
```bash
# Actualizar pip primero
python -m pip install --upgrade pip

# Instalar solo binarios pre-compilados
pip install --only-binary=:all: -r requirements.txt
```

#### Windows con Python 3.14 (o versiones muy nuevas):

Si usas una versión muy reciente de Python donde aún no hay wheels disponibles:

```bash
# Opción 1: Instalar paquetes individuales con versiones específicas
pip install --only-binary=:all: numpy==1.26.4 scipy==1.11.4 matplotlib==3.8.2 seaborn==0.13.0 pytest==7.4.3 pytest-cov==4.1.0

# Opción 2: Downgrade a Python 3.11 (recomendado para máxima compatibilidad)
# Desinstala Python 3.14 e instala Python 3.11.x desde python.org
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

### Error: "Unknown compiler(s)" o "Could not find Visual Studio"

Este error ocurre cuando pip intenta compilar paquetes desde código fuente en Windows sin compilador C.

**Solución 1:** Usar solo binarios pre-compilados (RECOMENDADO)
```bash
python -m pip install --upgrade pip
pip install --only-binary=:all: -r requirements.txt
```

**Solución 2:** Versiones específicas que tienen wheels
```bash
pip install --only-binary=:all: numpy==1.26.4 scipy==1.11.4 matplotlib==3.8.2 seaborn==0.13.0 pytest==7.4.3 pytest-cov==4.1.0
```

**Solución 3:** Usar Python 3.11 en lugar de 3.14
- Python 3.14 es muy nuevo y algunos paquetes aún no tienen wheels pre-compilados
- Descargar Python 3.11.x de https://www.python.org/downloads/
- Reinstalar con Python 3.11

**Solución 4:** Instalar Microsoft C++ Build Tools (si quieres compilar)
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

- **Python:** 3.8 - 3.12 (recomendado 3.11)
  - ⚠️ Python 3.14 es muy nuevo y algunos paquetes pueden no tener wheels pre-compilados
  - ⚠️ Python 3.7 está deprecated
  - ✅ Python 3.11 ofrece la mejor compatibilidad en Windows
- **RAM:** Mínimo 2GB (recomendado 4GB+)
- **Disco:** 500MB libres para dependencias

## Plataformas Soportadas

- ✅ Linux (todas las distribuciones)
- ✅ macOS (10.14+)
- ✅ Windows 10/11
  - Con Python 3.8-3.12: Totalmente soportado con `--only-binary=:all:`
  - Con Python 3.14: Puede requerir downgrade a 3.11

## Contacto

Si tienes problemas de instalación, consulta:
- `manual-user.md` - Manual de usuario
- `RUNNING.md` - Guía de ejecución
- Issues en GitHub

## Resumen de Comandos

```bash
# LINUX/MAC - Instalación estándar
pip install -r requirements.txt

# WINDOWS - Instalación recomendada (Python 3.8-3.12)
python -m pip install --upgrade pip
pip install --only-binary=:all: -r requirements.txt

# WINDOWS - Si usas Python 3.14 o falla lo anterior
pip install --only-binary=:all: -r requirements-windows.txt

# WINDOWS - Alternativa: Instalar paquetes uno por uno
pip install --only-binary=:all: numpy scipy matplotlib seaborn pytest pytest-cov

# Instalación con interfaz web (opcional, todos los sistemas)
pip install streamlit

# Instalación completa (todas las características opcionales)
pip install -r requirements.txt
pip install -r requirements-optional.txt
```
