import os
import yaml

def load_project_description(path):
    """
    Carga y valida un archivo HDaC YAML, devolviendo un diccionario estructurado.

    Args:
        path (str): Ruta absoluta o relativa del archivo YAML.

    Returns:
        dict: Estructura HDaC cargada

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo no tiene los campos mínimos requeridos
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Archivo YAML no encontrado: {path}")

    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error al parsear YAML: {e}")

    # Validación básica mínima
    required_fields = ["project_name", "hardware", "framework", "rtos"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"El campo obligatorio '{field}' no está definido en el YAML")

    # Normalizar claves opcionales si no existen
    data.setdefault("hal", [])
    data.setdefault("messages", [])
    data.setdefault("tasks", [])
    data.setdefault("libraries", [])
    data.setdefault("globals", [])

    return data