# HDaC - Hardware Description as Code

Este documento define la estructura y sintaxis del esquema **HDaC (Hardware Description as Code)**, utilizado para declarar requerimientos de sistemas embebidos como proyectos compilables en PlatformIO con ESP32 y FreeRTOS.

---

## 📁 Estructura General del YAML

```yaml
project_name: string             # Nombre del proyecto
description: string             # Descripción del sistema
hardware: string                # Hardware objetivo (ej: esp32-eddie-w)
framework: string               # Framework base. Opciones: [arduino, esp-idf]
rtos: string                    # RTOS utilizado. Opciones: [freertos]

hal:                            # Lista de periféricos HAL. Cada uno con:
  - name: string                # Nombre identificador único
    type: string                # Tipo de HAL. Opciones: [i2c, spi, adc, gpio, pwm]
    pins:                       # Diccionario de pines específicos del HAL
      sda: int
      scl: int
      frequency: int

messages:                       # Lista de estructuras de mensaje:
  - name: string
    fields:
      - field_name: type        # Ej: timestamp: uint32_t

libraries:                       # Librerías externas o internas requeridas
  - name: string
    type: string                # Opciones: [internal, external, builtin]
    include_path: string
    repo: string                # Solo si type == external

globals:                         # Variables globales compartidas entre tareas
  - name: string
    type: string
    access: string              # Opciones: [protected, atomic, unprotected]
    initial_value: any
    shared_by: [string]
    comment: string

tasks:                          # Lista de tareas FreeRTOS (nodos funcionales)
  - name: string
    execution_model: string     # Comportamiento principal. Opciones: [loop, periodic, reactive, oneshot, service]
    interrupt_mode: string      # Solo si execution_model == reactive. Opciones: [discard, restart]
    period_ms: int              # Requerido si execution_model == periodic
    uses: [string]              # HALs o librerías utilizadas
    publishes: [string]         # Mensajes que publica
    subscribes: [string]        # Mensajes que consume (si aplica)
    priority: int
    stack_size: int
```

---

## 🔧 HAL Definitions

Cada HAL define un periférico de hardware abstracto. Ejemplo de un periférico I2C:

```yaml
- name: hal_i2c
  type: i2c
  pins:
    sda:        int
    scl:        int
    frequency:  int
```

---

## 📩 Messages Definitions

Define los mensajes estructurados que las tareas pueden publicar o consumir.

```yaml
- name: temp_data
  fields:
    - timestamp: uint32_t
    - temperature: float
```

---

## 📚 Libraries

Define las librerías externas o internas utilizadas por el sistema. Esta sección es útil para gestionar dependencias y controlar las inclusiones desde el YAML.

```yaml
libraries:
  - name: sensor_bme280
    type: internal    # Opciones: [internal, external]
    include_path: lib/sensor_bme280
    repo: https://github.com/ejemplo/sensor_bme280.git   # Solo si es externa
```

---

## 🧮 Global Variables

Permite declarar variables globales compartidas entre tareas que serán protegidas mediante mecanismos de sincronización de FreeRTOS (mutex, semáforos, etc).

```yaml
globals:
  - name: sensor_status
    type: uint8_t
    access: protected   # Opciones: [protected, atomic, unprotected]
    comment: Estado compartido del sensor entre tareas
```

- `access` define el tipo de protección:
  - `protected`: uso con mutex/semaphore.
  - `atomic`: uso con operaciones atómicas.
  - `unprotected`: sin control de concurrencia (no recomendado).
---

## ⚙️ Task (o Node) Definitions

El campo `execution_model` reemplaza al antiguo `type` para definir el comportamiento principal de la tarea.

### Tipos de ejecución (`execution_model`):

| Tipo         | Descripción |
|--------------|-------------|
| `loop`       | Se ejecuta continuamente; el código interno controla la frecuencia. |
| `periodic`   | Se ejecuta con una frecuencia fija (`period_ms`), medida por temporizador. |
| `reactive`   | Se activa mediante una señal externa o mensaje. Soporta `interrupt_mode`. |
| `oneshot`    | Se ejecuta una única vez (ej. inicialización o evento puntual). |
| `service`    | Espera y responde a peticiones (tipo RPC o comandos). |

### Campo adicional para `reactive`:
- `interrupt_mode: discard | restart`
  - `discard`: ignora nuevas señales mientras se ejecuta.
  - `restart`: interrumpe y reinicia si recibe nueva señal.

Ejemplo:

```yaml
- name: nodo_sensor
  execution_model: periodic
  period_ms: 1000
  uses: [ sensor_bme280 ]
  publishes: [ temp_data ]
  priority: 2
  stack_size: 4096

- name: nodo_control
  execution_model: reactive
  interrupt_mode: restart
  subscribes: [ comando_control ]
  priority: 1
  stack_size: 2048
```

---

## ✅ Ejemplo Completo

```yaml
project_name: sistema_clima
description: Sistema de monitoreo de temperatura y humedad
hardware: esp32-eddie-w
framework: arduino
rtos: freertos

hal:
  - name: hal_i2c
    type: i2c
    pins:
        sda:        21
        scl:        22
        frequency:  400000

messages:
  - name: temp_data
    fields:
      - timestamp: uint32_t
      - temperature: float

  - name: humidity_data
    fields:
      - timestamp: uint32_t
      - humidity: float

libraries:
  - name: sensor_bme280
    type: internal
    include_path: lib/sensor_bme280

globals:
  - name: sensor_ready
    type: bool
    access: atomic
    initial_value: false
    shared_by: [nodo_sensor_bme280, nodo_logger]
    comment: Variable de estado que indica si el sensor está inicializado

tasks:
  - name: nodo_sensor_bme280
    execution_model: periodic
    period_ms: 2000
    uses: [ sensor_bme280, hal_i2c ]
    publishes: [ temp_data, humidity_data ]
    priority: 2
    stack_size: 4096

  - name: nodo_logger
    execution_model: reactive
    interrupt_mode: discard
    subscribes: [ temp_data, humidity_data ]
    priority: 1
    stack_size: 2048
```

---</file>