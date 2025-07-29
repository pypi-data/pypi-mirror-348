# RTOS CLI - Ayuda de Comandos

Este documento describe el uso de cada comando disponible en `rtos_cli.py`, la herramienta CLI para automatizar proyectos PlatformIO + FreeRTOS personalizados para el ESP32.

---

## Notas Generales

* Todos los cambios se integran automáticamente al proyecto existente.
* Se actualiza `README.md`, `platformio.ini` y `project_config.h` si aplica.
* Todas las funciones incluyen documentación tipo Doxygen.

---

Para obtener ayuda directamente desde CLI:

```bash
python rtos_cli.py --help
```


## Comandos Disponibles

### `create_project <project_name>`

Crea una estructura completa de proyecto PlatformIO + FreeRTOS para ESP32.

* Utiliza la placa `esp32-eddie-w.json`.
* Estructura carpetas, `platformio.ini`, `README.md`, y archivos base.

**Ejemplo:**

```bash
python rtos_cli.py create_project MiProyecto
```

---

### `create_task <task_name>`

Crea una tarea de FreeRTOS con archivos `.cpp` y `.h`, y la integra al proyecto.

**Ejemplo:**

```bash
python rtos_cli.py create_task sensor_reader
```

---

### `create_topic <task_name> <topic_name> <direction> <type> <rate>`

Crea un tópico de comunicación entre tareas tipo Publisher/Subscriber basado en colas de FreeRTOS.

* `direction`: puede ser `pub` (publicador) o `sub` (suscriptor).
* `type`: tipo de dato del tópico (e.g., `float`, `int`, etc).
* `rate`: intervalo de operación del tópico en milisegundos (usado como guía para la frecuencia de uso).

Este comando inserta automáticamente:

- Declaración de la cola asociada en `project_config.h`.
- Funciones `publish_<topic>()` y/o `subscribe_<topic>()` en `.cpp` y `.h` de la tarea correspondiente.
- Llamadas básicas de prueba al publicar y/o suscribir dentro del bucle `loop` de la tarea.
- Comentarios tipo Doxygen en cada función creada.
- Entrada en `README.md` del proyecto de destino.

**Ejemplos:**

```bash
python rtos_cli.py create_topic sensor_1 temperatura pub float 500
python rtos_cli.py create_topic actuador_1 temperatura sub float 500
```

---

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