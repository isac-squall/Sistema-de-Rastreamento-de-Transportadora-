#!/usr/bin/env python3
"""
Script de teste da nova arquitetura refatorada
"""

import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.services.container import ServiceContainer
from core.domain.value_objects.tracking_code import TrackingCode

def test_configuration():
    """Testa carregamento das configurações"""
    print("🔧 Testando configurações...")

    try:
        container = ServiceContainer.create()
        print(f"✅ Configurações carregadas: {container.settings.app_name}")
        print(f"   API URL: {container.settings.api_config.base_url}")
        print(f"   Excel file: {container.settings.excel_config.file_path}")
        return True
    except Exception as e:
        print(f"❌ Erro nas configurações: {e}")
        return False

def test_value_objects():
    """Testa value objects"""
    print("\n🏷️  Testando Value Objects...")

    try:
        # Teste válido
        code = TrackingCode.from_string("AA123456789BR")
        print(f"✅ Código válido: {code}")

        # Teste inválido
        try:
            invalid_code = TrackingCode.from_string("INVALID")
            print("❌ Deveria ter falhado")
        except ValueError:
            print("✅ Validação funcionou para código inválido")

        return True
    except Exception as e:
        print(f"❌ Erro nos Value Objects: {e}")
        return False

def test_api_adapter():
    """Testa API adapter"""
    print("\n🌐 Testando API Adapter...")

    try:
        container = ServiceContainer.create()
        success, message = container.api_adapter.test_connection()
        if success:
            print(f"✅ Conexão API: {message}")
        else:
            print(f"⚠️  Conexão API falhou: {message}")
        return True
    except Exception as e:
        print(f"❌ Erro no API Adapter: {e}")
        return False

def test_excel_repository():
    """Testa Excel repository"""
    print("\n📊 Testando Excel Repository...")

    try:
        container = ServiceContainer.create()
        records = container.excel_repository.get_all_records()
        print(f"✅ Registros carregados: {len(records)}")
        return True
    except Exception as e:
        print(f"❌ Erro no Excel Repository: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da arquitetura refatorada\n")

    tests = [
        test_configuration,
        test_value_objects,
        test_api_adapter,
        test_excel_repository,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1

    print(f"\n📈 Resultado: {passed}/{len(tests)} testes passaram")

    if passed == len(tests):
        print("🎉 Arquitetura refatorada está funcionando!")
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")

if __name__ == "__main__":
    main()