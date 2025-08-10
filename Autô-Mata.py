# =======================
# IMPORTAÇÕES
# =======================
from tkinter import *
from tkinter import ttk
from Ferramentas.ferramentas import Ferramentas
from Ferramentas.limpeza_windows import LimpezaArquivos
from services.func_interface import atualizar_caixa_texto as act
from services.chckbox_automática import checkbox_aba_automática as cba
from update.atualizacao import CURRENT_APP_VERSION, verificar_e_baixar_atualizacao_com_gui_selecao as vbags
from services.admin import verificar_admin as veri_a
import sys
import threading
import os

# =======================
# FUNÇÕES DE SISTEMA
# =======================
veri_a()

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
janela.title(f"Autô-Mata V: {CURRENT_APP_VERSION}")
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
limpeza = LimpezaArquivos()

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
act(ferramentas, caixa_texto, janela)

# =======================
# CHECKBOXES NA ABA AUTOMÁTICAS
# =======================
cba(ferramentas_automatizadas, botoes, ferramentas)

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
