# rtos_cli/commands/create_topic.py
"""
@file create_topic.py
@brief Command to create a new FreeRTOS topic for a task, enabling publish/subscribe communication between tasks
@version 1.4.0
@date 2025-05-08
@license MIT
"""

import os
from rtos_cli.utils import file_utils, readme_updater, doxygen

def run(task_name, topic_name, direction, msg_name, rate):
    print(f"🔧 Creating topic '{topic_name}' for task '{task_name}' ({direction})...")

    msg_name = msg_name.replace('/', '::')  # Ensure proper C++ namespace syntax

    # Ensure msg_name is valid message type
    if not msg_name:
        print(f"❌ Invalid message type: '{msg_name}'. Must be a valid message name.")
        return

    if direction not in ["pub", "sub"]:
        print(f"❌ Invalid direction: {direction}. Must be 'pub' or 'sub'.")
        return

    topic_var_name = f"{topic_name}_queue"
    func_name = f"{'publish' if direction == 'pub' else 'subscribe'}_{topic_name}"
    set_func = f"set_{task_name}"

    base_path = os.getcwd()
    include_path = os.path.join(base_path, "include")
    src_path = os.path.join(base_path, "src")

    project_config_path = os.path.join(include_path, "project_config.h")
    task_header_path = os.path.join(include_path, f"{task_name}.h")
    task_source_path = os.path.join(src_path, f"{task_name}.cpp")
    main_cpp_path = os.path.join(src_path, "main.cpp")

    # Determine if msg_name is a custom message and get header include
    msg_parts = msg_name.split("::")
    if len(msg_parts) == 2:
        msg_include_path = f'message/{msg_parts[0].lower()}_{msg_parts[1].lower()}.h'
        msg_include_line = f'#include "{msg_include_path}"\n'
    else:
        msg_include_line = ""

    # Handle publication
    if direction == "pub":
        if file_utils.contains_line(project_config_path, topic_var_name):
            print(f"⚠️ Topic '{topic_name}' already declared. Aborting.")
            return

        queue_decl = f"extern QueueHandle_t {topic_var_name};\n"
        queue_def = f"QueueHandle_t {topic_var_name};\n"

        event_group_var_name = f"{topic_name}_event_group"
        event_bit_mask = f"{topic_name.upper()}_BIT"
        event_group_decl = f"extern EventGroupHandle_t {event_group_var_name};\n#define {event_bit_mask} (1 << {file_utils.get_event_bit_index(topic_name)})\n"
        event_group_def = f"EventGroupHandle_t {event_group_var_name};\n"

        file_utils.insert_in_file(project_config_path, queue_decl, "// -- TOPIC QUEUE DECLARATIONS --")
        file_utils.insert_in_file(project_config_path, event_group_decl, "// -- TOPIC QUEUE DECLARATIONS --")
        file_utils.insert_in_file(main_cpp_path, queue_def, "// -- TOPIC QUEUE DEFINITIONS --")
        file_utils.insert_in_file(main_cpp_path, event_group_def, "// -- TOPIC QUEUE DEFINITIONS --")

        func_decl = f"void {func_name}({msg_name} data);\n"
        func_impl = f"""
void {func_name}({msg_name} data) {{
    xQueueSend({topic_var_name}, &data, portMAX_DELAY);
    xEventGroupSetBits({event_group_var_name}, {event_bit_mask});
    Serial.print("[{func_name}] Published: ");
    Serial.println(data.to_string());  // Ensure to_string() exists in msg
}}
"""

        # Insert message include in task header if not already present
        if msg_include_line and not file_utils.contains_line(task_header_path, msg_include_line.strip()):
            file_utils.insert_in_file(task_header_path, msg_include_line, "// -- TASK INCLUDES --")

        doxygen.add_function_description(
            header_path=task_header_path,
            function_name=func_name,
            brief=f"Publish to topic '{topic_name}' using complex message type '{msg_name}'",
            params=[("data", msg_name)],
            returns="void"
        )

        file_utils.insert_in_file(task_header_path, func_decl, "// -- TASK FUNCTION DECLARATIONS --")

        queue_creation = f"""
if ({topic_var_name} == NULL) {{
    {topic_var_name} = xQueueCreate(10, sizeof({msg_name}));
}}
if ({event_group_var_name} == NULL) {{
    {event_group_var_name} = xEventGroupCreate();
}}"""
        file_utils.insert_in_file(task_source_path, queue_creation, "// -- TASK INIT EXTENSIONS --")

    # Handle subscription
    else:
        if not file_utils.contains_line(project_config_path, topic_var_name):
            print(f"❌ Cannot subscribe: queue '{topic_var_name}' not found.")
            return

        func_decl = f"void {func_name}();\n"

        # Insert necessary includes in task header
        if not file_utils.contains_line(task_header_path, '#include "project_config.h"'):
            file_utils.insert_in_file(task_header_path, '#include "project_config.h"', "// -- TASK INCLUDES --")
        if not file_utils.contains_line(task_header_path, '#include "freertos/event_groups.h"'):
            file_utils.insert_in_file(task_header_path, '#include "freertos/event_groups.h"', "// -- TASK INCLUDES --")
        if msg_include_line and not file_utils.contains_line(task_header_path, msg_include_line.strip()):
            file_utils.insert_in_file(task_header_path, msg_include_line, "// -- TASK INCLUDES --")

        func_impl = f"""
void {func_name}() {{
    xEventGroupWaitBits({topic_name}_event_group, {topic_name.upper()}_BIT, pdTRUE, pdFALSE, pdMS_TO_TICKS({rate}));
    {msg_name} data;
    if (xQueueReceive({topic_var_name}, &data, pdMS_TO_TICKS({rate}))) {{
        {set_func}(data.value);  // Optional: implement this in task file
        Serial.print("[{func_name}] Received: ");
        Serial.println(data.to_string());  // Ensure to_string() exists
    }}
}}
"""

        doxygen.add_function_description(
            header_path=task_header_path,
            function_name=func_name,
            brief=f"Subscribe to topic '{topic_name}' using complex message type '{msg_name}'",
            params=[],
            returns="void"
        )

        file_utils.insert_in_file(task_header_path, func_decl, "// -- TOPIC FUNCTION DECLARATIONS --")

    # Insert implementations
    file_utils.insert_in_file(task_source_path, func_impl, "// -- TOPIC FUNCTION DEFINITIONS --")
    # Insert project_config include if missing
    if not file_utils.contains_line(task_source_path, '#include "project_config.h"'):
        file_utils.insert_in_file(task_source_path, '#include "project_config.h"', "// -- TASK INCLUDES --")

    # For publication, ensure function is called in loop (with dummy data)
    if direction == "pub":
        file_utils.insert_in_file(
            task_source_path,
            f"    {func_name}({msg_name}()); // TODO: Replace with actual message construction",
            "// -- TASK LOOP EXTENSIONS --"
        )

    # For subscription, ensure function is called in loop
    if direction == "sub":
        file_utils.insert_in_file(task_source_path, f"    {func_name}();", "// -- TASK LOOP EXTENSIONS --")

    # Update README
    readme_updater.append_section(
        "## Tópicos",
        f"- `{topic_name}` ({direction}) añadido a `{task_name}` (tipo: `{msg_name}`, frecuencia: `{rate}`ms)\n"
    )

    print(f"✅ Topic '{topic_name}' ({direction}) created for task '{task_name}'.")
