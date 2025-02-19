from Ferramentas.ferramentas import Ferramentas
import ctypes
import sys

ferramentas = Ferramentas()


def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def main():
    run_as_admin()
    print("Autô-Mata")
    print("v: 1.1")
    print("""
1. Verificacao do disco (CHKDSK)
2. Ferramenta de Resolucao de Problemas do Windows (DISM)
3. Ferramenta de Reparo do Componente do Sistema (SFC /SCANNOW)
4. Limpar dados dos Navegadores (Script Completo): (Não disponivel!)
5. Verificar ativação do Windows (SLMGR)
6. Limpeza de DNS (FlushDNS)
7. Sair
          """)
    opcoes = input("Qual ferramenta deseja utilizar? ")

    if opcoes == "1":
        ferramentas.check_disk()
        main()
    elif opcoes == "2":
        ferramentas.dism()
        main()
    elif opcoes == "3":
        ferramentas.scannow()
        main()
    elif opcoes == "4":
        ferramentas.limpeza_navegadores()
        main()
    elif opcoes == "5":
        ferramentas.windows_active()
        main()
    elif opcoes == "6":
        ferramentas.limpeza_dns()
        main()
    elif opcoes == "7":
        sys.exit()
    else:
        print("Opcao inválida!")

if __name__ == "__main__":
    main()
