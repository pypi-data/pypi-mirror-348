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
