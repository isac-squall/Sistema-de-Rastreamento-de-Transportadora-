"""
Script para criar uma planilha de exemplo para testes
Execute este arquivo para gerar a planilha de exemplo
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def criar_planilha_exemplo():
    """Cria uma planilha de exemplo com dados fictícios"""

    # Dados de exemplo
    dados = {
        'NF': [
            '2026000001',
            '2026000002',
            '2026000003',
            '2026000004',
            '2026000005',
            '2026000006',
            '2026000007',
            '2026000008',
            '2026000009',
            '2026000010',
        ],
        'Rastreamento': [
            'BR123456789ABC',
            'BR123456789DEF',
            'BR123456789GHI',
            'BR123456789JKL',
            'BR123456789MNO',
            'BR123456789PQR',
            'BR123456789STU',
            'BR123456789VWX',
            'BR123456789YZ1',
            'BR123456789Z23',
        ],
        'Status': [
            '✅ Entregue',
            '🚚 Em Trânsito',
            '📦 Saiu para Entrega',
            '⏳ Aguardando Retirada',
            '🚚 Em Trânsito',
            '✅ Entregue',
            '❌ Não Entregue',
            '🚚 Em Trânsito',
            '↩️ Devolvido',
            '⏳ Aguardando Retirada',
        ],
        'Última Atualização': [
            (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y %H:%M:%S'),
            (datetime.now() - timedelta(days=2)).strftime('%d/%m/%Y %H:%M:%S'),
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            (datetime.now() - timedelta(days=3)).strftime('%d/%m/%Y %H:%M:%S'),
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            (datetime.now() - timedelta(days=5)).strftime('%d/%m/%Y %H:%M:%S'),
            (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y %H:%M:%S'),
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            (datetime.now() - timedelta(days=4)).strftime('%d/%m/%Y %H:%M:%S'),
            (datetime.now() - timedelta(days=2)).strftime('%d/%m/%Y %H:%M:%S'),
        ],
        'Detalhes': [
            '📍 São Paulo - SP | 🕐 Entregue em 03/03/2026',
            '📍 Rio de Janeiro - RJ | 🕐 Em trânsito',
            '📍 Belo Horizonte - MG | 🕐 Saindo para entrega hoje',
            '📍 Curitiba - PR | 🕐 Aguardando retirada no cliente',
            '📍 Salvador - BA | 🕐 Em transporte',
            '📍 Brasília - DF | 🕐 Entregue em 28/02/2026',
            '📍 Manaus - AM | 🕐 Não foi entregue',
            '📍 Recife - PE | 🕐 Em transporte',
            '📍 Porto Alegre - RS | 🕐 Devolvido ao remetente',
            '📍 Fortaleza - CE | 🕐 Aguardando retirada',
        ]
    }

    # Cria DataFrame
    df = pd.DataFrame(dados)

    # Salva como Excel
    arquivo_saida = 'planilha_rastreamento_exemplo.xlsx'
    df.to_excel(arquivo_saida, index=False)

    print(f"✓ Planilha de exemplo criada: {arquivo_saida}")
    print(f"\nDados da planilha:")
    print(df.to_string(index=False))
    print(f"\nTotal de registros: {len(df)}")


if __name__ == '__main__':
    criar_planilha_exemplo()
