#!/usr/bin/env python3
"""
Sistema de dados melhorado com informações reais

Estrutura: {
    'codigo': 'AM947285279BR',
    'produto': 'Poltrona',
    'status': 'entregue',
    'ultimo_evento': 'Objeto entregue ao destinatário',
    'local': 'SAO PAULO/SP',
    'data_atualizacao': '25/09/2025 12:49',
    'prazo_entrega': '01/10/2025 23:59',
    'servico': 'ENCOMENDA PAC',
    'historico': [list of events]
}
"""

# Dados de exemplo baseado no rastreamento real
DADOS_REAIS = {
    "AM947285279BR": {
        "codigo": "AM947285279BR",
        "produto": "Poltrona",
        "status": "entregue",
        "status_codigo": "entregue",
        "status_amigavel": "Entregue",
        "ultimo_evento": "Objeto entregue ao destinatário",
        "local": "SAO PAULO/SP",
        "data_atualizacao": "25/09/2025 12:49",
        "prazo_entrega": "01/10/2025 23:59",
        "servico": "ENCOMENDA PAC",
        "numero_nf": "",
        "detalhes": {
            "remetente": "",
            "destinatario": "",
            "endereco_entrega": "SAO PAULO/SP",
            "peso": "",
            "valor": "",
            "servico": "ENCOMENDA PAC"
        },
        "historico": [
            {
                "data": "25/09/2025",
                "hora": "12:49",
                "local": "SAO PAULO/SP",
                "status": "entregue",
                "descricao": "Objeto entregue ao destinatário"
            },
            {
                "data": "25/09/2025",
                "hora": "10:30",
                "local": "UNIDADE DE DISTRIBUICAO SAO PAULO",
                "status": "saiu_para_entrega",
                "descricao": "Saiu para entrega"
            },
            {
                "data": "24/09/2025",
                "hora": "15:20",
                "local": "UNIDADE DE DISTRIBUICAO SAO PAULO",
                "status": "chegou_unidade",
                "descricao": "Chegou na unidade de distribuição"
            },
            {
                "data": "23/09/2025",
                "hora": "08:00",
                "local": "CENTRO DE TRATAMENTO BRASILIA",
                "status": "em_transito",
                "descricao": "Objeto em trânsito"
            },
            {
                "data": "21/09/2025",
                "hora": "14:45",
                "local": "UNIDADE DE ORIGEM BRASILIA",
                "status": "postado",
                "descricao": "Objeto postado"
            }
        ]
    }
}

if __name__ == "__main__":
    import json
    print(json.dumps(DADOS_REAIS, indent=2, ensure_ascii=False))
