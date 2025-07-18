import os
import subprocess
import ctypes
import sys
import queue
import threading
from Ferramentas.limpeza_windows import LimpezaArquivos

class Ferramentas:
    def __init__(self):
        # Inicializa a fila quando uma INSTÂNCIA é criada
        self.output_queue = queue.Queue()
        self.resultado = None

    # =======================
    # MÉTODO GENÉRICO DE COMANDO
    # =======================
    def comand_terminal(self, text, comand):
        try:
            self.output_queue.put(f"{text}\n")
            self.resultado = subprocess.Popen(
                comand,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            for line in self.resultado.stdout:
                self.output_queue.put(line)
            self.resultado.wait()
            self.output_queue.put("\n" + "-"*50 + "\n")
        except subprocess.CalledProcessError as e:
            error_msg = f"\nErro durante a execução (Código {e.returncode}):\n"
            error_msg += e.stderr if e.stderr else "Sem detalhes de erro.\n"
            self.output_queue.put(error_msg)
            self.output_queue.put("\n" + "-"*50 + "\n")
        except Exception as e:
            error_msg = f"\nErro inesperado: {str(e)}\n"
            self.output_queue.put(error_msg)
            self.output_queue.put("\n" + "-"*50 + "\n")

    # =======================
    # FERRAMENTAS DE SISTEMA
    # =======================
    def check_disk(self):
        threading.Thread(
            target=self.comand_terminal,
            args=("O disco será checado!\n Reinicie o computador!", "echo s | chkdsk /f /r"),
            daemon=True
        ).start()

    def dism(self):
        threading.Thread(
            target=self.comand_terminal,
            args=("O Dism foi executado!", "dism /online /cleanup-image /restorehealth"),
            daemon=True
        ).start()

    def scannow(self):
        threading.Thread(
            target=self.comand_terminal,
            args=("O Scannow foi executado!", "sfc /scannow"),
            daemon=True
        ).start()

    def windows_active(self):
        threading.Thread(
            target=self.comand_terminal,
            args=("A verificação da ativação do windows foi executada", "slmgr /xpr"),
            daemon=True
        ).start()

    def limpeza_dns(self):
        threading.Thread(
            target=self.comand_terminal,
            args=("O dns foi limpo!", "ipconfig /flushdns"),
            daemon=True
        ).start()

    def verificacao_de_memoria(self):
        threading.Thread(
            target=self.comand_terminal,
            args=("A verificação de memória foi executada", "mdsched.exe"),
            daemon=True
        ).start()

    def limpeza_de_disco(self):
        threading.Thread(
            target=self.comand_terminal,
            args=("O disco será limpo!", "cleanmgr /d C:"),
            daemon=True
        ).start()

    def services(self):
        threading.Thread(
            target=self.comand_terminal,
            args=("O programa services.msc foi aberto!", "services.msc"),
            daemon=True
        ).start()

    def msconfig(self):
        threading.Thread(
            target=self.comand_terminal,
            args=("O programa msconfig foi aberto!", "msconfig"),
            daemon=True
        ).start()

    def trim(self):
        threading.Thread(
            target=self.comand_terminal,
            args=("Verificação da ativação do trim SSD", "Fsutil behavior query DisableDeleteNotify"),
            daemon=True
        ).start()
        threading.Thread(
            target=self.comand_terminal,
            args=("Configuração do trim SSD", "Fsutil behavior set DisableDeleteNotify 0"),
            daemon=True
        ).start()

    # =======================
    # FERRAMENTA DE LIMPEZA DE NAVEGADORES
    # =======================
    def limpeza_navegadores(self):
        def verificar_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        if not verificar_admin():
            script = sys.argv[0]
            parametros = " ".join(f'"{arg}"' for arg in sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {parametros}', None, 1)
            sys.exit()

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
        self.limpar = LimpezaArquivos()
        self.limpar.limpar_recent_temp_prefetch()
        
        print("Limpeza de arquivos concluída!")