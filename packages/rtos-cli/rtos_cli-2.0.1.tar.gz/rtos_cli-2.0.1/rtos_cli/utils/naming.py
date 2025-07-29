# rtos_cli/commands/create_project.py
"""
@file naming.py
@brief Naming 
@author Innervycs
@version 1.2.0
@date 2025-05-05
@license MIT
"""

import re

def to_snake_case(name: str) -> str:
    """
    @brief Convert a PascalCase or camelCase string to snake_case.
    @param name Input string in PascalCase or camelCase.
    @return The string converted to snake_case.
    """
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name

def to_pascal_case(name: str) -> str:
    """
    @brief Convert a snake_case string to PascalCase.
    @param name Input string in snake_case.
    @return The string converted to PascalCase.
    """
    return ''.join(word.capitalize() for word in name.split('_'))