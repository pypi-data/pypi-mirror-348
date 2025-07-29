import os
import subprocess

def generate_docs(project_path, output_dir="docs/html"):
    doxyfile_path = os.path.join(project_path, "Doxyfile")
    full_output_path = os.path.join(project_path, output_dir)
    os.makedirs(full_output_path, exist_ok=True)

    if not os.path.isfile(doxyfile_path):
        import textwrap
        print("📝 Doxyfile no encontrado. Generando plantilla básica...")
        doxyfile_content = textwrap.dedent(f"""\
            PROJECT_NAME           = "{os.path.basename(project_path)}"
            OUTPUT_DIRECTORY       = {full_output_path}
            INPUT                  = include lib src
            RECURSIVE              = YES
            GENERATE_HTML          = YES
            GENERATE_LATEX         = NO
            QUIET                  = YES
            EXTRACT_ALL            = YES
            FILE_PATTERNS          = *.cpp *.h
            GENERATE_TREEVIEW      = YES
        """)
        with open(doxyfile_path, "w") as f:
            f.write(doxyfile_content)
        print(f"✅ Doxyfile generado: {doxyfile_path}")

    print("📚 Generando documentación con Doxygen...")
    subprocess.run(["doxygen", "Doxyfile"], cwd=project_path, check=True)
    print(f"✅ Documentación generada en {output_dir}")
