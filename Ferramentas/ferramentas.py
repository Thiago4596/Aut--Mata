import os
import subprocess
import ctypes
import sys

class Ferramentas:
    @classmethod
    def comand_terminal(self, text, comand):
        print(text)
        os.system(comand)
        print("\n")
        #os.system("cls")

    def check_disk(self):
        self.comand_terminal("O disco será checado!\n Reinicie o computador!", "echo s | chkdsk /f /r")

    def dism(self):
        self.comand_terminal("O Dism foi executado!", "dism /online /cleanup-image /restorehealth")

    def scannow(self):
        self.comand_terminal("O Scannow foi executado", "sfc /scannow")

    def limpeza_navegadores(self):
        # Função para verificar se o script está sendo executado como administrador
        def verificar_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        # Se não for administrador, pedir permissão para executar como administrador
        if not verificar_admin():
            script = sys.argv[0]
            parametros = " ".join(f'"{arg}"' for arg in sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {parametros}', None, 1)
            sys.exit()

        # Caminho relativo para o arquivo .bat na pasta 'ferramentas'
        bat_file_path = os.path.join(os.path.dirname(__file__), "Limpeza_navegadores.bat")
        print("A limpeza dos navegadores foi executada com sucesso!")

        # Executa o arquivo .bat com privilégios de administrador
        subprocess.run(bat_file_path, shell=True)


    def windows_active(self):
        self.comand_terminal("A verificação da ativação do windows foi executada", "slmgr /xpr")

    def limpeza_dns(self):
        self.comand_terminal("O dns foi limpo!", "ipconfig /flushdns")

    def verificacao_de_memoria(self):
        self.comand_terminal("A verificação de memória foi executada", "mdsched.exe")

    def limpeza_de_disco(self):
        self.comand_terminal("O disco será limpo!", "cleanmgr /d C:")

    def services(self):
        self.comand_terminal("O programa services.msc foi aberto!", "services.msc")
    
    def msconfig(self):
        self.comand_terminal("O programa msconfig foi aberto!", "msconfig")

    def trim(self):
        self.comand_terminal("Verificação da ativação do trim SSD", "Fsutil behavior query DisableDeleteNotify")
        if self.comand_terminal("O trim foi executado!", "Fsutil behavior set DisableDeleteNotify") == 1:
            self.comand_terminal("O trim foi executado!", "Fsutil behavior set DisableDeleteNotify 0")