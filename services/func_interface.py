from tkinter import END
import threading
import subprocess
import sys

# =======================
# FUNÇÕES DE INTERFACE
# =======================
def atualizar_caixa_texto(ferramentas, caixa_texto, janela):
    """Atualiza a caixa de texto com conteúdo da fila."""
    # A lógica de atualização da caixa de texto agora é tratada pelo Redirecionador
    # em Autô-Mata.py, que intercepta sys.stdout. Não precisamos mais de uma fila aqui.
    # Esta função pode ser removida ou adaptada se houver necessidade de alguma
    # lógica de interface específica que não seja apenas exibir texto.
    # Por enquanto, ela pode ser um placeholder ou ser removida se não for mais necessária.
    janela.after(100, atualizar_caixa_texto, ferramentas, caixa_texto, janela)

def executar_selecionados(ferramentas, ferramentas_marcadas):
    """Executa as funções marcadas nas ferramentas automáticas."""
    for ferramenta, var in ferramentas_marcadas.items():
        if var.get():
            try:
                threading.Thread(target=getattr(ferramentas, ferramenta), daemon=True).start()
            except Exception as e:
                # Agora esta saída irá para a caixa de texto
                print(f"Erro ao executar {ferramenta}: {e}")

def executar_comando(comando):
    """Executa um comando e retorna a saída."""
    try:
        process = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode(), stderr.decode()
    except Exception as e:
        return "", str(e)


