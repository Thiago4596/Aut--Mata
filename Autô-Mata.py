# =======================
# IMPORTAÇÕES
# =======================
from tkinter import *
from tkinter import ttk
import tkinter as tk
import sys
import threading
import os

# Importações de módulos do seu projeto
# Certifique-se de que esses arquivos estão no caminho correto
try:
    from Ferramentas.ferramentas import Ferramentas
    from Ferramentas.limpeza_windows import LimpezaArquivos
    from services.func_interface import atualizar_caixa_texto as act
    from services.chckbox_automática import checkbox_aba_automática as cba
    from update.atualizacao import CURRENT_APP_VERSION, verificar_e_baixar_atualizacao_com_gui_selecao as vbags
    from services.admin import verificar_admin as veri_a
except ImportError as e:
    print(f"Erro ao importar um módulo: {e}. Verifique se todos os arquivos estão na estrutura de pastas correta.")
    sys.exit()

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
janela = tk.Tk()
janela.title(f"Autô-Mata V: {CURRENT_APP_VERSION}")
icone_path = os.path.join(os.path.dirname(__file__), "image", "icone.ico")
if os.path.exists(icone_path):
    janela.iconbitmap(icone_path)
janela.geometry("800x600")
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
    "limpeza_arquivos": "Limpar Recent, Temp e Prefetch",
    "mrt": "Ferramenta de Remoção de Software Mal-Intencionado (MRT)"
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
caixa_texto = Text(height=5, width=40)

# Redireciona a saída do console para a caixa de texto
sys.stdout = Redirecionador(caixa_texto)
sys.stderr = sys.stdout

# =======================
# LAYOUT DA JANELA COM GRID
# =======================
# Configura a janela para que as colunas e a linha se expandam
janela.grid_columnconfigure(0, weight=1)
janela.grid_columnconfigure(1, weight=0)
janela.grid_rowconfigure(0, weight=1)

# Posiciona o painel de abas (notebook) na primeira coluna (coluna 0)
guias.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

# Posiciona a caixa de texto na segunda coluna (coluna 1)
caixa_texto.grid(row=0, column=1, sticky='nsew', padx=3, pady=5)

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
# Inicia atualização periódica da caixa de texto
act(ferramentas, caixa_texto, janela)
janela.mainloop()