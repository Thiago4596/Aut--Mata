import os
import subprocess
import ctypes
import sys
import threading
from models.command import Command

class Ferramentas:
    def __init__(self):
        self.resultado = None

    # =======================
    # FERRAMENTAS DE SISTEMA
    # =======================
    def check_disk(self):
        check_disk = Command()
        check_disk.command_execute("O disco será checado!\n Reinicie o computador!", "echo s | chkdsk /f /r")

    def dism(self):
        dism = Command()
        dism.command_execute("O Dism foi executado!", "dism /online /cleanup-image /restorehealth")

    def scannow(self):
        scannow = Command()
        scannow.command_execute("O Scannow foi executado!", "sfc /scannow")

    def windows_active(self):
        windows_active = Command()
        windows_active.command_execute("A verificação da ativação do windows foi executada", "slmgr /xpr")

    def limpeza_dns(self):
        limpeza_dns = Command()
        limpeza_dns.command_execute("O dns foi limpo!", "ipconfig /flushdns")

    def verificacao_de_memoria(self):
        verificacao_de_memoria = Command()
        verificacao_de_memoria.command_execute("A verificação de memória foi executada", "mdsched.exe")

    def limpeza_de_disco(self):
        limpeza_de_disco = Command()
        limpeza_de_disco.command_execute("O disco será limpo!", "cleanmgr /d C:")

    def services(self):
        services = Command()
        services.command_execute("O programa services.msc foi aberto!", "services.msc")

    def msconfig(self):
        msconfig = Command()
        msconfig.command_execute("O programa msconfig foi aberto!", "msconfig")


    def trim(self):
        trim = Command()
        trim.command_execute("Verificação da ativação do trim SSD", "Fsutil behavior query DisableDeleteNotify")
        trim.command_execute("Configuração do trim SSD", "Fsutil behavior set DisableDeleteNotify 0")

    def mrt(self):
        mrt = Command()
        mrt.command_execute("A ferramenta de remoção de software mal-intencionado foi executada", "mrt.exe")
    

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
        from Ferramentas.limpeza_windows import LimpezaArquivos
        self.limpar = LimpezaArquivos()
        self.limpar.limpar_recent_temp_prefetch()
        
        print("Limpeza de arquivos concluída!")

