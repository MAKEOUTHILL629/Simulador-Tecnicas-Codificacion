# Cómo Ejecutar la Interfaz Web

## Instalación de Dependencias

### Dependencias Core (Requeridas)
```bash
pip install -r requirements.txt
```

### Interfaz Web (Opcional)
```bash
pip install streamlit
```

**⚠️ Nota para Windows:** Si encuentras errores de compilación (PyArrow, CMake, Visual Studio), consulta `INSTALL.md` para soluciones específicas de Windows.

**Alternativa:** El simulador funciona completamente sin Streamlit usando `python main.py`

## Ejecutar la Aplicación Web

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## Características de la Interfaz

- ⚙️ **Panel de Configuración**: Ajusta todos los parámetros del simulador
- 📊 **Visualización de Resultados**: Métricas en tiempo real
- 💡 **Ayuda Integrada**: Guía de uso y recomendaciones
- 🎨 **Interfaz Intuitiva**: Fácil de usar, no requiere programación

## Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ --cov=src --cov-report=html

# Ejecutar tests específicos
pytest tests/test_simulator.py -v
```

## Ejemplos desde Línea de Comandos

Si prefieres usar la línea de comandos:

```bash
# Ejecutar ejemplos predefinidos
python main.py

# Las gráficas se guardarán en ./plots/
```

## Estructura del Proyecto

```
.
├── app.py              # Interfaz web Streamlit
├── main.py             # Ejemplos de línea de comandos
├── src/                # Código fuente del simulador
├── tests/              # Suite de tests (31 tests)
├── data/               # Datos de prueba
└── plots/              # Gráficas generadas
```

## Solución de Problemas

**Error: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**Error: streamlit command not found**
```bash
pip install streamlit
```

**Puerto ocupado**
```bash
streamlit run app.py --server.port 8502
```

Para más información, consulta `manual-user.md` y `manual-dev.md`.
