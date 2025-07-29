import argparse
from rtos_cli.utils import yaml_loader, graph_builder

def run():
    parser = argparse.ArgumentParser(description="Visualiza el grafo del sistema desde un archivo YAML HDaC")
    parser.add_argument('--yaml', required=True, help='Ruta del archivo YAML')
    parser.add_argument('--output', default='system_graph.png', help='Archivo de salida (.png, .svg, etc)')
    args = parser.parse_args()

    data = yaml_loader.load_project_description(args.yaml)
    graph = graph_builder.build_graph_from_yaml(data)
    graph.write(args.output, format=args.output.split('.')[-1])

    print(f"✅ Grafo generado exitosamente: {args.output}")