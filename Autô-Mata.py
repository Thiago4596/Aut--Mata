# =======================
# IMPORTAÇÕES
# =======================
from tkinter import *
from tkinter import ttk
from Ferramentas.ferramentas import Ferramentas
from Ferramentas.limpeza_windows import LimpezaArquivos
from update.atualizacao import verificar_e_baixar_atualizacao_com_gui_selecao as vbags
import sys
import threading
import ctypes
import os
import queue
import subprocess  # Importado para execução de comandos

# =======================
# FUNÇÕES DE SISTEMA
# =======================
def verificar_admin():
    """Verifica se o script está rodando como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Reinicia como administrador se necessário
if not verificar_admin():
    script = sys.argv[0]
    parametros = " ".join(f'"{arg}"' for arg in sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {parametros}', None, 1)
    sys.exit()

# =======================
# REDIRECIONADOR DE SAÍDA
# =======================
class Redirecionador:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, texto):
        self.text_widget.insert(END, texto)
        self.text_widget.see(END)

    def flush(self):
        pass

# =======================
# INICIALIZAÇÃO DA JANELA
# =======================
janela = Tk()
janela.title("Autô-Mata V: 2.5")
icone_path = os.path.join(os.path.dirname(__file__), "image", "icone.ico")
janela.iconbitmap(icone_path)
janela.geometry("500x600")
janela.resizable(False, False)
janela.config(bg="#95a5a6")

style = ttk.Style()
style.theme_use("clam")

# =======================
# CRIAÇÃO DAS ABAS
# =======================
guias = ttk.Notebook(janela)
ferramentas_aba = ttk.Frame(guias)
ferramentas_automatizadas = ttk.Frame(guias)
configuracao_aba = ttk.Frame(guias)
guias.add(ferramentas_aba, text="Ferramentas")
guias.add(ferramentas_automatizadas, text="Ferramentas Automáticas")
guias.add(configuracao_aba, text="Configuração")
guias.pack(expand=True, fill='both')

# =======================
# INSTÂNCIAS DAS CLASSES
# =======================
ferramentas = Ferramentas()
limpeza = LimpezaArquivos()  # Remova se não for usar

# =======================
# FUNÇÕES DE INTERFACE
# =======================
def atualizar_caixa_texto():
    """Atualiza a caixa de texto com conteúdo da fila."""
    try:
        while True:
            texto = ferramentas.output_queue.get_nowait()
            caixa_texto.insert(END, texto)
            caixa_texto.see(END)
    except queue.Empty:
        pass
    janela.after(100, atualizar_caixa_texto)

def executar_selecionados():
    """Executa as funções marcadas nas ferramentas automáticas."""
    for ferramenta, var in ferramentas_marcadas.items():
        if var.get():
            try:
                threading.Thread(target=getattr(ferramentas, ferramenta), daemon=True).start()
            except Exception as e:
                print(f"Erro ao executar {ferramenta}: {e}")

def executar_comando(comando):
    """Executa um comando e retorna a saída."""
    try:
        process = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode(), stderr.decode()
    except Exception as e:
        return "", str(e)

#def dism():
    #Executa a ferramenta DISM."""
""" stdout, stderr = executar_comando("DISM /Online /Cleanup-Image /CheckHealth")
    print(stdout)
    if stderr:
        print(f"Erro ao executar DISM: {stderr}") """

# =======================
# BOTÕES DA ABA FERRAMENTAS
# =======================
botoes = {
    "dism": "Ferramenta de Problemas (DISM)",
    "scannow": "Reparo do Sistema (SFC /SCANNOW)",
    "limpeza_navegadores": "Limpar Navegadores",
    "windows_active": "Verificar Ativação do Windows (SLMGR)",
    "limpeza_dns": "Limpeza de DNS (FlushDNS)",
    "verificacao_de_memoria": "Verificação de memória",
    "limpeza_de_disco": "Limpeza de disco",
    "services": "Service.msc",
    "msconfig": "Msconfig",
    "trim": "Trim",
    "limpeza_arquivos": "Limpar Recent, Temp e Prefetch"
}

# Botão extra (Chkdsk)
btn1 = ttk.Button(
    ferramentas_aba,
    text="Verificação de disco (Chkdsk)",
    command=lambda: threading.Thread(target=ferramentas.check_disk, daemon=True).start()
)
btn1.pack(pady=5, padx=10, fill='x')

# Botões dinâmicos
for func, text in botoes.items():
    btn = ttk.Button(
        ferramentas_aba,
        text=text,
        command=lambda f=func: threading.Thread(target=getattr(ferramentas, f), daemon=True).start()
    )
    btn.pack(pady=5, padx=10, fill='x')

# =======================
# CAIXA DE TEXTO DE SAÍDA
# =======================
caixa_texto = Text(height=5, width=70)
caixa_texto.pack(pady=5)
sys.stdout = Redirecionador(caixa_texto)
sys.stderr = sys.stdout

# Inicia atualização periódica da caixa de texto
atualizar_caixa_texto()

# =======================
# CHECKBOXES NA ABA AUTOMÁTICAS
# =======================
ferramentas_marcadas = {}
frame_check = Frame(ferramentas_automatizadas)
frame_check.pack(pady=10)

for func, text in botoes.items():
    var = BooleanVar()
    chk = ttk.Checkbutton(frame_check, text=text, variable=var)
    chk.pack(anchor='w', padx=10, pady=2)
    ferramentas_marcadas[func] = var

# Botão para executar selecionados
btn_executar = ttk.Button(
    ferramentas_automatizadas,
    text="Executar Selecionados",
    command=executar_selecionados
)
btn_executar.pack(pady=10)

# =======================
# CONFIGURAÇÃO
# =======================
btn_config = ttk.Button(
    configuracao_aba,
    text="Verificar Atualizações",
    command=lambda: threading.Thread(target=vbags, daemon=True).start()
)
btn_config.pack(pady=10)

# =======================
# INICIA A INTERFACE GRÁFICA
# =======================
janela.mainloop()
