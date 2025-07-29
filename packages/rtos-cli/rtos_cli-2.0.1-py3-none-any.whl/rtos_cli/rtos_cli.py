# rtos_cli.py
"""
@file rtos_cli.py
@brief Main CLI entry point for FreeRTOS + PlatformIO project automation
@version 1.2.0
@date 2025-05-05
@license MIT
@author Efrain Reyes Araujo

@details
RTOS CLI automates the setup and extension of FreeRTOS-based ESP32 projects using PlatformIO. It supports:
- Project creation with board configuration
- Task creation with FreeRTOS logic
- Global variable and queue management

@example
    python rtos_cli.py create_project MyProject
    python rtos_cli.py create_task sensor_reader
"""

import argparse
import sys

from rtos_cli.utils import file_utils, readme_updater, doxygen

from rtos_cli.commands import (
    create_project,
    create_hal_i2c,
    create_lib,
    add_hal,
    create_task,
    create_topic,
    create_msg,
    view_graph,
    generate_docs,
    init_project,
)

def main():
    parser = argparse.ArgumentParser(
        description="RTOS CLI - Automate FreeRTOS Project Development (Develop Edition)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create_hal (generalized)
    p_hal_generic = subparsers.add_parser("create_hal", help="Create a generic HAL module")
    p_hal_generic.add_argument("name", help="Name of the HAL to create")
    p_hal_generic.add_argument("--hal_type", default="gpio", help="Type of HAL to base on (e.g., i2c, gpio)")
    p_hal_generic.add_argument("--sda", type=int, help="SDA pin (for i2c)")
    p_hal_generic.add_argument("--scl", type=int, help="SCL pin (for i2c)")
    p_hal_generic.add_argument("--freq", type=int, help="Frequency (for i2c)")

    # create_project
    p_project = subparsers.add_parser("create_project", help="Create a new PlatformIO + FreeRTOS project")
    p_project.add_argument("project_name", nargs="?", help="Name of the new project")
    p_project.add_argument("--yaml", help="YAML file with project definition")

    # create_task
    p_task = subparsers.add_parser("create_task", help="Create a new FreeRTOS task")
    p_task.add_argument("task_name", help="Name of the task to create")

    # create_topic
    p_topic = subparsers.add_parser("create_topic", help="Create a FreeRTOS topic")
    p_topic.add_argument("task_name", help="Name of Task to the create topic")
    p_topic.add_argument("direction", help="Topic type of subscription or publisher")
    p_topic.add_argument("topic_name", help="Name of the topic to create")
    p_topic.add_argument("type", help="Type of data")
    p_topic.add_argument("rate", help="Frecuency of pub/susb of topic")

    # create_hal_i2c
    p_hal = subparsers.add_parser("create_hal_i2c", help="Create a HAL driver")
    p_hal.add_argument("--bus", type=int, default=1, help="Number Bus")
    p_hal.add_argument("--sda", type=int, default=21, help="SDA pin")
    p_hal.add_argument("--scl", type=int, default=22, help="SCL pin")
    p_hal.add_argument("--freq", type=int, default=100000, help="I2C frequency")
    
    # create_lib
    p_lib = subparsers.add_parser("create_lib", help="Create a new reusable library module")
    p_lib.add_argument("domain", help="Domain of the library (e.g., sensor, driver, utility)")
    p_lib.add_argument("device", help="Device or functionality name (e.g., fdc1004, kalman)")

    # add_hal 
    p_add_hal = subparsers.add_parser("add_hal", help="Add a specific Hal into the Library")
    p_add_hal.add_argument("lib_name", help="Name of Library")
    p_add_hal.add_argument("hal_name", help="Name of specific Hal")

    # create_msg
    p_msg = subparsers.add_parser("create_msg", help="Create a new type of message")
    p_msg.add_argument("msg_name", help="Name of type message")

    # view_graph
    p_graph = subparsers.add_parser("view_graph", help="Visualizar el grafo del sistema desde un archivo YAML")
    p_graph.add_argument("--yaml", required=True, help="Ruta del archivo YAML")
    p_graph.add_argument("--output", default="system_graph.png", help="Archivo de salida (.png, .svg, etc)")

    # generate_docs
    p_docs = subparsers.add_parser("generate_docs", help="Genera documentación técnica con Doxygen")
    p_docs.add_argument("--project", required=True, help="Ruta del proyecto")
    p_docs.add_argument("--output", default="docs/html", help="Directorio de salida para documentación")

    # init_project
    p_init = subparsers.add_parser("init_project", help="Inicializa un proyecto completo con estructura CLI + PlatformIO")
    p_init.add_argument("project_name", help="Nombre del proyecto raíz")

    args = parser.parse_args()

    if args.command == "create_project":
        create_project.run(project_name=args.project_name, yaml_path=args.yaml)

    elif args.command == "create_task":
        create_task.run(args.task_name)

    elif args.command == "create_topic":
        create_topic.run(args.task_name, args.direction, args.topic_name, args.type, args.rate)

    elif args.command == "create_hal_i2c":
        create_hal_i2c.run(args.bus, args.sda, args.scl, args.freq)

    elif args.command == "create_lib":
        create_lib.run(args.domain, args.device)

    elif args.command == "add_hal":
        add_hal.run(args.lib_name, args.hal_name)

    elif args.command == "create_msg":
        p_msg.run(args.msg_name)

    elif args.command == "create_hal":
        from rtos_cli.commands import create_hal
        create_hal.run(args.name, hal_type=args.hal_type, sda=args.sda, scl=args.scl, freq=args.freq)

    elif args.command == "view_graph":
        import sys
        sys.argv = ["view_graph", "--yaml", args.yaml, "--output", args.output]
        view_graph.run()

    elif args.command == "generate_docs":
        import sys
        sys.argv = ["generate_docs", "--project", args.project, "--output", args.output]
        generate_docs.run()

    elif args.command == "init_project":
        init_project.run(args.project_name)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()