import os
import shutil
import subprocess
import glob

class LimpezaNavegadores:

    @staticmethod
    def delete_files(path, pattern):
        """Deleta arquivos que correspondem ao padrão especificado."""
        if not os.path.exists(path):
            print(f"Caminho não encontrado: {path}")
            return

        for file_path in glob.glob(os.path.join(path, pattern)):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Arquivo deletado: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Pasta deletada: {file_path}")
            except Exception as e:
                print(f"Erro ao deletar {file_path}: {e}")

    def clear_recycle_bin(self):
        """Limpa a lixeira."""
        try:
            subprocess.run(
                ["PowerShell.exe", "-NoProfile", "-Command", "Clear-RecycleBin", "-Confirm:$false"],
                check=True,
            )
            print("Lixeira limpa com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao limpar a lixeira: {e}")

    def delete_temp_files(self, user_path):
        """Deleta arquivos temporários do usuário."""
        temp_path = os.path.join(user_path, "AppData", "Local", "Temp")
        if os.path.exists(temp_path):
            self.delete_files(temp_path, "*")
            # Remove pastas vazias
            for root, dirs, files in os.walk(temp_path, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        if not os.listdir(dir_path):  # Verifica se a pasta está vazia
                            os.rmdir(dir_path)
                            print(f"Pasta vazia removida: {dir_path}")
                    except OSError as e:
                        print(f"Erro ao remover pasta {dir_path}: {e}")

    def delete_windows_temp_files(self):
        """Deleta arquivos temporários do Windows."""
        windows_temp_path = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Temp")
        if os.path.exists(windows_temp_path):
            self.delete_files(windows_temp_path, "*")
            # Remove pastas vazias
            for root, dirs, files in os.walk(windows_temp_path, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        if not os.listdir(dir_path):  # Verifica se a pasta está vazia
                            os.rmdir(dir_path)
                            print(f"Pasta vazia removida: {dir_path}")
                    except OSError as e:
                        print(f"Erro ao remover pasta {dir_path}: {e}")

    def delete_log_files(self):
        """Deleta arquivos de log do Windows."""
        system_root = os.environ.get("SystemRoot", "C:\\Windows")
        log_paths = [
            os.path.join(system_root, "Logs", "cbs"),
            os.path.join(system_root, "Logs", "measuredboot"),
            os.path.join(system_root, "Logs", "MoSetup"),
            os.path.join(system_root, "Panther"),
            os.path.join(system_root, "Performance", "WinSAT"),
            os.path.join(system_root, "inf"),
            os.path.join(system_root, "SoftwareDistribution"),
            os.path.join(system_root, "Microsoft.NET"),
        ]
        for path in log_paths:
            self.delete_files(path, "*.log")

    def delete_onedrive_logs(self, user_path):
        """Deleta arquivos de log do OneDrive."""
        onedrive_path = os.path.join(user_path, "AppData", "Local", "Microsoft", "OneDrive")
        if os.path.exists(onedrive_path):
            self.delete_files(os.path.join(onedrive_path, "setup", "logs"), "*.log")
            self.delete_files(onedrive_path, "*.odl")
            self.delete_files(onedrive_path, "*.aodl")
            self.delete_files(onedrive_path, "*.otc")
            self.delete_files(os.path.join(user_path, "AppData", "Local", "OneDrive"), "*.qmlc")

    def delete_crash_dumps(self, user_path):
        """Deleta arquivos de dump de programas."""
        crash_dumps_path = os.path.join(user_path, "AppData", "Local", "CrashDumps")
        if os.path.exists(crash_dumps_path):
            self.delete_files(crash_dumps_path, "*.dmp")

    def delete_browser_cache(self, user_path, browser_name):
        """Deleta cache de navegadores."""
        browser_paths = {
            "Edge": os.path.join(user_path, "AppData", "Local", "Microsoft", "Edge", "User Data"),
            "Chrome": os.path.join(user_path, "AppData", "Local", "Google", "Chrome", "User Data"),
            "Brave": os.path.join(user_path, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data"),
            "Vivaldi": os.path.join(user_path, "AppData", "Local", "Vivaldi", "User Data"),
        }
        if browser_name in browser_paths:
            browser_path = browser_paths[browser_name]
            if os.path.exists(browser_path):
                self.delete_files(os.path.join(browser_path, "Default", "Cache", "Cache_Data"), "data*")
                self.delete_files(os.path.join(browser_path, "Default", "Cache", "Cache_Data"), "f*")
                self.delete_files(os.path.join(browser_path, "Default", "Cache", "Cache_Data"), "index")
                self.delete_files(os.path.join(browser_path, "Default", "GPUCache"), "d*")
                self.delete_files(os.path.join(browser_path, "Default", "GPUCache"), "i*")
                self.delete_files(os.path.join(browser_path, "Default", "Code Cache", "js"), "*")
                self.delete_files(os.path.join(browser_path, "Default", "Code Cache", "wasm"), "*")
                self.delete_files(os.path.join(browser_path, "Default", "Service Worker", "CacheStorage"), "*")
                self.delete_files(os.path.join(browser_path, "Default", "Service Worker", "Database"), "*")
                self.delete_files(os.path.join(browser_path, "Default", "Service Worker", "ScriptCache"), "*")

    def delete_spotify_cache(self, user_path):
        """Deleta cache do Spotify."""
        spotify_path = os.path.join(user_path, "AppData", "Local", "Spotify")
        if os.path.exists(spotify_path):
            self.delete_files(os.path.join(spotify_path, "Data"), "*.file")
            self.delete_files(os.path.join(spotify_path, "Browser", "Cache", "Cache_Data"), "f*")
            self.delete_files(os.path.join(spotify_path, "Browser", "GPUCache"), "*")

    def delete_adobe_cache(self, user_path):
        """Deleta cache do Adobe."""
        adobe_path = os.path.join(user_path, "AppData", "Roaming", "Adobe", "Common", "Media Cache Files")
        if os.path.exists(adobe_path):
            self.delete_files(adobe_path, "*")
        self.delete_files(os.path.join(user_path, "AppData", "Roaming", "Adobe"), "*.log")

    def delete_vmware_logs(self):
        """Deleta logs do VMware."""
        program_data = os.environ.get("ProgramData", "C:\\ProgramData")
        vmware_path = os.path.join(program_data, "VMware", "logs")
        if os.path.exists(vmware_path):
            self.delete_files(vmware_path, "*.log")

    def delete_teamviewer_cache(self, user_path):
        """Deleta cache do TeamViewer."""
        teamviewer_path = os.path.join(user_path, "AppData", "Local", "TeamViewer", "EdgeBrowserControl")
        if os.path.exists(teamviewer_path):
            self.delete_files(teamviewer_path, "data_*")
            self.delete_files(teamviewer_path, "f_*")
            self.delete_files(teamviewer_path, "index.*")

    def limpar_tudo(self):
        """Executa todas as operações de limpeza."""
        # Limpa a lixeira
        self.clear_recycle_bin()

        # Obtém a lista de usuários
        users_path = os.path.join("C:", "Users")
        if os.path.exists(users_path):
            for user in os.listdir(users_path):
                user_path = os.path.join(users_path, user)
                if os.path.isdir(user_path):
                    # Deleta arquivos temporários do usuário
                    self.delete_temp_files(user_path)
                    # Deleta logs do OneDrive
                    self.delete_onedrive_logs(user_path)
                    # Deleta crash dumps
                    self.delete_crash_dumps(user_path)
                    # Deleta cache de navegadores
                    self.delete_browser_cache(user_path, "Edge")
                    self.delete_browser_cache(user_path, "Chrome")
                    self.delete_browser_cache(user_path, "Brave")
                    self.delete_browser_cache(user_path, "Vivaldi")
                    # Deleta cache do Spotify
                    self.delete_spotify_cache(user_path)
                    # Deleta cache do Adobe
                    self.delete_adobe_cache(user_path)
                    # Deleta cache do TeamViewer
                    self.delete_teamviewer_cache(user_path)

        # Deleta arquivos temporários do Windows
        self.delete_windows_temp_files()

        # Deleta logs do Windows
        self.delete_log_files()

        # Deleta logs do VMware
        self.delete_vmware_logs()


# Exemplo de uso
if __name__ == "__main__":
    limpeza = LimpezaNavegadores()
    limpeza.limpar_tudo()