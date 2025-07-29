# utils/file_utils.py
"""
@file file_utils.py
@brief Utility functions for file operations in RTOS CLI
@author Efrain Reyes Araujo
@version 1.2.0
@date 2025-05-05
@license MIT
"""
import os
import shutil

def insert_in_file(filepath, content, anchor):
    """
    @brief Insert content below a specific anchor comment in a file
    @param filepath Path to the target file
    @param content Code/content to insert
    @param anchor Marker line to look for
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    new_lines = []
    inserted = False

    for line in lines:
        new_lines.append(line)
        if anchor.strip() in line.strip() and not inserted:
            new_lines.append(content + '\n')
            inserted = True

    with open(filepath, 'w') as f:
        f.writelines(new_lines)

def append_to_file(filepath, content):
    """
    @brief Append content to end of a file
    @param filepath File path to append to
    @param content Text to append
    """
    with open(filepath, 'a') as f:
        f.write(content + '\n')

def create_file(path, content):
    """
    @brief Create a file with given content, or skip if it exists
    @param path Path to create the file at
    @param content Initial file contents
    """
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(content)
    else:
        print(f"⚠️  File '{path}' already exists. Skipped.")


def copy_template_to_project(template_dir, project_name):
    """
    @brief Copia el contenido del directorio o archivo de plantilla al proyecto.
    """
    if os.path.isdir(template_dir):
        for item in os.listdir(template_dir):
            s = os.path.join(template_dir, item)
            d = os.path.join(project_name, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
    elif os.path.isfile(template_dir):
        if not os.path.exists(template_dir):
            raise FileNotFoundError(f"❌ Template file '{template_dir}' not found.")
        dest_path = os.path.join(project_name, os.path.basename(template_dir))
        shutil.copy2(template_dir, dest_path)
    else:
        raise FileNotFoundError(f"❌ Template path '{template_dir}' not found.")
def write_file(path, content):
    """
    @brief Write content to a file (overwrite if exists)
    @param path Path to the file
    @param content Text content to write
    """
    with open(path, 'w') as f:
        f.write(content)

def contains_line(filepath, keyword):
    """
    @brief Check if a given line or keyword exists in the file.
    @param filepath Path to the file.
    @param keyword Keyword or exact string to search.
    @return True if keyword is found, False otherwise.
    """
    if not os.path.exists(filepath):
        return False

    with open(filepath, 'r') as f:
        for line in f:
            if keyword in line:
                return True
    return False        


def insert_comment(filepath, anchor, comment):
    """
    @brief Insert a comment line below a specific anchor comment in a file.
    @param filepath Path to the file.
    @param anchor Anchor comment to look for.
    @param comment Comment line to insert (without //).
    """
    comment_line = f"// {comment}"
    insert_in_file(filepath, comment_line, anchor)


def prepend_to_file(filepath, content):
    """
    @brief Prepend content to the beginning of a file.
    @param filepath Path to the file
    @param content Text to insert at the top of the file
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ File '{filepath}' not found for prepending.")
    
    with open(filepath, 'r') as f:
        existing_content = f.read()
    with open(filepath, 'w') as f:
        f.write(content + '\n' + existing_content)

_event_bit_registry = {}

def get_event_bit_index(topic_name):
    """
    @brief Get a unique bit index (0-23) for a given topic to be used in an EventGroup.
    @param topic_name Name of the topic
    @return Integer bit index
    @note Uses a simple in-memory registry. Should be persisted in a real-world scenario.
    """
    if topic_name in _event_bit_registry:
        return _event_bit_registry[topic_name]
    
    used_bits = set(_event_bit_registry.values())
    for i in range(24):  # ESP32 EventGroup supports up to 24 bits (bit 0 to bit 23)
        if i not in used_bits:
            _event_bit_registry[topic_name] = i
            return i

    raise RuntimeError("❌ No available EventGroup bits. Max 24 topics with event signals.")