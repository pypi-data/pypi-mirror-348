import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Exceção personalizada para erros de download
class DownloadErroException(Exception):
    """
    Exceção para erros durante o processo de download.
    Contém informações sobre o erro, incluindo seletor, código e elemento específico.
    """
    def __init__(self, mensagem=None, seletor_erro=None, codigo_erro=None, elemento_visivel=None):
        self.codigo_erro = codigo_erro or "DESCONHECIDO"
        self.seletor_erro = seletor_erro
        self.elemento_visivel = elemento_visivel
        self.mensagem = mensagem or f"Erro de download: {self.codigo_erro}"
        super().__init__(self.mensagem)
        
    def __str__(self):
        return self.mensagem


class NewFileHandler(FileSystemEventHandler):
    """
    Manipulador de eventos de arquivo para monitoramento de arquivos temporários.
    
    Attributes:
        new_file_detected (bool): Indica se um arquivo temporário foi detectado.
        new_files (set): Conjunto de arquivos temporários detectados.
    """
    def __init__(self):
        super().__init__()
        self.new_file_detected = False
        self.new_files = set()

    def _handle(self, path):
        self.new_file_detected = True
        self.new_files.add(path)

    def on_created(self, event):
        if not event.is_directory:
            self._handle(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._handle(event.dest_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._handle(event.src_path)


def iniciar_monitoramento(dir_download):
    """
    Inicia o monitoramento do diretório de download.

    Args:
        dir_download: Diretório de download a ser monitorado.

    Returns:
        tuple: (handler, observer) Instâncias do manipulador de eventos e observador.
    """
    # Inicia o monitoramento do diretório
    handler = NewFileHandler()
    observer = Observer()
    observer.schedule(handler, dir_download, recursive=False)
    observer.start()

    # Aguarda que todos os emissores estejam ativos
    while not all(emitter.is_alive() for emitter in observer.emitters):
        time.sleep(0.1)
    print(" -> Monitoramento de download iniciado")

    # Limpa o estado do handler
    handler.new_file_detected = False
    handler.new_files.clear()
    
    return handler, observer


def iniciar_download(sb, btn_download, seletor_carregamento=None, iframe_carregamento=None, btn_download_js=False):
    """
    Clica no botão de download para iniciar o processo.

    Args:
        sb: Instância do SeleniumBase.
        btn_download: Elemento ou seletor para iniciar o download.
        seletor_carregamento: Seletor para verificar carregamento.
        iframe_carregamento: (Opcional) Seletor do iframe onde o elemento de carregamento está.
        btn_download_js: (Opcional) Se True, usa JavaScript para clicar no botão.
    """
    time.sleep(1)
    if isinstance(btn_download, str):
        if btn_download_js:
            sb.js_click(f"{btn_download}")
        else:
            sb.click(btn_download)
    else:
        btn_download.click()

    if seletor_carregamento:
        aguardar_carregamento(sb, seletor_carregamento, iframe=iframe_carregamento)


def aguardar_download(sb, dir_download, handler, observer, seletores_erro=None, tempo_max_espera=180, intervalo=1):
    """
    Aguarda a conclusão do download, monitorando a criação e finalização de arquivos temporários.

    Args:
        sb: Instância do SeleniumBase
        dir_download: Diretório de download
        handler: Instância do manipulador de eventos de arquivo
        observer: Instância do observador de diretório
        seletores_erro: Seletores para verificar erro
        tempo_max_espera: Tempo máximo de espera em segundos
        intervalo: Intervalo entre verificações em segundos

    Returns:
        str: Caminho do arquivo baixado.

    Raises:
        DownloadErroException: Se ocorrer algum erro durante o processo de download.
    """
    TEMP_EXTENSIONS = (".crdownload", ".part", ".tmp")
    
    
    # Aguarda a detecção de um arquivo temporário por um tempo fixo
    tempo_inicio = time.time()
    while not handler.new_file_detected:
    
        if seletores_erro:
            for seletor in seletores_erro:
                if sb.is_element_visible(seletor):
                    console_limpar_linha()
                    
                    # Obtém texto do elemento de erro
                    try:
                        texto_erro = sb.get_text(seletor) or seletor
                    except:
                        texto_erro = seletor

                    msg_erro = f"Elemento de erro visível durante o download: \n{'-'*50}\n{texto_erro}\n{'-'*50}"
            
                    # Lança a exceção com todos os detalhes
                    raise DownloadErroException(
                        mensagem=msg_erro,  
                        codigo_erro="ELEMENTO",        # Código do erro
                        elemento_visivel=seletor       # Seletor específico que estava visível
                    )

        if time.time() - tempo_inicio > tempo_max_espera:  
            observer.stop()
            observer.join()
            console_limpar_linha()
            msg_erro = "Tempo limite excedido aguardando o início do download"
            print(msg_erro)
            raise Exception(msg_erro)

        console_carregamento("Aguardando início do download")
        time.sleep(intervalo)

    console_limpar_linha()
    print(" -> Download iniciado!")

    # Aguarda que o download seja concluído (ou seja, até que os arquivos temporários sumam do diretório)
    tempo_inicio_download = time.time()
    
    while any(arquivo.endswith(TEMP_EXTENSIONS) for arquivo in os.listdir(dir_download)):
        if seletores_erro:
            for seletor in seletores_erro:
                if sb.is_element_visible(seletor):
                    console_limpar_linha()
                    
                    # Obtém texto do elemento de erro
                    try:
                        texto_erro = sb.get_text(seletor) or seletor
                    except:
                        texto_erro = seletor
                    
                    msg_erro = f"Elemento de erro visível durante o download: \n{'-'*50}\n{texto_erro}\n{'-'*50}"
                    
                    # Lança a exceção com todos os detalhes
                    raise DownloadErroException(
                        mensagem=msg_erro,
                        codigo_erro="ELEMENTO",        # Código do erro
                        elemento_visivel=seletor       # Seletor específico que estava visível
                    )

        # Se o tempo máximo foi atingido, verificamos se o download ainda está ativo
        if time.time() - tempo_inicio_download > tempo_max_espera:
            # Verifica se algum arquivo ainda está crescendo
            if is_temp_file_growing(dir_download, TEMP_EXTENSIONS, duration=20, check_interval=1):
                console_limpar_linha()
                print(f" -> O download ainda está em progresso, continuando a espera... ({int(time.time() - tempo_inicio_download)}s)")
                tempo_inicio_download = time.time()  # Reinicia o contador, já que ainda há progresso
            else:
                observer.stop()
                observer.join()
                console_limpar_linha()

                msg_erro = "Tempo limite excedido durante o download"
                print(msg_erro)
                raise Exception(msg_erro)
        
        console_carregamento("Baixando arquivo")
        time.sleep(intervalo)
    
    console_limpar_linha()
    print(" -> Download concluído!")
    
    observer.stop()
    observer.join()

    # Filtra os arquivos finais (excluindo os temporários)
    arquivos_finais = [
        arquivo
        for arquivo in handler.new_files
        if not arquivo.endswith(TEMP_EXTENSIONS)]
    
    if arquivos_finais:
        # Encontra o arquivo mais recente (provavelmente o que acabou de ser baixado)
        caminho_arquivo_baixado = max(map(os.path.abspath, arquivos_finais), key=os.path.getmtime)
        
        time.sleep(0.5) 

        # Verificar se o arquivo está crescendo antes de continuar
        while is_temp_file_growing(dir_download, TEMP_EXTENSIONS, duration=5, check_interval=1):
            console_carregamento(f"Finalizando arquivo {os.path.basename(caminho_arquivo_baixado)}")
        
        console_limpar_linha()
        
        # Verificar se o arquivo está disponível para acesso
        if is_file_in_use(caminho_arquivo_baixado):
            while is_file_in_use(caminho_arquivo_baixado):
                console_carregamento("Aguardando liberação do arquivo")
                time.sleep(0.5)
            
            console_limpar_linha()

        time.sleep(1)
        
        return caminho_arquivo_baixado
        
    else:
        handler.new_files.clear()
        
        msg_erro = "Nenhum arquivo detectado após o download"
        print(msg_erro)
        raise Exception(msg_erro)


def processar_download(sb, dir_download, btn_download, nome_arquivo=None, seletores_erro=None, seletor_carregamento=None, iframe_carregamento=None, btn_download_js=False):
    """
    Processa o download de um arquivo, monitorando o diretório de download e renomeando o arquivo.
    
    Args:
        sb: Instância do SeleniumBase
        dir_download: Diretório onde o arquivo será baixado
        btn_download: Seletor do botão de download ou objeto clicável
        nome_arquivo: (Opcional) Nome do arquivo após o download; se None, não será renomeado
        seletores_erro: (Opcional) Seletor ou lista de seletores para verificar erros. Pode ser:
                       - Uma string única com um seletor: "seletor1"
                       - Uma lista de seletores: ["seletor1", "seletor2", ...]
        seletor_carregamento: (Opcional) Seletor opcional para aguardar o carregamento desaparecer
        iframe_carregamento: (Opcional) Seletor do iframe onde o elemento de carregamento está
        btn_download_js: (Opcional) Se o botão de download é um objeto JavaScript
        
    Returns:
        str: Caminho completo para o arquivo baixado e renomeado (ou apenas baixado, se nome_arquivo for None).
        
    Raises:
        DownloadErroException: Se ocorrer algum erro durante o processo de download.
    """
    intervalo = 1
    
    # Normaliza seletores_erro para uma lista, se não for None
    if seletores_erro is not None:
        if isinstance(seletores_erro, str):
            # Se for uma string, converte para lista com um elemento
            seletores_erro = [seletores_erro]
    
    # Inicia o monitoramento
    handler, observer = iniciar_monitoramento(dir_download)
    
    # Inicia o download
    iniciar_download(sb, btn_download, seletor_carregamento, iframe_carregamento, btn_download_js)
    
    # Aguarda o download ser concluído e retorna o caminho do arquivo
    caminho_arquivo_baixado = aguardar_download(sb, dir_download, handler, observer, seletores_erro, tempo_max_espera=180, intervalo=intervalo)
    
    # Se nome_arquivo for passado, renomeia; caso contrário, retorna o caminho original
    if nome_arquivo:
        caminho_final = renomear_arquivo(caminho_arquivo_baixado, nome_arquivo)
    else:
        caminho_final = caminho_arquivo_baixado

    return caminho_final




def split_nome_ext(nome, tamanho_max_ext=4):
    """
    Separa o nome da extensão, considerando apenas o último ponto,
    e valida se a parte após o ponto é curta o suficiente para ser uma extensão.
    
    Args:
        nome (str): Nome do arquivo.
        tamanho_max_ext (int): Tamanho máximo esperado para uma extensão (sem o ponto).
    
    Returns:
        tuple: (nome_sem_ext, ext) onde ext inclui o ponto, ou uma string vazia se não houver extensão.
    """
    partes = nome.rsplit('.', 1)
    if len(partes) == 2 and 1 <= len(partes[1]) <= tamanho_max_ext:
        return partes[0], '.' + partes[1]
    return nome, ""



def limpar_nome_arquivo(nome):
    """
    Limpa o nome do arquivo, removendo caracteres inválidos e truncando o nome.
    
    Args:
        nome (str): Nome do arquivo.
        
    Returns:
        str: Nome do arquivo limpo.
    """
    try:
        # Remove caracteres inválidos para o Windows
        caracteres_invalidos = ["<", ">", ":", "'", "/", "\\", "|", "?", "*", '"']
        for char in caracteres_invalidos:
            nome = nome.replace(char, " ")

        # Trunca o nome do arquivo para um tamanho máximo permitido
        nome_limpo = nome[:250] if len(nome) > 250 else nome
        return nome_limpo.strip()
    except Exception as e:
        msg_erro = f"Erro ao usar a função limpar_nome_arquivo: {e}"
        raise Exception(msg_erro)




def renomear_arquivo(caminho_arquivo, novo_nome):
    """
    Renomeia um arquivo, permitindo renomear também a extensão se desejado.
    
    Se 'novo_nome' já contiver uma extensão válida (por exemplo, 'arquivo.txt'),
    essa extensão será utilizada; caso contrário, a extensão original do arquivo é mantida.
    
    Args:
        caminho_arquivo (str): Caminho do arquivo original.
        novo_nome (str): Novo nome do arquivo, com ou sem extensão.
        
    Returns:
        str: Caminho do arquivo renomeado.
    """
    import os

    try:
        diretorio_base = os.path.dirname(caminho_arquivo)
        
        # Separa o nome e a extensão usando nossa função customizada
        base_nome, ext_novo = split_nome_ext(novo_nome)
        
        if not ext_novo:
            base_nome = limpar_nome_arquivo(novo_nome)
            ext = os.path.splitext(caminho_arquivo)[1]
        else:
            base_nome = limpar_nome_arquivo(base_nome)
            ext = ext_novo
        
        novo_nome_final = base_nome + ext
        novo_caminho = os.path.join(diretorio_base, novo_nome_final)
        
        contador = 1
        while os.path.exists(novo_caminho):
            novo_nome_final = f"{base_nome} ({contador}){ext}"
            novo_caminho = os.path.join(diretorio_base, novo_nome_final)
            contador += 1
        
        os.rename(caminho_arquivo, novo_caminho)
        print(f"Arquivo renomeado para: {novo_caminho}")

        if is_file_in_use(novo_caminho):
            print(' -> Arquivo ainda está em uso. Aguardando liberação...')
            wait_for_file_access(novo_caminho)
            
        return novo_caminho

    except Exception as e:
        msg_erro = f"Erro ao usar a função renomear_arquivo: {e}"
        raise Exception(msg_erro)



# * Funções auxiliares para interface do console
# Variável global para controlar o estado da animação de carregamento
_carregamento_indice = 0


def console_carregamento(mensagem="Carregando", indice=None):
    """
    Exibe uma mensagem de carregamento animada no console.
    
    Args:
        mensagem (str): Texto base da mensagem de carregamento (padrão: "Carregando")
        indice (int, opcional): Índice de estado atual. Se None, usa o contador global sequencial.
    
    Returns:
        int: Próximo índice de estado para ser usado na próxima chamada (opcional)
    """
    global _carregamento_indice
    estados = ['.', '..', '...']
    
    # Se não foi fornecido um índice, usa o contador global sequencial
    if indice is None:
        indice = _carregamento_indice
        _carregamento_indice = (_carregamento_indice + 1) % len(estados)
    else:
        indice = indice % len(estados)
    
    # Exibe a mensagem
    print(f"\r{mensagem}{estados[indice]}   ", end='')
    
    # Retorna o próximo índice para quem quiser controlar a sequência manualmente
    return (indice + 1) % len(estados)

def console_limpar_linha():
    """
    Limpa a linha atual do console.
    """
    print("\r" + " " * 50, end='\r')  # Imprime espaços em branco e volta ao início da linha

# * Aguardar o carregamento da página   
def aguardar_carregamento(sb, elemento, iframe=None):
    """
    Aguarda o carregamento de uma página web, aguardando o elemento de carregamento ficar não visível.

    Args:
        sb: Instância do SeleniumBase.
        elemento: Elemento ou seletor de carregamento.
        iframe: (Opcional) Seletor do iframe onde o elemento está, se conhecido.
    """
    try:
        tempo_verificacao = 0.4 # Mudar conforme necessidade de intervalo de espera para verificação
        contador_nao_visivel = 0
        tempo_total = 0
        tempo_maximo = 600 # Limite maximo de espera em segundos (mudar conforme necessidade)

        # Abordagem otimizada para lidar com iframes
        sb.switch_to_default_content()
        
        # Se o iframe foi especificado, usa ele diretamente
        if iframe:
            sb.switch_to_frame(iframe)

        # Loop de verificação da visibilidade do elemento
        while contador_nao_visivel < 3 and tempo_total < tempo_maximo: 
            if not sb.is_element_visible(elemento):
                contador_nao_visivel += 1 
        
            sb.sleep(tempo_verificacao)
            tempo_total += tempo_verificacao

            console_carregamento("Carregando")

        # Limpa o console após o carregamento
        console_limpar_linha()
        
        # Volta para o default content, se necessário
        sb.switch_to_default_content()

        # Se o temporizador ultrapassar o tempo máximo, lança uma exceção
        if tempo_total >= tempo_maximo:
            raise TimeoutError(f"O tempo de espera para o elemento '{elemento}' ultrapassou o limite de {tempo_maximo} segundos.")
        
    except Exception as e:
        print(f"Ocorreu um erro ao aguardar carregamento: {e}")  

        raise   

def is_file_in_use(file_path):
    """
    Verifica se um arquivo está em uso por outro processo.
    
    Args:
        file_path (str): Caminho do arquivo para verificar.
        
    Returns:
        bool: True se o arquivo estiver em uso, False caso contrário.
    """
    try:
        with open(file_path, 'rb+') as file:
            return False
    except (IOError, PermissionError):
        return True
    except Exception as e:
        print(f"Erro ao verificar se o arquivo está em uso: {e}")
        return True  # Em caso de erro, assume que o arquivo está em uso por precaução


def wait_for_file_access(file_path, max_retries=30, retry_interval=1):
    """
    Aguarda até que um arquivo esteja disponível para acesso.
    
    Args:
        file_path (str): Caminho do arquivo para verificar.
        max_retries (int): Número máximo de tentativas.
        retry_interval (float): Intervalo entre as tentativas em segundos.
        
    Returns:
        bool: True se o arquivo estiver disponível, False caso contrário.
    """
    retry_count = 0
    while retry_count < max_retries:
        if not is_file_in_use(file_path):
            return True
        print(f" -> Arquivo {os.path.basename(file_path)} está em uso. Aguardando... ({retry_count + 1}/{max_retries})")
        time.sleep(retry_interval)
        retry_count += 1
    
    print(f" -> Timeout atingido. Arquivo {os.path.basename(file_path)} continua em uso após {max_retries} tentativas.")
    return False

def is_temp_file_growing(directory, temp_extensions=(".crdownload", ".part", ".tmp"), duration=10, check_interval=1):
    """
    Verifica se algum arquivo temporário dentro do diretório ainda está crescendo.

    Args:
        directory (str): Diretório a ser monitorado.
        temp_extensions (tuple): Extensões de arquivos temporários que indicam um download em andamento.
        duration (int): Tempo total para verificar crescimento (segundos).
        check_interval (int): Intervalo entre verificações (segundos).

    Returns:
        bool: True se algum arquivo temporário ainda estiver crescendo, False caso contrário.
    """
    temp_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(temp_extensions)]
    
    if not temp_files:
        return False  # Nenhum arquivo temporário encontrado, então não há crescimento

    file_sizes = {file: os.path.getsize(file) for file in temp_files}

    for _ in range(int(duration / check_interval)):
        time.sleep(check_interval)
        growing = False
        for file in temp_files:
            if os.path.exists(file):  # Verifica se o arquivo ainda existe
                new_size = os.path.getsize(file)
                if new_size > file_sizes[file]:  # O arquivo está crescendo
                    growing = True
                file_sizes[file] = new_size  # Atualiza o tamanho para a próxima checagem
        if growing:
            return True  # Se algum arquivo temporário cresceu, o download ainda está em andamento

    return False  # Se nenhum arquivo temporário cresceu dentro do período, o download pode ter parado
