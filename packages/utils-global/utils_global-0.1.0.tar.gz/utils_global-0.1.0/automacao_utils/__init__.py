"""
Biblioteca de funções úteis para automações com Selenium.
Fornece utilitários para manipulação de arquivos, downloads e interações com Selenium.
"""

# Versão do pacote
__version__ = "1.8.2"

# Funções de Download
from automacao_utils.download_utils import (
    processar_download,
    iniciar_monitoramento,
    aguardar_download,
    aguardar_carregamento,
    renomear_arquivo,
    is_file_in_use,
    wait_for_file_access,
    is_temp_file_growing,
    limpar_nome_arquivo,
    DownloadErroException
)

# Funções de Selenium
from automacao_utils.selenium_utils import garantir_iframe

# Funções de Notificações
from automacao_utils.notificacao_utils import enviar_msg_teams

# Funções de Movimentação de Arquivos
from automacao_utils.mover_arquivo_utils import mover_arquivo

# Verificação de versão ao importar
try:
    from automacao_utils.version_check import verificar_versao_mais_recente
    verificar_versao_mais_recente(__version__)
except ImportError:
    pass

# Funções públicas de verificação de versão
from automacao_utils.version_check import mostrar_ultima_versao