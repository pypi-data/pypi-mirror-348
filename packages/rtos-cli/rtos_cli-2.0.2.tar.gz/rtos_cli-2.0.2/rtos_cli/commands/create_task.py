# rtos_cli/commands/create_task.py
"""
@file create_task.py
@brief Command to create a new FreeRTOS task with .cpp/.h files, registration in main.cpp, and configuration in project_config.h following the rtos_cli architecture and conventions.
@author Efrain Reyes Araujo
@version 1.2.0
@date 2025-05-05
@license MIT
"""
import os
import re
from rtos_cli.utils import file_utils, readme_updater, doxygen

def run(task_name, stack_size=4096, priority=1):
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', task_name):
        print("❌ Invalid task name. Use only letters, numbers, and underscores, and do not start with a number.")
        return

    print(f"\n🔧 Creating task '{task_name}'...")

    src_path = os.path.join("src", f"{task_name}.cpp")
    include_path = os.path.join("include", f"{task_name}.h")

    if os.path.exists(src_path) or os.path.exists(include_path):
        print(f"⚠️ Task '{task_name}' already exists.")
        return


    # Template contents for .cpp and .h
    h_content = f"""{doxygen.generate_header(f"{task_name}.h", f"Header for {task_name} task")}
#ifndef {task_name.upper()}_H
#define {task_name.upper()}_H

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/semphr.h>
#include <freertos/queue.h>

#ifdef __cplusplus
extern "C" {{
#endif

// -- TASK SHARED VARIABLES --


// -- TASK FUNCTION DECLARATIONS --


// -- TOPIC FUNCTION DECLARATIONS --


// Shared handles
extern SemaphoreHandle_t x{task_name}Mutex;
extern QueueHandle_t x{task_name}Queue;
// extern EventGroupHandle_t x{task_name}EventGroup;  // Optional event group
// extern TimerHandle_t x{task_name}Timer;            // Optional software timer

// Task declaration
void {task_name}_task(void *pvParameters);

// Accessor functions
int get_{task_name.lower()}();
void set_{task_name.lower()}(int value);

// Optional loop function for test or modular execution
void {task_name}_loop();

// -- TASK INTERNAL STATE --
#ifdef __cplusplus
}}
#endif

#endif  // {task_name.upper()}_H
"""

    cpp_content = f"""{doxygen.generate_header(f"{task_name}.cpp", f"Implementation of {task_name} task")}
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/semphr.h>
#include <freertos/queue.h>
#include "{task_name}.h"
#include "project_config.h"
#include <stdio.h>
#include <Arduino.h>

// -- INCLUDES --

// ========================
// 🔧 Topics
// ========================
// -- TOPIC FUNCTION DEFINITIONS --

// -- TOPIC FUNCTION DECLARATIONS --

// ========================
// 🔧 Shared Resources
// ========================
SemaphoreHandle_t x{task_name}Mutex = NULL;
QueueHandle_t x{task_name}Queue = NULL;
// EventGroupHandle_t x{task_name}EventGroup = NULL;  // Optional: Create in init if needed
// TimerHandle_t x{task_name}Timer = NULL;            // Optional: Define callback and init

// -- TASK SHARED RESOURCES --

// ========================
// 📦 Internal Variables
// ========================
static int {task_name.lower()}_value = 0;
static int {task_name.lower()}_status = 0;
static bool {task_name.lower()}_ready = false;
static float {task_name.lower()}_average = 0.0f;

// -- TASK INTERNAL VARIABLES --

// ========================
// 🔍 Internal Functions
// ========================
static int read_{task_name.lower()}_raw();
static int process_{task_name.lower()}(int raw);

// -- TASK INTERNAL FUNCTIONS --

// ========================
// 🔁 Task Loop Function
// ========================
void {task_name}_loop() {{
    printf("[%.3f] [{task_name}] Running loop\\n", (double)(millis() / 1000.0));
    int raw = read_{task_name.lower()}_raw();
    int result = process_{task_name.lower()}(raw);

    if (xSemaphoreTake(x{task_name}Mutex, portMAX_DELAY)) {{
        {task_name.lower()}_value = result;
        xSemaphoreGive(x{task_name}Mutex);
    }}

    if (x{task_name}Queue != NULL) {{
        xQueueSend(x{task_name}Queue, &result, 0);
    }}

    // -- TASK LOOP EXTENSIONS -- 
    
}}



// ========================
// 🚀 FreeRTOS Task Entry
// ========================
void {task_name}_task(void *pvParameters) {{
    if (x{task_name}Mutex == NULL) {{
        x{task_name}Mutex = xSemaphoreCreateMutex();
        if (x{task_name}Mutex == NULL) {{
            printf("❌ Failed to create mutex for {task_name}\\n");
            vTaskDelete(NULL);
        }}
    }}
    
    // -- TASK INIT EXTENSIONS --
    // Create topic queue if not already created

    while (true) {{
        {task_name}_loop();
        vTaskDelay(pdMS_TO_TICKS({task_name.upper()}_DELAY_MS));
    }}
}}

// ========================
// ✅ Public Interface
// ========================
// Set and get additional states
bool is_{task_name.lower()}_ready() {{
    return {task_name.lower()}_ready;
}}
void mark_{task_name.lower()}_ready(bool ready) {{
    {task_name.lower()}_ready = ready;
}}

int get_{task_name.lower()}() {{
    int val = 0;
    if (xSemaphoreTake(x{task_name}Mutex, portMAX_DELAY)) {{
        val = {task_name.lower()}_value;
        xSemaphoreGive(x{task_name}Mutex);
    }}
    return val;
}}

void set_{task_name.lower()}(int value) {{
    if (xSemaphoreTake(x{task_name}Mutex, portMAX_DELAY)) {{
        {task_name.lower()}_value = value;
        xSemaphoreGive(x{task_name}Mutex);
    }}
}}

// -- TASK PUBLIC FUNCTIONS EXTENSION --

// ========================
// 🧪 Mockup Implementations
// ========================
static int read_{task_name.lower()}_raw() {{
    return 42;  // TODO: Replace with sensor data
}}

static int process_{task_name.lower()}(int raw) {{
    return raw + 1;  // TODO: Replace with logic
}}
"""

    os.makedirs(os.path.dirname(src_path), exist_ok=True)
    file_utils.write_file(src_path, cpp_content)
    # Register task in main.cpp inside setup()
    task_registration = f'    xTaskCreate({task_name}_task, "{task_name}", {stack_size}, NULL, {priority}, NULL);'
    
    file_utils.insert_in_file(
        "src/main.cpp", 
        task_registration, 
        anchor="// -- TASK CREATION --")

    file_utils.insert_in_file(
        "src/main.cpp", 
        f'#include "{task_name}.h"',
        anchor="// -- TASK INCLUDES --")

    os.makedirs(os.path.dirname(include_path), exist_ok=True)
    file_utils.write_file(include_path, h_content)
    # Insert task declaration in project_config.h
    file_utils.insert_in_file(
        "include/project_config.h", 
        f'#include "{task_name}.h"',
        anchor="// -- TASK INCLUDES --")

    file_utils.insert_in_file(
        "include/project_config.h", 
        f"#define {task_name.upper()}_STACK_SIZE {stack_size}\n#define {task_name.upper()}_PRIORITY {priority}\n#define {task_name.upper()}_DELAY_MS 1000",
        anchor="// -- GLOBAL CONSTANTS --")

    # Insert shared resources in project_config.h
    file_utils.insert_in_file(
        "include/project_config.h", 
        f"// {task_name} shared resources\nextern SemaphoreHandle_t x{task_name}Mutex;\nextern QueueHandle_t x{task_name}Queue;\n// extern EventGroupHandle_t x{task_name}EventGroup;\n// extern TimerHandle_t x{task_name}Timer;",
        anchor="// -- TASK RESOURCES --")

    # Update README
    readme_updater.append_section("## Tasks\n", f"- {task_name}_task: Created using rtos_cli\n")

    print(f"✅ Task '{task_name}' created and registered.")