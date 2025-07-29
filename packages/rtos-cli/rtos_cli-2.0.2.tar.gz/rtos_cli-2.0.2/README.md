# RTOS CLI – Automatizador de Proyectos FreeRTOS para ESP32

`rtos_cli` es una herramienta de línea de comandos diseñada para acelerar y estructurar el desarrollo de proyectos basados en FreeRTOS, PlatformIO y ESP32. Permite crear, visualizar, documentar y gestionar tareas, periféricos, mensajes y recursos de sistema en proyectos de firmware embebido.

---

## 🚀 Propósito

Facilitar la creación y mantenimiento de arquitecturas basadas en tareas FreeRTOS, siguiendo principios de diseño inspirados en ROS (tópicos, mensajes, nodos), con soporte para documentación Doxygen, visualización de arquitectura y generación automatizada desde descripciones YAML.

---

## 🎯 Características principales

- Generación automática de estructuras de proyecto PlatformIO (ESP32 + Arduino).
- Creación modular de tareas, tópicos, colas, timers, mutex y otros recursos RTOS.
- Generador de HALs (abstracción de periféricos como I2C, SPI, GPIO, etc).
- Documentación técnica integrada vía Doxygen.
- Visualización de arquitectura basada en YAML mediante grafos.
- Sistema de inicialización de proyectos desde definiciones HDaC (Hardware Description as Code).

---

## 📁 Estructura general

```plaintext
rtos_cli/
├── commands/         # Comandos disponibles en el CLI
├── templates/        # Plantillas base para generar archivos
├── utils/            # Módulos auxiliares internos
├── README.md         # Documentación principal
├── setup.py          # Configuración del paquete
└── rtos_cli.py       # Punto de entrada del CLI
```

---

## 🔧 Estado actual

Esta herramienta está en constante evolución. La versión actual permite:

- Construcción de proyectos a partir de archivos YAML
- Generación automática de documentación y visualización
- Modularidad para escalar y mantener sistemas embebidos complejos

---

## 📌 Próximas mejoras

- Validación estructural del YAML
- Sistema de sincronización incremental de proyectos
- Biblioteca reutilizable de bloques funcionales
- Interfaz web opcional para modelado visual

---

## 🛠️ Requisitos

- Python 3.7+
- PlatformIO
- Doxygen
- Graphviz
- Dependencias: `pyyaml`, `pydot`, `networkx`, `graphviz`, `rtos_cli` (editable)

---

## 📄 Licencia

MIT License © Efraín Reyes Araujo

---

Para conocer más sobre los comandos disponibles o contribuir al proyecto, revisa la documentación técnica o ejecuta:

```bash
rtos_cli --help
```