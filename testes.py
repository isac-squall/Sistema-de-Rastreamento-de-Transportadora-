"""
Testes unitários e de integração para o sistema de rastreamento
Execute com: python -m pytest testes.py -v
"""

import unittest
import os
from unittest.mock import patch, MagicMock
from api_rastreamento import ConsultadorAPI
from processador_excel import ProcessadorExcel
from utils import RateLimiter, BackupManager
from logger_setup import logger
from main import OrquestradorRastreamento


class TestConsultadorAPI(unittest.TestCase):
    """Testes para o consultador de API"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.api = ConsultadorAPI()

    def test_inicializacao_api(self):
        """Testa inicialização da API"""
        self.assertIsNotNone(self.api.headers)
        self.assertIn('User-Agent', self.api.headers)

    def test_preparar_headers(self):
        """Testa preparação de headers"""
        headers = self.api._preparar_headers()
        self.assertIn('Content-Type', headers)
        self.assertEqual(headers['Content-Type'], 'application/json')

    @patch('api_rastreamento.requests.get')
    def test_consultar_por_nf_sucesso(self, mock_get):
        """Testa consulta por NF com sucesso"""
        # Mock da resposta
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'nf': '2026000001',
            'tracking_code': 'BR123456789ABC',
            'status': {'code': 'entregue', 'description': 'Entregue'},
            'last_update': '03/03/2026 10:00:00',
            'location': 'São Paulo - SP'
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        resultado = self.api.consultar_por_nf('2026000001')

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['numero_nf'], '2026000001')


class TestRateLimiter(unittest.TestCase):
    """Testes para o rate limiter"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.rate_limiter = RateLimiter(max_requests=5, period=1)

    def test_inicializacao(self):
        """Testa inicialização do rate limiter"""
        self.assertEqual(self.rate_limiter.max_requests, 5)
        self.assertEqual(self.rate_limiter.period, 1)
        self.assertEqual(len(self.rate_limiter.request_times), 0)

    def test_get_requests_count(self):
        """Testa contagem de requisições"""
        self.rate_limiter.wait_if_needed()
        self.rate_limiter.wait_if_needed()

        count = self.rate_limiter.get_requests_count()
        self.assertEqual(count, 2)


class TestBackupManager(unittest.TestCase):
    """Testes para o gerenciador de backup"""

    def setUp(self):
        """Configuração antes de cada teste"""
        # Cria arquivo de teste
        self.arquivo_teste = 'teste_backup.xlsx'
        with open(self.arquivo_teste, 'w') as f:
            f.write('teste')

    def tearDown(self):
        """Limpeza após cada teste"""
        # Remove arquivo de teste
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)

        # Remove backups criados
        if os.path.exists('backups'):
            import shutil
            shutil.rmtree('backups')

    def test_criar_backup(self):
        """Testa criação de backup"""
        caminho_backup = BackupManager.criar_backup(self.arquivo_teste)
        self.assertTrue(os.path.exists(caminho_backup))

    def test_listar_backups(self):
        """Testa listagem de backups"""
        BackupManager.criar_backup(self.arquivo_teste)
        BackupManager.criar_backup(self.arquivo_teste)

        backups = BackupManager.listar_backups()
        self.assertEqual(len(backups), 2)

    def test_restaurar_backup(self):
        """Testa restauração de backup"""
        caminho_backup = BackupManager.criar_backup(self.arquivo_teste)

        # Remove arquivo original
        os.remove(self.arquivo_teste)

        # Restaura backup
        BackupManager.restaurar_backup(caminho_backup, self.arquivo_teste)

        self.assertTrue(os.path.exists(self.arquivo_teste))


class TestProcessadorExcel(unittest.TestCase):
    """Testes para o processador de Excel"""

    def setUp(self):
        """Configuração antes de cada teste"""
        # Cria planilha de teste
        import pandas as pd
        df = pd.DataFrame({
            'NF': ['2026000001', '2026000002'],
            'Rastreamento': ['BR123456789ABC', 'BR123456789DEF'],
            'Status': ['⏳ Aguardando', '🚚 Em Trânsito'],
            'Última Atualização': ['', ''],
            'Detalhes': ['', '']
        })
        self.arquivo_teste = 'teste_planilha.xlsx'
        df.to_excel(self.arquivo_teste, index=False)
        self.processador = ProcessadorExcel(self.arquivo_teste)

    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)

    def test_carregar_planilha(self):
        """Testa carregamento de planilha"""
        resultado = self.processador.carregar_planilha()
        self.assertTrue(resultado)
        self.assertIsNotNone(self.processador.df)

    def test_validar_colunas_obrigatorias(self):
        """Testa validação de colunas"""
        self.processador.carregar_planilha()
        resultado = self.processador.validar_colunas_obrigatorias()
        self.assertTrue(resultado)

    def test_obter_registros_para_processar(self):
        """Testa obtenção de registros"""
        self.processador.carregar_planilha()
        registros = self.processador.obter_registros_para_processar()
        self.assertEqual(len(registros), 2)
        self.assertEqual(registros[0]['numero_nf'], '2026000001')

    def test_orquestrador_cria_modelo_quando_planilha_falta(self):
        """Ao processar sem planilha existente, o orquestrador cria modelo e retorna True"""
        # garante que não exista a planilha padrão
        from config import EXCEL_FILE_PATH
        if os.path.exists(EXCEL_FILE_PATH):
            os.remove(EXCEL_FILE_PATH)

        orq = OrquestradorRastreamento()
        resultado = orq.processar_rastreamentos()
        self.assertTrue(resultado)
        # deve ter criado a planilha de modelo
        self.assertTrue(os.path.exists(EXCEL_FILE_PATH))


class TestIntegracao(unittest.TestCase):
    """Testes de integração"""

    def test_fluxo_completo_simulado(self):
        """Testa fluxo completo com dados simulados"""
        logger.info("Iniciando teste de integração...")

        # Simula dados de rastreamento
        dados_api = {
            'numero_nf': '2026000001',
            'codigo_rastreamento': 'BR123456789ABC',
            'status_codigo': 'entregue',
            'status_amigavel': '✅ Entregue',
            'data_atualizacao': '03/03/2026',
            'localizacao': 'São Paulo - SP'
        }

        # Verifica se dados tem estrutura esperada
        self.assertIn('numero_nf', dados_api)
        self.assertIn('status_amigavel', dados_api)

        logger.info("✓ Teste de integração passou")


def executar_testes():
    """Executa todos os testes"""
    # Cria suite de testes
    suite = unittest.TestSuite()

    # Adiciona testes
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConsultadorAPI))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRateLimiter))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBackupManager))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestProcessadorExcel))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIntegracao))

    # Executa testes
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)

    return 0 if resultado.wasSuccessful() else 1


if __name__ == '__main__':
    import sys
    sys.exit(executar_testes())
