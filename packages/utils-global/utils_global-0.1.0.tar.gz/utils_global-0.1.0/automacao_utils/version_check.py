"""
Utilitário para verificação de novas versões da biblioteca utils-global.
"""
import re
import warnings
from datetime import datetime, timedelta
import os
import json

def verificar_versao_mais_recente(versao_atual, force=False):
    """
    Verifica se há uma versão mais recente da biblioteca disponível no GitHub.
    
    Args:
        versao_atual: Versão atual do pacote
        force: Se True, ignora o cache e sempre verifica a versão mais recente
        
    Returns:
        bool: True se uma nova versão foi encontrada, False caso contrário
    """
    try:
        import requests
        
        # Verificar se deve usar cache
        if not force and not _deve_verificar_versao():
            return False
            
        # URL para verificar a versão mais recente no GitHub (arquivo raw do setup.py na branch main)
        url = "https://raw.githubusercontent.com/gabrielpelizzari/utils-global/main/setup.py"
        
        response = requests.get(url, timeout=2)
        
        if response.status_code == 200:
            conteudo = response.text
            
            # Procura pela linha com a versão no setup.py
            match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', conteudo)
            
            if match:
                versao_github = match.group(1)
                
                # Salva informação da verificação no cache
                _atualizar_cache_versao(versao_github)
                
                # Converte para tuplas de inteiros para comparação (0.1.3 -> (0, 1, 3))
                v_atual = tuple(map(int, versao_atual.split('.')))
                v_github = tuple(map(int, versao_github.split('.')))
                
                if v_github > v_atual:
                    aviso = f"\n⚠️ Nova versão da biblioteca utils-global disponível: {versao_github} (você está usando {versao_atual}).\n"\
                           f"Para atualizar, execute: pip install --upgrade git+https://github.com/gabrielpelizzari/utils-global.git\n"
                    
                    # Mostra um aviso colorido no terminal
                    print("\033[93m" + aviso + "\033[0m")
                    
                    # Também emite um aviso do Python
                    warnings.warn(aviso)
                    
                    return True
        
        return False
    
    except Exception as e:
        # Silencia qualquer erro na verificação para não afetar o uso normal da biblioteca
        # print(f"Erro ao verificar versão: {e}")
        return False

def mostrar_ultima_versao():
    """
    Mostra informações sobre a última versão disponível da biblioteca.
    Para uso diretamente pelo usuário quando quiser verificar manualmente.
    """
    from automacao_utils import __version__
    
    # Força uma nova verificação
    if not verificar_versao_mais_recente(__version__, force=True):
        print(f"Você já está usando a versão mais recente: {__version__}")

def _deve_verificar_versao():
    """
    Determina se a biblioteca deve verificar por uma nova versão,
    baseado no tempo decorrido desde a última verificação.
    
    Returns:
        bool: True se deve verificar, False caso contrário
    """
    try:
        # Arquivo de cache para a verificação de versão
        cache_file = os.path.join(os.path.expanduser("~"), ".utils_global_version_cache.json")
        
        # Se o arquivo não existir, deve verificar
        if not os.path.exists(cache_file):
            return True
            
        # Lê o arquivo de cache
        with open(cache_file, 'r') as f:
            cache = json.load(f)
            
        # Obtém a data da última verificação
        ultima_verificacao = datetime.fromisoformat(cache.get('ultima_verificacao', '2000-01-01'))
        
        # Verifica se passou pelo menos 24 horas desde a última verificação
        return datetime.now() - ultima_verificacao > timedelta(hours=24)
            
    except Exception:
        # Em caso de erro, assume que deve verificar
        return True

def _atualizar_cache_versao(versao_github):
    """
    Atualiza o cache com a informação da última verificação.
    
    Args:
        versao_github: Versão mais recente encontrada no GitHub
    """
    try:
        # Arquivo de cache para a verificação de versão
        cache_file = os.path.join(os.path.expanduser("~"), ".utils_global_version_cache.json")
        
        # Cria o objeto de cache
        cache = {
            'ultima_verificacao': datetime.now().isoformat(),
            'ultima_versao': versao_github
        }
        
        # Salva o cache
        with open(cache_file, 'w') as f:
            json.dump(cache, f)
            
    except Exception:
        # Silencia erros ao salvar o cache
        pass

# Para teste quando o módulo é executado diretamente
if __name__ == "__main__":
    try:
        from automacao_utils import __version__
        print(f"Verificando atualizações para utils-global {__version__}...")
        mostrar_ultima_versao()
    except ImportError:
        print("Não foi possível determinar a versão atual do pacote.")
