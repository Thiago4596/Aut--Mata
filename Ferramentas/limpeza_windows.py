import os
import shutil

class LimpezaArquivos:

    def recent(self):
        """
        Limpa a pasta 'Recent' do usuário atual no Windows.
        """
        caminho_recent = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Recent")
        self._limpar_pasta(caminho_recent, "Recent")

    def temp(self):
        """
        Limpa a pasta 'Temp' global do Windows e a pasta '%TEMP%' do usuário atual.
        """
        temp_user = os.environ.get("TEMP")  # %TEMP% do usuário atual
        temp_global = r"C:\Windows\Temp"  # Pasta Temp global do sistema
        
        self._limpar_pasta(temp_user, "%TEMP% (usuário)")
        self._limpar_pasta(temp_global, "Temp (global)")

    def prefetch(self):
        """
        Limpa a pasta 'Prefetch' do Windows.
        """
        caminho_prefetch = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Prefetch")
        self._limpar_pasta(caminho_prefetch, "Prefetch")

    def _limpar_pasta(self, caminho, nome_pasta):
        """
        Método interno para limpar qualquer pasta.
        """
        if os.path.exists(caminho):
            for arquivo in os.listdir(caminho):
                caminho_arquivo = os.path.join(caminho, arquivo)
                try:
                    if os.path.isfile(caminho_arquivo) or os.path.islink(caminho_arquivo):
                        os.remove(caminho_arquivo)  # Remove arquivos e atalhos
                    elif os.path.isdir(caminho_arquivo):
                        shutil.rmtree(caminho_arquivo)  # Remove pastas e conteúdos
                    print(f"Deletado: {caminho_arquivo}")
                except Exception as e:
                    print(f"Erro ao deletar {caminho_arquivo}: {e}")
            print(f"✔️ A pasta {nome_pasta} foi limpa!")
        else:
            print(f"❌ A pasta {nome_pasta} não foi encontrada!")

    def limpar_recent_temp_prefetch(self):
        """
        Limpa as pastas Recent, Temp e Prefetch.
        """
        self.recent()
        self.temp()
        self.prefetch()
