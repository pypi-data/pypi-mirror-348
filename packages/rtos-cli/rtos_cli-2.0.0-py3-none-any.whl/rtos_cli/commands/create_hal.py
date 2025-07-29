import os
from rtos_cli.utils import file_utils, readme_updater, doxygen

TEMPLATE_MAP = {
    "i2c": "hal_i2c.template",
    "gpio": "hal_gpio.template",
    "spi": "hal_spi.template",
    "pwm": "hal_pwm.template",
    "uart": "hal_uart.template",
    "adc": "hal_adc.template",
    "wifi": "hal_wifi.template",
    "sd": "hal_sd.template",
    "timer": "hal_timer.template",
    "rtc": "hal_rtc.template",
    "ble": "hal_ble.template",
}

def run(name, hal_type="gpio", hal_num=None, **kwargs):
    """
    @brief Crea un HAL específico para un periférico.

    Esta función genera los archivos fuente y de encabezado para un HAL basado en plantillas,
    configurando pines, frecuencias y parámetros según el tipo de periférico y número de instancia.

    @param name Nombre base del HAL (ej. "i2c")
    @param hal_type Tipo de HAL a generar (ej. "i2c", "gpio", "spi", etc.)
    @param hal_num Sufijo numérico o nombre identificador para diferenciar múltiples instancias
    @param kwargs Diccionario con parámetros adicionales específicos para cada tipo de HAL
    """
    if hal_type not in TEMPLATE_MAP:
        raise ValueError(f"Tipo de HAL '{hal_type}' no soportado")

    project_root = os.getcwd()
    include_dir = os.path.join(project_root, "include")
    project_config_path = os.path.join(include_dir, "project_config.h")

    suffix = f"_bus{hal_num}" if hal_num is not None else ""
    hal_basename = f"hal_{name}{suffix}"

    hal_root_dir = os.path.join(project_root, "lib", "hal", hal_basename)
    hal_src_dir = os.path.join(hal_root_dir, "src")
    hal_include_dir = os.path.join(hal_root_dir, "include")

    os.makedirs(hal_src_dir, exist_ok=True)
    os.makedirs(hal_include_dir, exist_ok=True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, "..", "templates", "hal")
    template_file = TEMPLATE_MAP[hal_type]
    with open(os.path.join(templates_dir, template_file), "r") as f:
        template_content = f.read()

    cpp_content, h_content = "", ""
    parts = template_content.split("// ========")
    for part in parts:
        if part.strip().startswith(f"{hal_basename}.cpp"):
            cpp_content = part.split("========", 1)[-1].strip()
        elif part.strip().startswith(f"{hal_basename}.h"):
            h_content = part.split("========", 1)[-1].strip()

    if not cpp_content or not h_content:
        raise ValueError(f"Plantilla para '{hal_type}' no contiene secciones válidas para .cpp y .h")

    cpp_content = cpp_content.replace("hal_template", hal_basename)
    h_content = h_content.replace("hal_template", hal_basename)

    if hal_num is not None:
        if hal_type == "i2c":
            cpp_content = cpp_content.replace("i2c_mutex", f"i2c_mutex_bus{hal_num}")

    if hal_type == "i2c":
        sda_pin = kwargs.get("sda", 21)
        scl_pin = kwargs.get("scl", 22)
        freq_hz = kwargs.get("freq", 100000)
        cpp_content = (
            cpp_content
            .replace("{{SDA_PIN}}", str(sda_pin))
            .replace("{{SCL_PIN}}", str(scl_pin))
            .replace("{{FREQ_HZ}}", str(freq_hz))
        )
        h_content = (
            h_content
            .replace("{{SDA_PIN}}", str(sda_pin))
            .replace("{{SCL_PIN}}", str(scl_pin))
            .replace("{{FREQ_HZ}}", str(freq_hz))
        )
    elif hal_type == "spi":
        mosi = kwargs.get("mosi", 23)
        miso = kwargs.get("miso", 19)
        sck = kwargs.get("sck", 18)
        cs = kwargs.get("cs", 5)
        cpp_content = (
            cpp_content
            .replace("{{MOSI_PIN}}", str(mosi))
            .replace("{{MISO_PIN}}", str(miso))
            .replace("{{SCK_PIN}}", str(sck))
            .replace("{{CS_PIN}}", str(cs))
        )
        h_content = (
            h_content
            .replace("{{MOSI_PIN}}", str(mosi))
            .replace("{{MISO_PIN}}", str(miso))
            .replace("{{SCK_PIN}}", str(sck))
            .replace("{{CS_PIN}}", str(cs))
        )
    elif hal_type == "pwm":
        pwm_pin = kwargs.get("pin", 4)
        freq = kwargs.get("freq", 5000)
        channel = kwargs.get("channel", 0)
        cpp_content = (
            cpp_content
            .replace("{{PWM_PIN}}", str(pwm_pin))
            .replace("{{PWM_FREQ}}", str(freq))
            .replace("{{PWM_CHANNEL}}", str(channel))
        )
        h_content = (
            h_content
            .replace("{{PWM_PIN}}", str(pwm_pin))
            .replace("{{PWM_FREQ}}", str(freq))
            .replace("{{PWM_CHANNEL}}", str(channel))
        )
    elif hal_type == "uart":
        tx = kwargs.get("tx", 1)
        rx = kwargs.get("rx", 3)
        baudrate = kwargs.get("baudrate", 115200)
        cpp_content = (
            cpp_content
            .replace("{{TX_PIN}}", str(tx))
            .replace("{{RX_PIN}}", str(rx))
            .replace("{{BAUDRATE}}", str(baudrate))
        )
        h_content = (
            h_content
            .replace("{{TX_PIN}}", str(tx))
            .replace("{{RX_PIN}}", str(rx))
            .replace("{{BAUDRATE}}", str(baudrate))
        )
    elif hal_type == "adc":
        adc_pin = kwargs.get("pin", 34)
        cpp_content = cpp_content.replace("{{ADC_PIN}}", str(adc_pin))
        h_content = h_content.replace("{{ADC_PIN}}", str(adc_pin))

    file_utils.write_file(os.path.join(hal_src_dir, f"{hal_basename}.cpp"), cpp_content)
    file_utils.write_file(os.path.join(hal_include_dir, f"{hal_basename}.h"), h_content)

    library_json = {
        "name": hal_basename,
        "version": "1.0.0",
        "keywords": ["HAL", hal_type, "ESP32"],
        "description": f"HAL para manejar periférico {hal_type} con FreeRTOS",
        "authors": [
            {
                "name": "Efrain Reyes Araujo",
                "email": "dev@reyes-araujo.com"
            }
        ],
        "frameworks": ["arduino"],
        "platforms": ["espressif32"]
    }

    import json
    with open(os.path.join(hal_root_dir, "library.json"), "w") as f:
        json.dump(library_json, f, indent=4)

    section_comment = doxygen.add_section_comment(
        f"HAL {hal_basename.upper()}",
        f"Configuración para {hal_type.upper()} ({hal_basename})"
    )
    file_utils.insert_in_file(project_config_path, section_comment, anchor="// -- GLOBAL CONSTANTS --")

    readme_path = os.path.join(project_root, "README.md")
    readme_updater.append_section(
        f"HAL: {hal_basename}",
        f"""
Soporte agregado para HAL `{hal_basename}` basado en tipo `{hal_type}`.

```cpp
#include <{hal_basename}.h>
```
"""
    )

    print(f"✅ HAL '{hal_basename}' creado exitosamente como tipo '{hal_type}'")