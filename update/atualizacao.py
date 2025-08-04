import requests
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from packaging.version import parse as parse_version

# ==============================================================================
# CONFIGURAÇÃO GERAL (Variáveis definidas diretamente no script)
# ==============================================================================
# Defina a versão atual do seu aplicativo.
CURRENT_APP_VERSION = "2.7"

# Parâmetros do Repositório GitHub
GITHUB_OWNER = "Thiago4596"
GITHUB_REPO = "Auto-Mata"
# O token é definido como None, pois o repositório é público e não exige autenticação.
GITHUB_TOKEN = None

# Identificador para o arquivo de atualização esperado na release.
TARGET_FILE_IDENTIFIER = ".exe"

# O diretório padrão de download (pode ser sobrescrito pelo usuário via GUI)
# Não é estritamente necessário se você sempre pede ao usuário, mas pode ser um fallback.
DOWNLOAD_DIR = "downloads"


# ==============================================================================
# FUNÇÕES DE INTERAÇÃO COM A API DO GITHUB
# ==============================================================================

def get_latest_github_release(owner: str, repo: str, token: str = None) -> dict | None:
    """
    Busca os detalhes da release mais recente de um repositório GitHub.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token: # O cabeçalho de autorização só é adicionado se um token for fornecido
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de Conexão", f"Não foi possível acessar a API do GitHub: {e}")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Erro de Dados", "A resposta da API do GitHub não é um JSON válido.")
        return None

def download_file(url: str, destination_path: str) -> bool:
    """
    Baixa um arquivo de uma URL para um caminho de destino especificado.
    """
    messagebox.showinfo("Download", f"Iniciando download de: {os.path.basename(destination_path)}")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(destination_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        messagebox.showinfo("Download Concluído", f"Download concluído:\n{destination_path}")
        return True
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de Download", f"Falha ao baixar o arquivo: {e}")
        return False
    except IOError as e:
        messagebox.showerror("Erro de Arquivo", f"Não foi possível salvar o arquivo em {destination_path}: {e}")
        return False

# ==============================================================================
# FUNÇÃO PRINCIPAL DE ATUALIZAÇÃO (Com seleção de pasta via GUI)
# ==============================================================================

def verificar_e_baixar_atualizacao_com_gui_selecao():
    """
    Verifica a versão mais recente do aplicativo no GitHub e, se houver uma nova versão,
    pede ao usuário para selecionar a pasta de download e baixa o arquivo.
    Usa caixas de diálogo Tkinter para interação.
    """
    root = tk.Tk()
    root.withdraw() # Esconde a janela principal do Tkinter

    print("Verificando atualizações...")
    # Parse da versão atual do aplicativo

    current_version_parsed = parse_version(CURRENT_APP_VERSION)
    latest_release_info = get_latest_github_release(GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN)

    if not latest_release_info:
        return # A mensagem de erro já foi mostrada por get_latest_github_release

    latest_tag = latest_release_info.get('tag_name', 'N/A')
    if latest_tag == 'N/A':
        messagebox.showwarning("Aviso", "A release mais recente encontrada não possui uma 'tag_name' válida.")
        return

    latest_version_parsed = parse_version(latest_tag)

    if latest_version_parsed > current_version_parsed:
        response = messagebox.askyesno(
            "Nova Versão Disponível",
            f"Uma nova versão ({latest_tag}) está disponível! Sua versão é {CURRENT_APP_VERSION}.\n\nDeseja baixar a atualização agora?"
        )
        
        if not response:
            messagebox.showinfo("Atualização Cancelada", "Atualização cancelada pelo usuário.")
            return

        assets = latest_release_info.get('assets', [])
        download_url = None
        asset_name = None

        if assets:
            for asset in assets:
                if TARGET_FILE_IDENTIFIER.lower() in asset.get('name', '').lower():
                    download_url = asset.get('browser_download_url')
                    asset_name = asset.get('name')
                    break
            
            if download_url and asset_name:
                selected_dir = filedialog.askdirectory(
                    title="Selecione o diretório para baixar a atualização",
                    initialdir=os.path.expanduser("~")
                )

                if not selected_dir:
                    messagebox.showwarning("Download Cancelado", "Nenhum diretório selecionado. Download cancelado.")
                    return
                    
                destination_path = os.path.join(selected_dir, asset_name)
                
                if download_file(download_url, destination_path):
                    messagebox.showinfo("Sucesso", f"A nova versão foi baixada para:\n{destination_path}\n\nPor favor, instale a nova versão.")
                else:
                    messagebox.showerror("Falha", "Não foi possível concluir o download da atualização.")
            else:
                messagebox.showwarning("Arquivo Não Encontrado", f"Nenhum arquivo de atualização '{TARGET_FILE_IDENTIFIER}' encontrado na release {latest_tag}.")
                if assets:
                    asset_names = "\n".join([a.get('name', 'Nome desconhecido') for a in assets])
                    messagebox.showinfo("Assets Disponíveis", f"Assets disponíveis nesta release:\n{asset_names}")
        else:
            messagebox.showwarning("Aviso", "Nenhuma asset (arquivo) encontrada para a release mais recente.")
    elif latest_version_parsed < current_version_parsed:
        messagebox.showinfo("Versão", f"Sua versão ({CURRENT_APP_VERSION}) é mais recente que a do GitHub ({latest_tag}).")
    else:
        messagebox.showinfo("Versão Atualizada", f"Você já está na versão mais recente: {latest_tag}.")

    root.destroy()
