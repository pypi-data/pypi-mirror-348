import os
import argparse
from rtos_cli.utils import file_utils, doxygen, readme_updater

def run(domain, device):
    """
    Crea una librería modular bajo la convención <domain>_<device>.
    """
    lib_name = f"{domain}_{device}"
    project_root = os.getcwd()
    lib_dir = os.path.join(project_root, "lib", "utils", lib_name)
    include_dir = os.path.join(lib_dir, "include")
    src_dir = os.path.join(lib_dir, "src")

    # Crear estructura de carpetas
    os.makedirs(include_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)

    header_path = os.path.join(include_dir, f"{lib_name}.h")
    source_path = os.path.join(src_dir, f"{lib_name}.cpp")

    # Contenido de la cabecera
    header_guard = f"{lib_name.upper()}_H"
    header_content = f"""#ifndef {header_guard}
#define {header_guard}

#include <Arduino.h>
#include "project_config.h"

// -- HAL INCLUDES --

class {lib_name} {{
public:
    {lib_name}();
    void begin();
    void update();

    // -- PUBLIC METHODS --

private:
    // -- STATIC CONFIGURATION --

    // -- INTERNAL VARIABLES --

    // -- CALLBACKS --
}};

#endif // {header_guard}
"""

    # Contenido del .cpp
    source_content = f"""#include \"{lib_name}.h\""

{lib_name}::{lib_name}() {{
    // Constructor
}}

void {lib_name}::begin() {{
    // Inicialización del dispositivo
}}

void {lib_name}::update() {{
    // Lógica de actualización
}}
"""

    # Escribir archivos
    file_utils.write_file(header_path, header_content)
    # Incluir cabecera general del proyecto y anchors de integración
    file_utils.write_file(source_path, source_content)

    # Agregar documentación Doxygen
    file_utils.prepend_to_file(
        header_path,
        doxygen.generate_header(f"{lib_name}.h", f"Header for {lib_name} library")
    )
    file_utils.prepend_to_file(
        source_path,
        doxygen.generate_header(f"{lib_name}.cpp", f"Source for {lib_name} library")
    )

    # Agregar a README
    readme_updater.append_section(
        f"Librería {lib_name}",
        f"""Esta librería gestiona el dispositivo `{device}` bajo el dominio `{domain}`.

#### Estructura de uso:
```cpp

#include <Arduino.h>
#include "{lib_name}.h"

// -- HAL INCLUDES --

{lib_name} sensor;

void setup() {{
    sensor.begin();
}}

void loop() {{
    sensor.update();
}}
```"""
    )

    print(f"✅ Librería '{lib_name}' creada en lib/utils/{lib_name}/")
