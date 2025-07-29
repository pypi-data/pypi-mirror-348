import argparse
from rtos_cli.utils import doxygen_generator

def run():
    parser = argparse.ArgumentParser(description="Genera documentación técnica del proyecto")
    parser.add_argument("--project", required=True, help="Ruta del proyecto")
    parser.add_argument("--output", default="docs/html", help="Directorio de salida")
    args = parser.parse_args()

    doxygen_generator.generate_docs(args.project, output_dir=args.output)
