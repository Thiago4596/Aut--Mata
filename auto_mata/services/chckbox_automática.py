# services/chckbox_automática.py
from tkinter import *
from tkinter import ttk
from services.func_interface import executar_selecionados

# =======================
# CHECKBOXES NA ABA AUTOMÁTICAS
# =======================
def checkbox_aba_automática(ferramentas_automatizadas, botoes, ferramentas):
    ferramentas_marcadas = {}
    frame_check = Frame(ferramentas_automatizadas)
    frame_check.pack(pady=10)

    for func, text in botoes.items():
        var = BooleanVar()
        chk = ttk.Checkbutton(frame_check, text=text, variable=var)
        chk.pack(anchor='w', padx=10, pady=2)
        ferramentas_marcadas[func] = var

    # Botão para executar selecionados
    btn_executar = ttk.Button(
        ferramentas_automatizadas,
        text="Executar Selecionados",
        command=lambda: executar_selecionados(ferramentas, ferramentas_marcadas)
    )
    btn_executar.pack(pady=10)