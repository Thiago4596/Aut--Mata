import os
import subprocess
import ctypes
import sys
import threading
from auto_mata.core.command import run_command

class Ferramentas:
    def __init__(self):
        self.resultado = None

    # =======================
    # FERRAMENTAS DE SISTEMA
    # =======================
    def check_disk(self):
        run_command("O disco será checado!\n Reinicie o computador!", "echo s | chkdsk /f /r")

    def dism(self):
        run_command("O Dism foi executado!", "dism /online /cleanup-image /restorehealth")

    def scannow(self):
        run_command("O Scannow foi executado!", "sfc /scannow")

    def windows_active(self):
        run_command("A verificação da ativação do windows foi executada", "slmgr /xpr")

    def limpeza_dns(self):
        run_command("O dns foi limpo!", "ipconfig /flushdns")

    def verificacao_de_memoria(self):
        run_command("A verificação de memória foi executada", "mdsched.exe")

    def limpeza_de_disco(self):
        run_command("O disco será limpo!", "cleanmgr /d C:")

    def services(self):
        run_command("O programa services.msc foi aberto!", "services.msc")

    def msconfig(self):
        run_command("O programa msconfig foi aberto!", "msconfig")

    def trim(self):
        run_command("Verificação da ativação do trim SSD", "Fsutil behavior query DisableDeleteNotify")
        run_command("Configuração do trim SSD", "Fsutil behavior set DisableDeleteNotify 0")

    def mrt(self):
        run_command("A ferramenta de remoção de software mal-intencionado foi executada", "mrt.exe")

    # =======================
    # FERRAMENTA DE LIMPEZA DE NAVEGADORES
    # =======================
    def limpeza_navegadores(self):
        bat_file_path = os.path.join(os.path.dirname(__file__), "Limpeza_navegadores.bat")
        subprocess.run(bat_file_path, shell=True)
        print("A limpeza dos navegadores foi concluída com sucesso!")

    # =======================
    # FERRAMENTA DE LIMPEZA DE ARQUIVOS
    # =======================
    def limpeza_arquivos(self):
        """
        Inicializa a ferramenta de limpeza de arquivos.
        """
        # A importação de LimpezaArquivos foi movida para dentro da função
        # para evitar dependência circular e garantir que a instância seja criada
        # apenas quando a função for chamada.
        from auto_mata.ferramentas.limpeza_windows import LimpezaArquivos
        self.limpar = LimpezaArquivos()
        self.limpar.limpar_recent_temp_prefetch()
        
        print("Limpeza de arquivos concluída!")
