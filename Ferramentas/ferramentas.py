import os

class Ferramentas:

    @classmethod
    def comand_terminal(self, text, comand):
        print(text)
        os.system(comand)
        print("\n")
        #os.system("cls")

    def check_disk(self):
        self.comand_terminal("O disco será checado!", "chkdsk /f /r")

    def dism(self):
        self.comand_terminal("O restorehealth será executado!", "dism /online /cleanup-image /restorehealth")

    def scannow(self):
        self.comand_terminal("O sfc /scannow será executado!", "sfc /scannow")

    def limpeza_navegadores(self):
        print("Limpeza de navegadores não pode ser iniciada, o recurso não está disponivel!")

    def windows_active(self):
        self.comand_terminal("A verificação da ativação do windows será executada!", "slmgr /xpr")

    def limpeza_dns(self):
        self.comand_terminal("O dns será limpo!", "ipconfig /flushdns")
