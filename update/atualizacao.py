import requests
import os
import shutil
import json
import zipfile
import time

# --- Configurações do Repositório GitHub ---
GITHUB_REPO_OWNER = 'Thiago4596'
GITHUB_REPO_NAME = 'Auto-Mata'
GITHUB_API_BASE_URL = f'https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}'
# VERIFIQUE AQUI: Use 'main' se for o branch padrão do seu repositório (mais comum agora)
# Caso contrário, use 'master'
GITHUB_RAW_BASE_URL = f'https://raw.githubusercontent.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/Master'

# Caminho para o arquivo de versão local
LOCAL_VERSION_FILE = 'VERSION.txt'

# --- Funções de Verificação de Versão ---
def get_local_version():
    """Lê a versão atual do aplicativo."""
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, 'r') as f:
            return f.read().strip()
    return '0.0'

def get_remote_version():
    """Busca a versão mais recente do GitHub a partir do VERSION.txt no branch principal."""
    try:
        response = requests.get(f'{GITHUB_RAW_BASE_URL}/VERSION.txt')
        response.raise_for_status() # Levanta erro para status 4xx/5xx
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar versão remota: {e}")
        return None

# --- Função de Download e Extração ---
def download_and_extract_latest_release(target_dir='.'):
    """
    Baixa o arquivo zip da última release do GitHub e extrai.
    Prioriza o 'zipball_url' (código-fonte) e depois procura outros .zip nos assets.
    """
    try:
        response = requests.get(f'{GITHUB_API_BASE_URL}/releases/latest')
        response.raise_for_status()
        release_info = response.json()

        zip_url = release_info.get('zipball_url')
        if zip_url:
            zip_filename = f"{GITHUB_REPO_NAME}-{release_info['tag_name']}.zip"
        else:
            # Fallback: procura por .zip nos assets (se anexado manualmente)
            assets = release_info.get('assets', [])
            for asset in assets:
                if asset['name'].endswith('.zip'):
                    zip_url = asset['browser_download_url']
                    zip_filename = asset['name']
                    break
        
        if not zip_url:
            print("Nenhum arquivo .zip encontrado na última release.")
            return False

        download_path = os.path.join(target_dir, zip_filename)

        # Remove o arquivo ZIP antigo se existir, para garantir um download limpo
        if os.path.exists(download_path):
            try:
                os.remove(download_path)
                time.sleep(0.1) # Pequena pausa para liberar bloqueio
            except PermissionError as e:
                print(f"Aviso: Não foi possível remover o ZIP antigo. Erro: {e}")
            except Exception as e:
                print(f"Aviso: Erro inesperado ao remover ZIP antigo: {e}")

        # Baixa o arquivo
        with requests.get(zip_url, stream=True) as r:
            r.raise_for_status()
            with open(download_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Descompacta e move os arquivos
        temp_extract_dir = "temp_update_extract"
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
        os.makedirs(temp_extract_dir)

        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_dir)
        
        time.sleep(0.5) # Pausa para o SO liberar o arquivo ZIP

        extracted_contents = os.listdir(temp_extract_dir)
        if not extracted_contents:
            print("Erro: O arquivo ZIP está vazio ou não contém arquivos após a extração.")
            return False

        # Encontra a pasta raiz extraída (se houver apenas uma pasta dentro do zip)
        source_path = temp_extract_dir
        if len(extracted_contents) == 1 and os.path.isdir(os.path.join(temp_extract_dir, extracted_contents[0])):
            source_path = os.path.join(temp_extract_dir, extracted_contents[0])

        # Move os arquivos para o diretório de destino
        for item_name in os.listdir(source_path):
            s = os.path.join(source_path, item_name)
            d = os.path.join(target_dir, item_name)
            
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                if os.path.exists(d):
                    os.remove(d)
                shutil.copy2(s, d)

        # Limpa arquivos temporários
        shutil.rmtree(temp_extract_dir)
        if os.path.exists(download_path):
            os.remove(download_path)

        return True

    except (requests.exceptions.RequestException, json.JSONDecodeError, zipfile.BadZipFile, PermissionError) as e:
        print(f"Erro durante a atualização: {e}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a atualização: {e}")
        import traceback
        traceback.print_exc()
        return False

# --- Função Principal de Verificação ---
def check_for_updates():
    """Verifica se há atualizações e pergunta ao usuário se deseja atualizar."""
    local_version = get_local_version()
    remote_version = get_remote_version()

    print(f"Versão local: {local_version}")
    print(f"Versão remota: {remote_version}")

    if remote_version is None:
        print("Não foi possível verificar atualizações no momento.")
        return False

    try:
        # Comparação de versões numérica
        if float(remote_version) > float(local_version):
            print(f"Uma nova versão ({remote_version}) está disponível!")
            confirm = input("Deseja atualizar agora? (s/n): ").lower()
            if confirm == 's':
                if download_and_extract_latest_release():
                    print("Atualização concluída com sucesso! Por favor, reinicie o aplicativo.")
                    return True
                else:
                    print("Falha ao aplicar a atualização.")
                    return False
            else:
                print("Atualização adiada.")
                return False
        elif float(remote_version) == float(local_version):
            print("Seu aplicativo já está na versão mais recente.")
            return False
        else: # remote_version < local_version
             print("Sua versão local é mais recente que a remota disponível. Nenhuma atualização necessária.")
             return False
    except ValueError:
        print("Erro: Formato de versão inválido para comparação numérica. Verifique VERSION.txt.")
        return False

# --- Exemplo de Uso ---
if __name__ == "__main__":
    if not os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, 'w') as f:
            f.write('1.0') # Versão inicial para testes

    print("Iniciando o aplicativo...")
    check_for_updates()
    print("Aplicativo em execução (ou reiniciando após a atualização)...")
    # Seu código principal do aplicativo viria aqui