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
        # Tenta verificar se o script está rodando como administrador
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        # Se não for possível verificar, retorna False
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
guias = ttk.Notebook(janela)
guias.pack(expand=True, fill='both')
ferramentas = Ferramentas()
limpeza = LimpezaArquivos()

ferramentas_aba = ttk.Frame(guias)
ferramentas_automatizadas = ttk.Frame(guias)

guias.add(ferramentas_aba, text="Ferramentas")
guias.add(ferramentas_automatizadas, text="Ferramentas Automaticas")

janela.title("Autô-Mata V: 2.1")
icone_path = os.path.join(os.path.dirname(__file__), "Ferramentas", "icone.ico")

# Definir o ícone
janela.iconbitmap(icone_path)
#janela.geometry("500x600")
janela.geometry()
janela.resizable(False, False)
janela.config(bg="#95a5a6")

style = ttk.Style()
style.theme_use("clam")

# Criando botões para chamar as funções do script Ferramentas.ferramentas na aba Ferramentas
btn1 = ttk.Button(ferramentas_aba, text="Verificação de disco (Chkdsk)", command=lambda: ferramentas.check_disk())
btn1.pack(pady=5, padx=10, fill='x')

btn2 = ttk.Button(ferramentas_aba, text="Ferramenta de Problemas (DISM)", command=lambda: ferramentas.dism())
btn2.pack(pady=5, padx=10, fill='x')

btn3 = ttk.Button(ferramentas_aba, text="Reparo do Sistema (SFC /SCANNOW)", command=lambda: ferramentas.scannow())
btn3.pack(pady=5, padx=10, fill='x')

btn4 = ttk.Button(ferramentas_aba, text="Limpar Navegadores", command=lambda: ferramentas.limpeza_navegadores())
btn4.pack(pady=5, padx=10, fill='x')

btn5 = ttk.Button(ferramentas_aba, text="Verificar Ativação do Windows (SLMGR)", command=lambda: ferramentas.windows_active())
btn5.pack(pady=5, padx=10, fill='x')

btn6 = ttk.Button(ferramentas_aba, text="Limpeza de DNS (FlushDNS)", command=lambda: ferramentas.limpeza_dns())
btn6.pack(pady=5, padx=10, fill='x')

btn7 = ttk.Button(ferramentas_aba, text="Verificação de memória", command=lambda: ferramentas.verificacao_de_memoria())
btn7.pack(pady=5, padx=10, fill='x')

btn8 = ttk.Button(ferramentas_aba, text="Limpeza de disco", command=lambda: ferramentas.limpeza_de_disco())
btn8.pack(pady=5, padx=10, fill='x')

btn9 = ttk.Button(ferramentas_aba, text="Limpar a pasta Recent, Temp e Prefetch", command=lambda: limpeza.limpar_recent_temp_prefetch())
btn9.pack(pady=5, padx=10, fill='x')

btn10 = ttk.Button(ferramentas_aba, text="Service.msc", command=lambda: ferramentas.services())
btn10.pack(pady=5, padx=10, fill='x')

btn11 = ttk.Button(ferramentas_aba, text="Msconfig", command=lambda: ferramentas.msconfig())
btn11.pack(pady=5, padx=10, fill='x')

btn11 = ttk.Button(ferramentas_aba, text="Trim", command=lambda: ferramentas.trim())
btn11.pack(pady=5, padx=10, fill='x')

# Caixa de texto para exibir a saída do terminal
caixa_texto = Text(ferramentas_aba, height=5, width=70)
#caixa_texto.config(state = DISABLED)   
caixa_texto.pack(pady=5)



# Redireciona a saída do terminal para a caixa de texto
sys.stdout = Redirecionador(caixa_texto)
sys.stderr = sys.stdout

janela.mainloop()
