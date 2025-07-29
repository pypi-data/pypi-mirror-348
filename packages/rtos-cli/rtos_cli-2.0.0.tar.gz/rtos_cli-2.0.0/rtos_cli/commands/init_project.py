import os
import subprocess
import sys
from pathlib import Path

def to_camel_case(name: str) -> str:
    return ''.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())

def run(project_name):
    raw_name = project_name
    project_root = Path(f"{to_camel_case(raw_name)}_Project").resolve()
    yaml_name = f"{raw_name.lower()}.yaml"
    yaml_path = project_root / yaml_name

    print(f"🚀 Creando estructura base en: {project_root}")
    project_root.mkdir(parents=True, exist_ok=True)
    os.chdir(project_root)

    # Crear entorno virtual
    print("🐍 Creando entorno virtual...")
    subprocess.run(["python3", "-m", "venv", "venv"], check=True)

    activate = project_root / "venv/bin/activate"
    if not activate.exists():
        print("❌ No se pudo crear el entorno virtual.")
        sys.exit(1)

    # Crear requirements.txt
    print("📄 Creando requirements.txt...")
    with open("requirements.txt", "w") as f:
        f.write("rtos_cli\npyyaml\npydot\n")

    # Instalar dependencias
    print("📦 Instalando dependencias en entorno virtual...")
    subprocess.run("source venv/bin/activate && pip install -r requirements.txt", shell=True, executable="/bin/bash", check=True)

    # Crear carpetas auxiliares
    print("📂 Creando carpetas: docs/, graphs/, platformio_project/")
    (project_root / "docs").mkdir(exist_ok=True)
    (project_root / "graphs").mkdir(exist_ok=True)
    platformio_dir = project_root / "platformio_project"
    platformio_dir.mkdir(exist_ok=True)

    # Crear archivo YAML
    print(f"📝 Creando archivo de definición YAML: {yaml_path.name}")
    yaml_path.touch()

    # Ejecutar create_project con YAML
    print("⚙️ Generando proyecto PlatformIO...")
    subprocess.run(f"source venv/bin/activate && rtos_cli create_project --yaml {yaml_path}", shell=True, executable="/bin/bash", check=True)

    # Mover carpeta generada por create_project al subdirectorio
    generated_folder = Path(yaml_path.stem)
    if generated_folder.exists() and generated_folder.is_dir():
        subprocess.run(["mv", str(generated_folder), str(platformio_dir / generated_folder.name)], check=True)

    # Generar grafo
    print("🧠 Generando grafo del sistema...")
    subprocess.run(f"source venv/bin/activate && rtos_cli view_graph --yaml {yaml_path} --output graphs/system_graph.svg", shell=True, executable="/bin/bash", check=True)

    # Generar documentación
    print("📚 Generando documentación técnica...")
    doc_project_path = platformio_dir / generated_folder.name if (platformio_dir / generated_folder.name).exists() else platformio_dir
    subprocess.run(f"source venv/bin/activate && rtos_cli generate_docs --project {doc_project_path} --output docs/html", shell=True, executable="/bin/bash", check=True)

    print(f"✅ Proyecto {raw_name} inicializado correctamente en {project_root}")

if __name__ == "__main__":
    run()