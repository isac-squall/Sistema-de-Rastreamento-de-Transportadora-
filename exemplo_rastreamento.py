"""
Exemplo de uso da API de rastreamento dos Correios
"""

from api_rastreamento import ConsultadorAPI

def exemplo_rastreamento():
    """
    Exemplo de como usar a API de rastreamento
    """

    # Para teste rápido com dados simulados
    print("=== MODO TESTE ===")
    api_teste = ConsultadorAPI(modo_teste=True)

    # Exemplo de código de rastreamento dos Correios
    codigo = "AA123456789BR"

    resultado = api_teste.consultar_por_rastreamento(codigo)

    if resultado:
        print(f"Código: {resultado['codigo_rastreamento']}")
        print(f"Status: {resultado['status_amigavel']}")
        print(f"Última atualização: {resultado['data_atualizacao']}")
        print(f"Localização: {resultado['localizacao']}")
        print("\nHistórico:")
        for evento in resultado['historico']:
            print(f"  {evento['data']} - {evento['local']}: {evento['descricao']}")
    else:
        print("Falha na consulta")

    print("\n=== MODO PRODUÇÃO ===")
    print("Para usar com API real:")
    print("1. Obtenha chave de acesso no CWS dos Correios")
    print("2. Configure API_KEY no .env")
    print("3. Use: api = ConsultadorAPI()")
    print("4. resultado = api.consultar_por_rastreamento(codigo)")

if __name__ == "__main__":
    exemplo_rastreamento()