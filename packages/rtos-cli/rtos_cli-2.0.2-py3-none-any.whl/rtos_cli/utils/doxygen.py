# utils/doxygen.py
"""
@file doxygen.py
@brief Utility to generate Doxygen-compatible documentation blocks
@version 1.0.0
@date 2025-05-05
@license MIT
@author Efrain Reyes Araujo
"""

def generate_header(filename, description, author=" ... ", version="1.0.0", date="2025-05-05"):
    return f"""/**
 * @file {filename}
 * @brief {description}
 * @author {author}
 * @version {version}
 * @date {date}
 * @license MIT
 */
"""

def generate_task_doc(task_name):
    """
    @brief Generate a Doxygen block for a FreeRTOS task
    @param task_name Name of the task
    @return str - Doxygen formatted string
    """
    return f"""/**
 * @brief Task {task_name}
 * @details FreeRTOS task created by RTOS CLI.
 *
 * @return void
 */"""

def generate_variable_doc(var_name, var_type):
    """
    @brief Generate a Doxygen comment for a global variable
    @param var_name Variable name
    @param var_type Type of the variable
    @return str - Doxygen formatted comment
    """
    return f"""/**
 * @brief Global variable '{var_name}' of type '{var_type}'
 */"""

def generate_queue_doc(queue_name, item_type, length):
    """
    @brief Generate a Doxygen comment for a FreeRTOS queue
    @param queue_name Queue name
    @param item_type Type of items in the queue
    @param length Queue length
    @return str - Doxygen comment block
    """
    return f"""/**
 * @brief Queue '{queue_name}'
 * @details Queue of type {item_type} with length {length}.
 */"""

def add_function_description(header_path, function_name, brief, params=None, returns="void"):
    """
    @brief Insert a Doxygen function description into a header file
    @param header_path Path to the header file
    @param function_name Name of the function to describe
    @param brief Short description of the function
    @param params List of tuples: (param_name, param_type)
    @param returns Return type of the function
    """
    doc = f"/**\n * @brief {brief}\n"
    if params:
        for name, typ in params:
            doc += f" * @param {name} {typ}\n"
    doc += f" * @return {returns}\n */\n"

    # Insert before the function declaration
    with open(header_path, "r") as f:
        lines = f.readlines()

    with open(header_path, "w") as f:
        inserted = False
        for line in lines:
            if function_name in line and not inserted:
                f.write(doc)
                inserted = True
            f.write(line)
def add_section_comment(title, description=None):
    """
    @brief Generate a Doxygen-style section comment.
    @param title Section title
    @param description Optional multiline description
    @return A formatted string ready to be inserted in a file.
    """
    comment = "/**\n"
    comment += f" * @section {title}\n"
    if description:
        for line in description.split('\n'):
            comment += f" * {line}\n"
    comment += " */\n"
    return comment