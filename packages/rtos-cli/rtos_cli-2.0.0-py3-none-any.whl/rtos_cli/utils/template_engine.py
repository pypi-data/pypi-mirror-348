import os
from typing import Dict, List


def parse_template(template_path: str) -> Dict[str, str]:
    """
    Parsea un archivo template que contiene múltiples archivos delimitados por comentarios.
    Retorna un diccionario con la ruta relativa y el contenido generado.
    """
    sections = {}
    current_path = None
    current_lines: List[str] = []

    with open(template_path, 'r') as file:
        for line in file:
            if line.startswith('// ==== FILE:'):
                if current_path and current_lines:
                    sections[current_path] = ''.join(current_lines).strip()
                current_path = line.split(':', 1)[1].strip().strip('=').strip()
                current_lines = []
            else:
                current_lines.append(line)

        if current_path and current_lines:
            sections[current_path] = ''.join(current_lines).strip()

    return sections


def render_template(template_str: str, context: Dict[str, str]) -> str:
    """
    Reemplaza placeholders tipo {{PLACEHOLDER}} por los valores definidos en context.
    """
    for key, value in context.items():
        template_str = template_str.replace(f"{{{{{key}}}}}", value)
    return template_str


def generate_from_template(template_path: str, output_root: str, context: Dict[str, str]) -> List[str]:
    """
    Procesa un template y genera archivos en output_root con el contenido renderizado.
    Retorna una lista con las rutas creadas.
    """
    parsed_sections = parse_template(template_path)
    created_files = []

    for relative_path, content in parsed_sections.items():
        rendered_content = render_template(content, context)
        full_path = os.path.join(output_root, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(rendered_content + '\n')
        created_files.append(full_path)

    return created_files