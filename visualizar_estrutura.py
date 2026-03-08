"""
Visualizar estrutura do projeto
Execute: python visualizar_estrutura.py
"""

import os
from pathlib import Path


def visualizar_estrutura(diretorio='.', prefixo='', ignorar=['__pycache__', '.git', 'backups', 'logs', 'venv', '.pytest_cache']):
    """Visualiza a estrutura de arquivos do projeto"""
    
    itens = []
    
    try:
        arquivos = sorted(os.listdir(diretorio))
    except PermissionError:
        return
    
    arquivos = [a for a in arquivos if a not in ignorar and not a.startswith('.')]
    
    for i, arquivo in enumerate(arquivos):
        caminho = os.path.join(diretorio, arquivo)
        eh_ultimo = i == len(arquivos) - 1
        
        simbolo = '└── ' if eh_ultimo else '├── '
        
        if os.path.isdir(caminho):
            itens.append(f"{prefixo}{simbolo}{arquivo}/")
            novo_prefixo = prefixo + ('    ' if eh_ultimo else '│   ')
            itens.extend(visualizar_estrutura(caminho, novo_prefixo, ignorar))
        else:
            itens.append(f"{prefixo}{simbolo}{arquivo}")
    
    return itens


def descrever_arquivos():
    """Fornece descrição de cada arquivo"""
    
    descricoes = {
        'main.py': 'Módulo principal que orquestra todo o fluxo de processamento',
        'api_rastreamento.py': 'Consumo da API da transportadora com retry e rate limiting',
        'processador_excel.py': 'Manipulação e atualização de planilhas Excel',
        'config.py': 'Configurações centralizadas e variáveis de ambiente',
        'logger_setup.py': 'Sistema de logging com arquivo e console',
        'utils.py': 'Rate limiter e gerenciador de backups',
        'cli.py': 'Interface de linha de comando para fácil uso',
        'requirements.txt': 'Dependências Python do projeto',
        '.env': 'Variáveis de ambiente (mantenha confidencial)',
        '.env.example': 'Exemplo de configuração de .env',
        'README.md': 'Documentação completa do projeto',
        'GUIA_RAPIDO.md': 'Guia de início rápido (5 minutos)',
        'GUIA_INTEGRACAO.md': 'Instruções detalhadas de integração com API',
        'EXEMPLOS_INTEGRACAO.py': '10 exemplos de integração com diferentes APIs',
        'criar_exemplo.py': 'Script para criar planilha de exemplo com dados fictícios',
        'testes.py': 'Testes unitários e de integração',
        'backups/': 'Pasta onde backups da planilha são armazenados',
        'logs/': 'Pasta com logs de execução do sistema',
    }
    
    return descricoes


def main():
    """Função principal"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     ESTRUTURA DO PROJETO - RASTREAMENTO DE TRANSPORTADORA      ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    print("📁 ESTRUTURA DE ARQUIVOS:\n")
    
    estrutura = visualizar_estrutura()
    for linha in estrutura:
        print(linha)
    
    print("\n" + "="*70)
    print("📋 DESCRIÇÃO DOS ARQUIVOS:\n")
    
    descricoes = descrever_arquivos()
    
    print("✚ ARQUIVOS PRINCIPAIS:")
    arquivos_principais = [
        ('main.py', 'Orquestrador do sistema'),
        ('api_rastreamento.py', 'Integração com API'),
        ('processador_excel.py', 'Manipulação de Excel'),
    ]
    
    for arquivo, desc in arquivos_principais:
        print(f"  • {arquivo:<25} - {desc}")
    
    print("\n✚ ARQUIVOS DE SUPORTE:")
    arquivos_suporte = [
        ('config.py', 'Configurações'),
        ('cli.py', 'Linha de comando'),
        ('utils.py', 'Utilitários'),
        ('logger_setup.py', 'Logging'),
    ]
    
    for arquivo, desc in arquivos_suporte:
        print(f"  • {arquivo:<25} - {desc}")
    
    print("\n✚ DOCUMENTAÇÃO:")
    docs = [
        ('README.md', 'Documentação completa'),
        ('GUIA_RAPIDO.md', 'Começar em 5 minutos'),
        ('GUIA_INTEGRACAO.md', 'Integrar com sua API'),
        ('EXEMPLOS_INTEGRACAO.py', '10 exemplos de APIs'),
    ]
    
    for arquivo, desc in docs:
        print(f"  • {arquivo:<25} - {desc}")
    
    print("\n✚ CONFIGURAÇÃO E EXEMPLO:")
    config = [
        ('.env', 'Variáveis de ambiente'),
        ('.env.example', 'Exemplo de .env'),
        ('criar_exemplo.py', 'Criar dados exemplo'),
    ]
    
    for arquivo, desc in config:
        print(f"  • {arquivo:<25} - {desc}")
    
    print("\n✚ TESTES:")
    testes = [
        ('testes.py', 'Testes unitários'),
    ]
    
    for arquivo, desc in testes:
        print(f"  • {arquivo:<25} - {desc}")
    
    print("\n✚ PASTA DINÂMICAS:")
    pastas = [
        ('backups/', 'Backups automáticos'),
        ('logs/', 'Logs de execução'),
    ]
    
    for pasta, desc in pastas:
        print(f"  • {pasta:<25} - {desc}")
    
    print("\n" + "="*70)
    print("\n🚀 PRÓXIMOS PASSOS:\n")
    
    passos = [
        "1. Instale dependências: pip install -r requirements.txt",
        "2. Copie .env.example para .env e configure API",
        "3. Crie planilha modelo: python cli.py criar-modelo",
        "4. Adapte api_rastreamento.py para sua API (veja GUIA_INTEGRACAO.md)",
        "5. Preencha planilha_rastreamento.xlsx com dados reais",
        "6. Execute: python cli.py processar",
    ]
    
    for passo in passos:
        print(f"  {passo}")
    
    print("\n" + "="*70)
    print("\n📚 DOCUMENTAÇÃO:\n")
    
    docs_info = [
        ("Guia Rápido", "GUIA_RAPIDO.md", "Começar em 5 minutos"),
        ("Documentação Completa", "README.md", "Todas as funcionalidades"),
        ("Guia de Integração", "GUIA_INTEGRACAO.md", "Adaptar para sua API"),
        ("Exemplos de Código", "EXEMPLOS_INTEGRACAO.py", "10 exemplos práticos"),
    ]
    
    for nome, arquivo, descricao in docs_info:
        print(f"  • {nome:<25} ({arquivo:<25}) - {descricao}")
    
    print("\n" + "="*70)
    print("\n💡 DICAS:\n")
    
    dicas = [
        "• Comece pelo GUIA_RAPIDO.md se é sua primeira vez",
        "• Consulte GUIA_INTEGRACAO.md para adaptar a API",
        "• Veja EXEMPLOS_INTEGRACAO.py para exemplos práticos",
        "• Logs são salvos em logs/ para debugging",
        "• Backups automáticos são salvos em backups/",
        "• Configure LOG_LEVEL=DEBUG para mais detalhes",
    ]
    
    for dica in dicas:
        print(f"  {dica}")
    
    print("\n" + "="*70)
    print("\n✨ Projeto pronto para usar! Boa sorte! ✨\n")


if __name__ == '__main__':
    main()
