import sys
import ctypes

# =======================
# FUNÇÕES DE SISTEMA
# =======================
def verificar_admin():
    """Verifica se o script está rodando como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Reinicia como administrador se necessário
if not verificar_admin():
    script = sys.argv[0]
    parametros = " ".join(f'"{arg}"' for arg in sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {parametros}', None, 1)
    sys.exit()