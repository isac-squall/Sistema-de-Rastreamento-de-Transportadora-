#!/usr/bin/env python3
"""
Teste simples das configurações
"""

import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.config.settings import Settings
    print("✅ Import settings OK")

    settings = Settings()
    print(f"✅ Settings loaded: {settings.app_name}")
    print(f"   API URL: {settings.api_base_url}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()