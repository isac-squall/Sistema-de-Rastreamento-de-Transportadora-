"""
Interface de linha de comando (CLI) para o sistema de rastreamento
"""

import argparse
import sys
from main import OrquestradorRastreamento
from logger_setup import logger


def main():
    """Função principal da CLI"""
    parser = argparse.ArgumentParser(
        description='Sistema de Rastreamento de Transportadora - Atualizar planilha Excel com dados de rastreamento'
    )

    subparsers = parser.add_subparsers(dest='comando', help='Comando a executar')

    # Comando: processar
    parser_processar = subparsers.add_parser(
        'processar',
        help='Processa rastreamentos e atualiza planilha'
    )
    parser_processar.add_argument(
        '--sem-backup',
        action='store_true',
        help='Não criar backup antes de processar'
    )

    # Comando: criar-modelo
    subparsers.add_parser(
        'criar-modelo',
        help='Cria uma planilha modelo com estrutura básica'
    )

    # Comando: listar-backups
    subparsers.add_parser(
        'listar-backups',
        help='Lista todos os backups disponíveis'
    )

    # Comando: restaurar-backup
    parser_restaurar = subparsers.add_parser(
        'restaurar-backup',
        help='Restaura um backup anterior'
    )
    parser_restaurar.add_argument(
        'caminho',
        help='Caminho do arquivo de backup'
    )

    args = parser.parse_args()

    # Se nenhum comando foi especificado, mostra ajuda
    if not args.comando:
        parser.print_help()
        return 1

    orquestrador = OrquestradorRastreamento()

    # Executa comando solicitado
    if args.comando == 'processar':
        criar_backup = not args.sem_backup
        logger.info(f"Iniciando processamento (backup: {criar_backup})...")
        sucesso = orquestrador.processar_rastreamentos(criar_backup=criar_backup)
        return 0 if sucesso else 1

    elif args.comando == 'criar-modelo':
        logger.info("Criando planilha modelo...")
        sucesso = orquestrador.criar_planilha_modelo()
        if sucesso:
            logger.info("✓ Planilha modelo criada com sucesso!")
            return 0
        else:
            logger.error("✗ Erro ao criar planilha modelo")
            return 1

    elif args.comando == 'listar-backups':
        logger.info("Listando backups disponíveis...")
        backups = orquestrador.listar_backups()

        if not backups:
            logger.info("Nenhum backup encontrado")
            return 0

        logger.info(f"Total de backups: {len(backups)}\n")
        for idx, backup in enumerate(backups, 1):
            logger.info(f"{idx}. {backup['arquivo']}")
            logger.info(f"   Caminho: {backup['caminho']}")
            logger.info(f"   Tamanho: {backup['tamanho']}")
            logger.info(f"   Data: {backup['data']}\n")

        return 0

    elif args.comando == 'restaurar-backup':
        logger.info(f"Restaurando backup: {args.caminho}...")
        sucesso = orquestrador.restaurar_backup(args.caminho)
        if sucesso:
            logger.info("✓ Backup restaurado com sucesso!")
            return 0
        else:
            logger.error("✗ Erro ao restaurar backup")
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
