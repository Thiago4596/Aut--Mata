import subprocess
import threading
import sys

class Command:
    def __init__(self):
        self.resultado = None

    # =======================
    # MÉTODO GENÉRICO DE COMANDO
    # =======================
    def comand_terminal(self, text, comand):
        try:
            print(f"{text}\n")
            self.resultado = subprocess.Popen(
                comand,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            for line in self.resultado.stdout:
                print(line)
            self.resultado.wait()
            print("\n" + "-"*50 + "\n")
        except subprocess.CalledProcessError as e:
            error_msg = f"\nErro durante a execução (Código {e.returncode}):\n"
            error_msg += e.stderr if e.stderr else "Sem detalhes de erro.\n"
            print(error_msg)
            print("\n" + "-"*50 + "\n")
        except Exception as e:
            error_msg = f"\nErro inesperado: {str(e)}\n"
            print(error_msg)
            print("\n" + "-"*50 + "\n")

    def command_execute(self, mensage, command):
        threading.Thread(
            target=self.comand_terminal,
            args=(mensage, command),
            daemon=True
        ).start()


