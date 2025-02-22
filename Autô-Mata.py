from tkinter import *
from tkinter import ttk
from Ferramentas.ferramentas import Ferramentas
from Ferramentas.limpeza_windows import LimpezaArquivos
import sys
import threading
import subprocess
import ctypes
import os

# Função para verificar se o script está rodando como administrador
def verificar_admin():
    """
    Verifica se o script está rodando como administrador.

    Retorna:
        bool: True se o script estiver rodando como administrador, False caso contrário.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Se não estiver rodando como administrador, reinicia como admin
if not verificar_admin():
    script = sys.argv[0]
    parametros = " ".join(f'"{arg}"' for arg in sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {parametros}', None, 1)
    sys.exit()

# Fecha o terminal ao iniciar o programa (apenas no Windows)
if os.name == "nt":
    os.system("taskkill /F /IM cmd.exe")

# Classe para redirecionar a saída do terminal para a caixa de texto
class Redirecionador:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, texto):
        self.text_widget.insert(END, texto)
        self.text_widget.see(END)

    def flush(self):
        pass  # Necessário para compatibilidade com sys.stdout

# Criando a janela principal
janela = Tk()
janela.title("Autô-Mata V: 2.2")
icone_path = os.path.join(os.path.dirname(__file__), "Ferramentas", "icone.ico")
janela.iconbitmap(icone_path)
janela.geometry("500x600")
janela.resizable(False, False)
janela.config(bg="#95a5a6")

style = ttk.Style()
style.theme_use("clam")

# Criando as abas
guias = ttk.Notebook(janela)
ferramentas_aba = ttk.Frame(guias)
ferramentas_automatizadas = ttk.Frame(guias)
guias.add(ferramentas_aba, text="Ferramentas")
guias.add(ferramentas_automatizadas, text="Ferramentas Automáticas")
guias.pack(expand=True, fill='both')

# Criando instâncias das classes
ferramentas = Ferramentas()
limpeza = LimpezaArquivos()

btn1 = ttk.Button(ferramentas_aba, text="Verificação de disco (Chkdsk)", command=lambda: ferramentas.check_disk())
btn1.pack(pady=5, padx=10, fill='x')

# Função para executar as funções selecionadas
def executar_selecionados():
    for ferramenta, var in ferramentas_marcadas.items():
        if var.get():
            threading.Thread(target=getattr(ferramentas, ferramenta), daemon=True).start()

# Botões na aba "Ferramentas"
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
    "trim": "Trim"
}

for func, text in botoes.items():
    btn = ttk.Button(ferramentas_aba, text=text, command=lambda f=func: threading.Thread(target=getattr(ferramentas, f), daemon=True).start())
    btn.pack(pady=5, padx=10, fill='x')

# Caixa de texto para saída do terminal
caixa_texto = Text(ferramentas_aba, height=5, width=70)
caixa_texto.pack(pady=5)
sys.stdout = Redirecionador(caixa_texto)
sys.stderr = sys.stdout

# Checkboxes na aba "Ferramentas Automáticas"
ferramentas_marcadas = {}
frame_check = Frame(ferramentas_automatizadas)
frame_check.pack(pady=10)

for func, text in botoes.items():
    var = BooleanVar()
    chk = ttk.Checkbutton(frame_check, text=text, variable=var)
    chk.pack(anchor='w', padx=10, pady=2)
    ferramentas_marcadas[func] = var

# Botão para executar funções marcadas
btn_executar = ttk.Button(ferramentas_automatizadas, text="Executar Selecionados", command=executar_selecionados)
btn_executar.pack(pady=10)

# Iniciando a interface gráfica
janela.mainloop()
