import os
from rtos_cli.utils import file_utils, doxygen, readme_updater

def run(lib_name, hal_name):
    """
    Agrega un HAL a una librería existente dentro del proyecto.
    
    :param lib_name: Nombre de la librería a la que se agregará el HAL
    :param hal_name: Nombre del HAL que se agregará
    """
    # Definir las rutas para los archivos de la librería
    lib_path = f"lib/{lib_name}"
    hal_path = f"hal/{hal_name}"

    # Verificar que la librería exista
    if not os.path.isdir(lib_path):
        print(f"❌ La librería '{lib_name}' no existe en la carpeta lib/")
        return

    # Verificar que los archivos del HAL existan directamente
    hal_header = f"hal/{hal_name}.h"
    hal_cpp = f"hal/{hal_name}.cpp"

    if not os.path.isfile(hal_header) or not os.path.isfile(hal_cpp):
        print(f"❌ Los archivos de HAL '{hal_name}' no están completos o no existen.")
        return

    lib_header_path = f"{lib_path}/include/{lib_name}.h"
    lib_source_path = f"{lib_path}/src/{lib_name}.cpp"

    file_utils.insert_in_file(lib_header_path, f"#include \'{hal_name}.h\'", anchor="// -- HAL INCLUDES --")
    file_utils.insert_in_file(lib_source_path, f"#include \'{hal_name}.h\'", anchor="// -- HAL INCLUDES --")

    # Añadir las funciones en la documentación Doxygen
    # TODO

    # Agregar una entrada en el README de la librería
    # TODO

    print(f"✅ HAL '{hal_name}' ha sido agregado correctamente a la librería '{lib_name}'.")