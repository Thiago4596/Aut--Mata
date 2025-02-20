from tkinter import *
from tkinter import ttk
from Ferramentas.ferramentas import Ferramentas
import sys
import threading
import subprocess
import ctypes
import os

# Função para verificar se o script está rodando como administrador
def verificar_admin():
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

# Função para executar funções do script ferramentas.py e capturar saída
def executar_funcao(funcaopy):
    def run():
        process = subprocess.Popen(
            [sys.executable, "-c", f"import Ferramentas.ferramentas; Ferramentas.ferramentas.{funcaopy}()"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
        )
        for linha in process.stdout:
            sys.stdout.write(linha)
        for linha in process.stderr:
            sys.stderr.write(linha)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

# Criando a janela principal
janela = Tk()
ferramentas = Ferramentas()

janela.title("Autô-Mata V: 2.0")
icone_path = os.path.join(os.path.dirname(__file__), "Ferramentas", "icone.ico")

# Definir o ícone
janela.iconbitmap(icone_path)
janela.geometry("500x400")
janela.config(bg="#95a5a6")

style = ttk.Style()
style.theme_use("clam")

# Criando botões para chamar as funções do script Ferramentas.ferramentas
btn1 = ttk.Button(janela, text="Verificação de disco (Chkdsk)", command=lambda: ferramentas.check_disk())
btn1.pack(pady=10, padx=20, fill='x')

btn2 = ttk.Button(janela, text="Ferramenta de Problemas (DISM)", command=lambda: ferramentas.dism())
btn2.pack(pady=10, padx=20, fill='x')

btn3 = ttk.Button(janela, text="Reparo do Sistema (SFC /SCANNOW)", command=lambda: ferramentas.scannow())
btn3.pack(pady=10, padx=20, fill='x')

btn4 = ttk.Button(janela, text="Limpar Navegadores", command=lambda: ferramentas.limpeza_navegadores())
btn4.pack(pady=10, padx=20, fill='x')

btn5 = ttk.Button(janela, text="Verificar Ativação do Windows (SLMGR)", command=lambda: ferramentas.windows_active())
btn5.pack(pady=10, padx=20, fill='x')

btn6 = ttk.Button(janela, text="Limpeza de DNS (FlushDNS)", command=lambda: ferramentas.limpeza_dns())
btn6.pack(pady=10, padx=20, fill='x')

# Caixa de texto para exibir a saída do terminal
caixa_texto = Text(janela, height=10, width=70)
caixa_texto.pack(pady=10)

# Redireciona a saída do terminal para a caixa de texto
sys.stdout = Redirecionador(caixa_texto)
sys.stderr = sys.stdout

janela.mainloop()
