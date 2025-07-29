# rtos_cli/commands/create_project.py
"""
@file create_project.py
@brief Command to create a new PlatformIO project for ESP32 Eddie-W board.
@author Innervycs
@version 1.2.0
@date 2025-05-05
@license MIT
"""
import os
import shutil
from rtos_cli.utils import file_utils, readme_updater
from rtos_cli.utils import yaml_loader

from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

BOARD_JSON = """
{
  "build": {
    "arduino": {
      "ldscript": "esp32_out.ld"
    },
    "core": "esp32",
    "extra_flags": "-DARDUINO_ESP32_DEV",
    "f_cpu": "240000000L",
    "f_flash": "80000000L",
    "flash_mode": "qio",
    "hwids": [["0x0403", "0x6010"]],
    "mcu": "esp32",
    "variant": "esp32"
  },
  "connectivity": ["wifi", "bluetooth", "ethernet", "can"],
  "debug": {
    "default_tool": "ftdi",
    "onboard_tools": ["ftdi"],
    "openocd_board": "esp32-wrover.cfg"
  },
  "frameworks": ["arduino", "espidf"],
  "name": "MetaBridge Eddie W",
  "upload": {
    "flash_size": "16MB",
    "maximum_ram_size": 8388608,
    "maximum_size": 16777216,
    "protocols": ["esptool", "espota", "ftdi"],
    "require_upload_port": true,
    "speed": 921600
  },
  "url": "https://innervycs.com/",
  "vendor": "..."
}
"""

def run(project_name=None, yaml_path=None):
    if yaml_path:
        project_desc = yaml_loader.load_project_description(yaml_path)
        project_name = project_desc.get("project_name", None)
        print(f"\n🚀 Creating PlatformIO project from YAML '{yaml_path}' with project name '{project_name}'...")
    else:
        print(f"\n🚀 Creating PlatformIO project '{project_name}'...")

    if not project_name:
        raise ValueError("Project name must be specified either directly or via YAML file.")

    os.makedirs(project_name, exist_ok=True)

    subdirs = ["src", "include", "lib", "test", "boards"]
    for d in subdirs:
        os.makedirs(os.path.join(project_name, d), exist_ok=True)

    # Crear carpetas base para librerías organizadas
    lib_subdirs = ["hals", "sensors", "messages", "utils"]
    for sub in lib_subdirs:
        base_path = os.path.join(project_name, "lib", sub)
        os.makedirs(os.path.join(base_path), exist_ok=True)
        with open(os.path.join(base_path, "README.md"), "w") as f:
            f.write(f"# {sub.capitalize()} Libraries\n\nThis directory contains {sub} libraries.")

    # Crear librería std_msgs dentro de message/
    std_msgs_dir = os.path.join(project_name, "lib", "messages", "std_msgs")
    std_msgs_src = os.path.join(std_msgs_dir, "src")
    std_msgs_inc = os.path.join(std_msgs_dir, "include")
    os.makedirs(std_msgs_src, exist_ok=True)
    os.makedirs(std_msgs_inc, exist_ok=True)

    # Copiar los archivos de mensajes estándar (plantillas) desde los templates
    base_msgs = {
        "std_msgs.h": std_msgs_inc,
        "std_msgs.cpp": std_msgs_src
    }
    for msg_file, dest_dir in base_msgs.items():
        src = TEMPLATE_DIR / "lib" / "messages" / msg_file
        if not src.exists():
            raise FileNotFoundError(f"Template not found: {src}")
        file_utils.copy_template_to_project(str(src), dest_dir)

    # Copiar library.json una única vez
    lib_json_src = TEMPLATE_DIR / "lib" / "messages" / "library.json"
    if lib_json_src.exists():
        file_utils.copy_template_to_project(str(lib_json_src), std_msgs_dir)

    # Write board JSON
    board_path = os.path.join(project_name, "boards", "esp32-eddie-w.json")
    with open(board_path, "w") as f:
        f.write(BOARD_JSON)

    # Copy template files with correct subdirectories
    templates = [
        ("platformio.ini", ""),
    ]
    for template_file, subdir in templates:
        template_path = TEMPLATE_DIR / template_file
        file_utils.copy_template_to_project(str(template_path), os.path.join(project_name, subdir))

    # Copy main.cpp from templates
    file_utils.copy_template_to_project(str(TEMPLATE_DIR / "src" / "main.cpp"), os.path.join(project_name, "src"))
    # Incluir la librería message/standard en main.cpp
    file_utils.insert_in_file(os.path.join(project_name, "src", "main.cpp"),
                              '#include "std_msgs/std_msgs.h"',
                              anchor="// -- INCLUDES HAL --")

    # Copy project_config.h from templates
    file_utils.copy_template_to_project(str(TEMPLATE_DIR / "include" / "project_config.h"), os.path.join(project_name, "include"))
    # Incluir la librería message/standard en project_config.h
    file_utils.insert_in_file(os.path.join(project_name, "include", "project_config.h"),
                              '#include "std_msgs/std_msgs.h"',
                              anchor="; -- INCLUDES HAL --")
    
    ini_path = os.path.join(project_name, "platformio.ini")
    file_utils.insert_in_file(ini_path, "   -Iinclude", anchor="; -- INCLUDES HAL --")
    file_utils.insert_in_file(ini_path, "   -Ilib/message/std_msgs/include", anchor="; -- INCLUDES MESSAGE --")

    # Copy .gitignore if it exists in templates
    gitignore_src = TEMPLATE_DIR / ".gitignore"
    if gitignore_src.exists():
        shutil.copy(gitignore_src, os.path.join(project_name, ".gitignore"))

    # README.md
    readme_path = os.path.join(project_name, "README.md")
    with open(readme_path, "w") as f:
        f.write(f"# {project_name}\n\nGenerated with `rtos_cli` for ESP32 Eddie-W.\n")
    with open(readme_path, "a") as f:
        f.write("Includes default message types (e.g., `std_msgs`) under `lib/message/std`.\n")

    print("✅ Project created successfully.")

    if yaml_path:
        create_hals(project_name, project_desc["hal"])
        create_libraries(project_name, project_desc["libraries"])
        create_globals(project_name, project_desc["globals"])
        create_messages(project_name, project_desc["messages"])
        create_tasks(project_name, project_desc["tasks"])


# Funciones auxiliares para crear componentes definidos en el YAML
def create_hals(project_path, hal_list):
    """Crea HALs definidos en el archivo YAML."""
    if not hal_list:
        return
    print("🧩 Creando HALs... (pendiente de implementación)")

def create_libraries(project_path, libraries):
    """Descarga o incluye librerías externas o internas."""
    if not libraries:
        return
    print("📚 Incluyendo librerías... (pendiente de implementación)")

def create_globals(project_path, globals_list):
    """Declara variables globales con mecanismos de protección."""
    if not globals_list:
        return
    print("🧠 Definiendo variables globales... (pendiente de implementación)")

def create_messages(project_path, messages):
    """Genera estructuras de mensajes tipo ROS."""
    if not messages:
        return
    print("📦 Generando mensajes... (pendiente de implementación)")

def create_tasks(project_path, tasks):
    """Genera tareas o nodos FreeRTOS."""
    if not tasks:
        return
    print("⚙️ Generando tareas... (pendiente de implementación)")