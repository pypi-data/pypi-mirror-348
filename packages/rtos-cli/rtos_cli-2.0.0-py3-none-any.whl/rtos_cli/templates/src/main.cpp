/**
 * @file main.cpp
 * @brief Main 
 * @version 1.0.0
 * @date 2025-05-01
 * @author Efrain Reyes Araujo
 * @license MIT
 */

#include <Arduino.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// -- INCLUDES HAL --

// -- TASK INCLUDES --


// -- TOPIC QUEUE DEFINITIONS --



void setup() {
    Serial.begin(115200);
    delay(1000);  // Pequeño retardo de inicialización

    // -- SETUP INIT EXTENSIONS --

    
    // -- TASK CREATION --
    
}

void loop() {
    // Loop de Arduino puede estar vacío si todo es FreeRTOS
    vTaskDelay(pdMS_TO_TICKS(1000));

}