#!/usr/bin/env python3
"""
Teste do container IoC
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.services.container import ServiceContainer
    print("Container import OK")

    container = ServiceContainer.create()
    print("Container created")
    print(f"Settings: {container.settings.app_name}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()