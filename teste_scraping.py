#!/usr/bin/env python3
"""
Script de teste para verificar o funcionamento do scraping do Site Rastreio
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_rastreamento import ConsultadorAPI

def testar_scraping():
    """Testa o scraping com um código de rastreamento"""
    consultador = ConsultadorAPI()

    # Código de teste fornecido pelo usuário
    codigo_teste = "AM947285279BR"

    print(f"Testando scraping para código: {codigo_teste}")
    print("-" * 50)

    try:
        resultado = consultador.consultar_por_rastreamento(codigo_teste)

        if resultado:
            print("✅ Scraping realizado com sucesso!")
            print(f"Código: {resultado.get('codigo_rastreamento', 'N/A')}")
            print(f"Status: {resultado.get('status_amigavel', 'N/A')}")
            print(f"Última atualização: {resultado.get('data_atualizacao', 'N/A')}")
            print(f"Localização: {resultado.get('localizacao', 'N/A')}")

            historico = resultado.get('historico', [])
            if historico:
                print(f"\n📋 Histórico ({len(historico)} eventos):")
                for i, evento in enumerate(historico[:5], 1):  # Mostra apenas os 5 primeiros
                    print(f"  {i}. {evento.get('data', '')} - {evento.get('local', '')}")
                    print(f"     {evento.get('descricao', '')}")
            else:
                print("\n📋 Nenhum histórico encontrado")
        else:
            print("❌ Falha no scraping - nenhum dado retornado")

    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_scraping()