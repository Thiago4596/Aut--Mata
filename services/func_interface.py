from tkinter import END
import queue
import threading
import subprocess

# =======================
# FUNÇÕES DE INTERFACE
# =======================
def atualizar_caixa_texto(ferramentas, caixa_texto, janela):
    """Atualiza a caixa de texto com conteúdo da fila."""
    try:
        while True:
            texto = ferramentas.output_queue.get_nowait()
            caixa_texto.insert(END, texto)
            caixa_texto.see(END)
    except queue.Empty:
        pass
    # A CORREÇÃO ESTÁ AQUI: a chamada recursiva precisa passar os argumentos novamente.
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