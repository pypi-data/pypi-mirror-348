# rtos_cli/commands/create_msg.py
"""
@file create_msg.py
@brief Command to create a new Type of Message
@version 1.4.0
@date 2025-05-08
@license MIT
"""

import os
from rtos_cli.utils.file_utils import create_file
from rtos_cli.utils.naming import to_snake_case, to_pascal_case
from rtos_cli.utils.readme_updater import add_to_readme_section

def run_create_msg(project_path, msg_name):
    """
    @brief Crea un nuevo tipo de mensaje con su estructura base y documentación
    @param project_path Ruta raíz del proyecto
    @param msg_name Nombre del mensaje a crear (ej. Float32)
    """
    # Ruta del directorio para los mensajes (directamente en lib/message)
    msg_dir = os.path.join(project_path, "lib", "message")
    include_dir = os.path.join(msg_dir, "include")
    src_dir = os.path.join(msg_dir, "src")
    os.makedirs(include_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)

    class_name = to_pascal_case(msg_name)
    snake_name = to_snake_case(msg_name)
    h_path = os.path.join(include_dir, f"{class_name}.h")
    cpp_path = os.path.join(src_dir, f"{class_name}.cpp")

    # Código para el archivo header (.h)
    header_code = f"""\
/**
 * @file {class_name}.h
 * @brief Definición del mensaje {class_name}
 * @author Efrain
 * @date 2025-05-13
 */

#ifndef _{class_name.upper()}_H_
#define _{class_name.upper()}_H_

#include <Arduino.h>

/**
 * @brief Estructura de mensaje {class_name}
 *        Incluye timestamp y campo de dato. Expande según necesidades.
 */
class {class_name} {{
public:
    uint32_t timestamp_ms;  ///< Marca de tiempo (ms)
    float value;            ///< Valor simple (ej. lectura de sensor)

    {class_name}();
    String to_string() const;
}};

#endif  // _{class_name.upper()}_H_
"""

    # Código para el archivo source (.cpp)
    cpp_code = f"""\
#include "{class_name}.h"

{class_name}::{class_name}() {{
    timestamp_ms = millis();
    value = 0.0f;
}}

String {class_name}::to_string() const {{
    return "[timestamp: " + String(timestamp_ms) + ", value: " + String(value, 2) + "]";
}}
"""

    # Crear los archivos
    create_file(h_path, header_code)
    create_file(cpp_path, cpp_code)

    # Actualizar README con la información del nuevo tipo de mensaje
    add_to_readme_section(
        os.path.join(project_path, "README.md"),
        "## Tipos de Mensaje",
        f"- `{class_name}` generado en `lib/message/`"
    )

    # Si la carpeta lib/message no está en platformio.ini, agregarla
    platformio_ini_path = os.path.join(project_path, "platformio.ini")
    if os.path.exists(platformio_ini_path):
        with open(platformio_ini_path, 'r') as file:
            lines = file.readlines()
        if 'lib_deps = ' not in ''.join(lines):
            with open(platformio_ini_path, 'a') as file:
                file.write("\nlib_deps = \n\tmessage\n")  # Agregar la ruta de la librería si no existe

    library_json_path = os.path.join(msg_dir, "library.json")
    if not os.path.exists(library_json_path):
        with open(library_json_path, "w") as f:
            f.write('{\n  "name": "message",\n  "version": "1.0.0",\n  "description": "Base message types for RTOS projects."\n}')

    print(f"✅ Mensaje {class_name} creado exitosamente en lib/message/")