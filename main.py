"""
Módulo principal - Orquestrador do sistema de rastreamento
"""

from typing import Dict, List
from datetime import datetime
from api_rastreamento import ConsultadorAPI
from processador_excel import ProcessadorExcel
from utils import BackupManager, RateLimiter
from config import CRIAR_BACKUP_ANTES, SALVAR_RELATORIO, EXCEL_FILE_PATH
from logger_setup import logger


class OrquestradorRastreamento:
    """Orquestra o fluxo completo de rastreamento"""

    def __init__(self):
        """Inicializa o orquestrador"""
        self.api = ConsultadorAPI()
        self.excel = ProcessadorExcel()
        self.backup_manager = BackupManager()
        self.atualizacoes = {
            'total_processados': 0,
            'sucesso': 0,
            'mudancas': 0,
            'erros': 0,
            'status_distribuicao': {},
            'erros_detalhes': []
        }

    def processar_rastreamentos(self, criar_backup: bool = CRIAR_BACKUP_ANTES) -> bool:
        """
        Processa todos os rastreamentos da planilha

        Args:
            criar_backup: Se deve criar backup antes de processar

        Returns:
            True se processou com sucesso, False caso contrário
        """
        logger.info("=" * 80)
        logger.info("INICIANDO PROCESSAMENTO DE RASTREAMENTOS")
        logger.info("=" * 80)

        try:
            # Passo 1: Criar backup
            if criar_backup:
                if not self._criar_backup():
                    return False

            # Passo 2: Carregar planilha (ou criar modelo se estiver faltando)
            if not self.excel.carregar_planilha():
                logger.warning("Planilha não encontrada, criando planilha modelo vazia")
                if not self.excel.criar_planilha_modelo():
                    logger.error("Falha ao criar planilha modelo")
                    return False
                # após criar modelo não há registros para processar
                logger.info("Processamento interrompido: não havia dados para processar")
                return True

            # Passo 3: Validar colunas
            if not self.excel.validar_colunas_obrigatorias():
                logger.error("Planilha não possui colunas obrigatórias")
                return False

            # Passo 4: Testar conexão com API
            sucesso, mensagem = self.api.teste_conexao()
            if not sucesso:
                logger.warning(f"Aviso: {mensagem}")
                # Continua mesmo assim, apenas avisa

            # Passo 5: Processar registros
            registros = self.excel.obter_registros_para_processar()
            self._processar_registros(registros)

            # Passo 6: Salvar planilha
            if not self.excel.salvar_planilha(aplicar_formatacao=True):
                logger.error("Falha ao salvar planilha")
                return False

            # Passo 7: Gerar relatório
            self._gerar_relatorio()

            logger.info("=" * 80)
            logger.info("PROCESSAMENTO CONCLUÍDO COM SUCESSO")
            logger.info("=" * 80)

            return True

        except Exception as e:
            logger.error(f"Erro crítico durante processamento: {str(e)}")
            return False

    def _criar_backup(self) -> bool:
        """Cria backup da planilha.

        Se o arquivo não existir (erro comum na primeira execução), emite um
        aviso mas não interrompe o processamento. Isso evita que a etapa de
        backup bloqueie a criação inicial da planilha modelo.
        """
        try:
            self.backup_manager.criar_backup(EXCEL_FILE_PATH)
            logger.info("Backup criado com sucesso")
            return True
        except FileNotFoundError:
            logger.warning("Arquivo da planilha não encontrado; pulando backup")
            return True
        except Exception as e:
            logger.error(f"Falha ao criar backup: {str(e)}")
            return False

    def _processar_registros(self, registros: List[Dict]):
        """Processa lista de registros"""
        total = len(registros)

        for contador, registro in enumerate(registros, 1):
            indice = registro['indice']
            nf = registro['numero_nf']
            rastreamento = registro['codigo_rastreamento']

            logger.info(f"[{contador}/{total}] Processando NF: {nf}, Rastreamento: {rastreamento}")

            self.atualizacoes['total_processados'] += 1

            # Tenta consultar por rastreamento primeiro (geralmente mais rápido)
            dados = None
            if rastreamento:
                dados = self.api.consultar_por_rastreamento(rastreamento)

            # Se não encontrou por rastreamento, tenta por NF
            if dados is None and nf:
                dados = self.api.consultar_por_nf(nf)

            # Se conseguiu dados, atualiza registro
            if dados:
                self.atualizacoes['sucesso'] += 1
                houve_mudanca = self.excel.atualizar_registro(indice, dados)

                if houve_mudanca:
                    self.atualizacoes['mudancas'] += 1
                    status = dados.get('status_amigavel', 'Desconhecido')
                    self.atualizacoes['status_distribuicao'][status] = \
                        self.atualizacoes['status_distribuicao'].get(status, 0) + 1
                    logger.info(f"  ✓ Status atualizado para: {status}")
                else:
                    logger.info(f"  ℹ Status sem mudanças")

            else:
                self.atualizacoes['erros'] += 1
                self.excel.atualizar_registro(indice, None)  # Marca como erro
                self.atualizacoes['status_distribuicao']['⚠️ Erro na Busca'] = \
                    self.atualizacoes['status_distribuicao'].get('⚠️ Erro na Busca', 0) + 1

                erro_msg = f"Falha ao consultar NF: {nf}, Rastreamento: {rastreamento}"
                self.atualizacoes['erros_detalhes'].append(erro_msg)
                logger.warning(f"  ✗ {erro_msg}")

            # Mostra status de rate limiting
            rate_limit_info = self.api.get_rate_limit_status()
            logger.debug(f"  Rate limit: {rate_limit_info['requisicoes_no_periodo']}/{rate_limit_info['limite']} "
                        f"no período de {rate_limit_info['periodo_segundos']}s")

    def _gerar_relatorio(self):
        """Gera e exibe relatório final"""
        relatorio = self.excel.gerar_relatorio_atualizacoes(self.atualizacoes)
        logger.info("\n" + relatorio)

        # Salva relatório em arquivo se configurado
        if SALVAR_RELATORIO:
            self._salvar_relatorio_arquivo(relatorio)

    def _salvar_relatorio_arquivo(self, relatorio: str):
        """Salva relatório em arquivo"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_arquivo = f"relatorio_rastreamento_{timestamp}.txt"

            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(relatorio)

            logger.info(f"Relatório salvo em: {nome_arquivo}")

        except Exception as e:
            logger.error(f"Erro ao salvar relatório: {str(e)}")

    def listar_backups(self) -> List[Dict]:
        """Lista todos os backups disponíveis"""
        return self.backup_manager.listar_backups()

    def restaurar_backup(self, caminho_backup: str) -> bool:
        """
        Restaura um backup

        Args:
            caminho_backup: Caminho do arquivo de backup

        Returns:
            True se restaurou com sucesso, False caso contrário
        """
        try:
            self.backup_manager.restaurar_backup(caminho_backup)
            logger.info(f"Backup restaurado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao restaurar backup: {str(e)}")
            return False

    def criar_planilha_modelo(self) -> bool:
        """Cria uma planilha modelo"""
        return self.excel.criar_planilha_modelo()

    def obter_atualizacoes(self) -> Dict:
        """Retorna as estatísticas de atualizações"""
        return self.atualizacoes


def main():
    """Função principal"""
    orquestrador = OrquestradorRastreamento()
    sucesso = orquestrador.processar_rastreamentos()

    if sucesso:
        logger.info("Processamento finalizado com sucesso!")
        return 0
    else:
        logger.error("Processamento finalizado com erros!")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
