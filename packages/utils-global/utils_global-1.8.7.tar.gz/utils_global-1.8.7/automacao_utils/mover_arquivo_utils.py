import os
import shutil

def mover_arquivo(diretorio_origem, diretorio_destino, nome_arquivo=None, substituir=True, max_arquivos=10):
    """
    Copia um arquivo do diretório de origem para o diretório de destino e exclui o arquivo original.
    
    Args:
        diretorio_origem: Caminho completo do arquivo a ser movido ou diretório de origem.
        diretorio_destino: Caminho do diretório de destino.
        nome_arquivo: Nome específico do arquivo a ser movido (opcional).
            Se None e diretorio_origem for um arquivo, usa o nome do arquivo no caminho.
            Se None e diretorio_origem for um diretório, move todos os arquivos do diretório.
        substituir: Se True, substitui o arquivo de destino caso já exista um com o mesmo nome.
            Se False (padrão), adiciona um contador no nome do arquivo caso já exista.
        max_arquivos: Número máximo de arquivos que podem ser movidos em uma única operação.
            Se for mover mais arquivos que este limite, será solicitada uma confirmação.
        
    Returns:
        Lista de caminhos dos arquivos no diretório de destino.
    """
    
    try:
        arquivos_movidos = []
        arquivos_para_mover = []
        
        # Verifica se diretorio_origem é um arquivo
        if os.path.isfile(diretorio_origem):
            # Extrai o nome do arquivo do caminho completo
            nome_arquivo_origem = os.path.basename(diretorio_origem)
            diretorio_origem_base = os.path.dirname(diretorio_origem)
            
            # Define o caminho de destino
            caminho_destino = os.path.join(diretorio_destino, nome_arquivo_origem)
            
            # Usa o nome_arquivo se fornecido
            if nome_arquivo:
                caminho_destino = os.path.join(diretorio_destino, nome_arquivo)
            
            # Verifica se o arquivo já existe no destino
            nome_base, extensao = os.path.splitext(os.path.basename(caminho_destino))
            contador = 1
            if not substituir:
                while os.path.exists(caminho_destino):
                    novo_nome = f"{nome_base} ({contador}){extensao}"
                    caminho_destino = os.path.join(diretorio_destino, novo_nome)
                    contador += 1
            
            arquivos_para_mover.append((diretorio_origem, caminho_destino))
            
        # Se diretorio_origem é um diretório
        elif os.path.isdir(diretorio_origem):
            # Se um nome de arquivo específico foi fornecido
            if nome_arquivo:
                caminho_origem = os.path.join(diretorio_origem, nome_arquivo)
                if os.path.exists(caminho_origem):
                    caminho_destino = os.path.join(diretorio_destino, nome_arquivo)
                    
                    # Verifica se o arquivo já existe no destino
                    if not substituir:
                        contador = 1
                        nome_base, extensao = os.path.splitext(nome_arquivo)
                        while os.path.exists(caminho_destino):
                            novo_nome = f"{nome_base} ({contador}){extensao}"
                            caminho_destino = os.path.join(diretorio_destino, novo_nome)
                            contador += 1
                    
                    arquivos_para_mover.append((caminho_origem, caminho_destino))
                else:
                    print(f"Arquivo não encontrado: {caminho_origem}")
            
            # Se nenhum nome de arquivo específico foi fornecido, move todos os arquivos
            else:
                arquivos = [f for f in os.listdir(diretorio_origem) if os.path.isfile(os.path.join(diretorio_origem, f))]
                
                if not arquivos:
                    print(f"Nenhum arquivo encontrado no diretório de origem: {diretorio_origem}")
                    return []
                
                for arquivo in arquivos:
                    caminho_origem = os.path.join(diretorio_origem, arquivo)
                    caminho_destino = os.path.join(diretorio_destino, arquivo)
                    
                    # Verifica se o arquivo já existe no destino
                    if not substituir:
                        contador = 1
                        nome_base, extensao = os.path.splitext(arquivo)
                        while os.path.exists(caminho_destino):
                            novo_nome = f"{nome_base} ({contador}){extensao}"
                            caminho_destino = os.path.join(diretorio_destino, novo_nome)
                            contador += 1
                    
                    arquivos_para_mover.append((caminho_origem, caminho_destino))
        else:
            raise Exception(f"O caminho especificado não existe: {diretorio_origem}")
        
        # Verifica o número de arquivos a serem movidos
        num_arquivos = len(arquivos_para_mover)
        if num_arquivos == 0:
            return []
            
        # Verifica se excede o limite e precisa de confirmação
        if num_arquivos > max_arquivos:
            print(f"Arquivos a serem movidos ({num_arquivos}):")
            for idx, (origem, destino) in enumerate(arquivos_para_mover, 1):
                print(f"{idx}. {origem} -> {destino}")
                
            resposta = input(f"ATENÇÃO: Você está prestes a mover {num_arquivos} arquivos, o que excede o limite de {max_arquivos}. Deseja continuar? (s/n): ").lower()
            if resposta != 's':
                print("Operação cancelada pelo usuário.")
                return []
        
        # Verifica se o diretório de destino existe
        if not os.path.exists(diretorio_destino):
            os.makedirs(diretorio_destino, exist_ok=True)
            print(f"Diretório de destino criado: {diretorio_destino}")
        
        # Move os arquivos
        for origem, destino in arquivos_para_mover:
            shutil.copy2(origem, destino)
            os.remove(origem)
            arquivos_movidos.append(destino)
            print(f"Arquivo movido: {origem} -> {destino}")
        
        return arquivos_movidos
    
    except Exception as e:
        msg_erro = f"Erro ao mover arquivo(s): {e}"
        raise Exception(msg_erro)