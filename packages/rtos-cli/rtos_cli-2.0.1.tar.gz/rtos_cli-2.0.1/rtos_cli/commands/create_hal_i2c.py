import os
from rtos_cli.utils import file_utils, readme_updater, doxygen

def run(bus_number, sda, scl, freq ):
    """
    Crea e integra el módulo HAL para I2C en el proyecto RTOS.
    Este comando:
        - Inserta definiciones en project_config.h
        - Crea los archivos hal_i2c.cpp y hal_i2c.h desde plantillas
        - Agrega documentación Doxygen
        - Actualiza el README.md
    """
    project_root = os.getcwd()
    include_dir = os.path.join(project_root, "include")
    src_dir = os.path.join(project_root, "src")
    project_config_path = os.path.join(include_dir, "project_config.h")

    hal_basename = f"hal_i2c_bus{bus_number}"

    # Definiciones de constantes I2C
    constants = [
        f"#define HAL_I2C_B{bus_number}_SDA {sda}  // Pin SDA",
        f"#define HAL_I2C_B{bus_number}_SCL {scl}  // Pin SCL",
        f"#define HAL_I2C_B{bus_number}_FREQUENCY {freq}  // Frecuencia del bus I2C"
    ]
    for line in constants:
        file_utils.insert_in_file(project_config_path, line, anchor="// -- GLOBAL CONSTANTS --")

    # Agregar include al archivo project_config.h
    # Removed as per instructions

    # Leer las plantillas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, "..", "templates", "hal")

    hal_root_dir = os.path.join(project_root, "lib", "hal", hal_basename)
    hal_src_dir = os.path.join(hal_root_dir, "src")
    hal_include_dir = os.path.join(hal_root_dir, "include")
    os.makedirs(hal_src_dir, exist_ok=True)
    os.makedirs(hal_include_dir, exist_ok=True)

    hal_cpp_path = os.path.join(hal_src_dir, f"{hal_basename}.cpp")
    hal_h_path = os.path.join(hal_include_dir, f"{hal_basename}.h")

    with open(os.path.join(templates_dir, "hal_i2c.cpp"), "r") as f:
        cpp_content = f.read() \
            .replace("{sda}", str(sda)) \
            .replace("{scl}", str(scl)) \
            .replace("{bus}", str(bus_number)) \
            .replace("hal_i2c", hal_basename)
    with open(os.path.join(templates_dir, "hal_i2c.h"), "r") as f:
        h_content = f.read() \
            .replace("{sda}", str(sda)) \
            .replace("{scl}", str(scl)) \
            .replace("{bus}", str(bus_number)) \
            .replace("hal_i2c", hal_basename)

    file_utils.write_file(hal_cpp_path, cpp_content)
    file_utils.write_file(hal_h_path, h_content)

    # Documentación Doxygen en project_config.h
    section_comment = doxygen.add_section_comment("Configuración I2C", "Constantes definidas para el uso del bus I2C.")
    file_utils.insert_in_file(
        project_config_path,
        section_comment,
        anchor="// -- GLOBAL CONSTANTS --"
    )

    # Actualizar README del proyecto
    readme_path = os.path.join(project_root, "README.md")
    readme_updater.append_section(
        "HAL I2C",
        """Se agregó soporte para HAL I2C con configuración SDA/SCL/Frecuencia.

#### Ejemplo de uso en una tarea:

```cpp
#include "hal_i2c.h"

void my_task_loop() {
    uint8_t data[2];
    if (hal_i2c_read(0x3C, data, sizeof(data))) {
        Serial.printf("Read success: %02X %02X\\n", data[0], data[1]);
    }
}
```

> ⚠️ Nota: Las tareas o librerías que necesiten usar el HAL deben incluir explícitamente el archivo correspondiente, por ejemplo:

```cpp
#include <hal_i2c_serial_20_21.h>
```
"""
    )
    # Actualizar platformio.ini
    ini_path = os.path.join(project_root, "platformio.ini")
    file_utils.insert_in_file(ini_path, "   -Ihal", anchor="; -- INCLUDES HAL --")

    print(f"✅ HAL I2C creado e integrado correctamente.")