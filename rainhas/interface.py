import tkinter as tk
from tkinter import ttk
import time

from algoritmos import (
    subida_encosta,
    subida_encosta_reinicio,
    tempera_simulada,
    estado_aleatorio,
    conflitos
)

estado_atual = None


def desenhar_tabuleiro(tabuleiro):
    for i in range(8):
        for j in range(8):
            texto = "♛" if tabuleiro[j] == i else ""
            cor = "#EEEED2" if (i + j) % 2 == 0 else "#769656"
            labels[i][j].config(text=texto, bg=cor)


def gerar_estado():
    global estado_atual

    estado_atual = estado_aleatorio()
    desenhar_tabuleiro(estado_atual)

    resultado.set(f"Estado inicial\nConflitos: {conflitos(estado_atual)}")


def executar():
    global estado_atual

    if estado_atual is None:
        resultado.set("Gere um estado primeiro.")
        return

    estado_inicial = estado_atual.copy()
    algoritmo = combo_algoritmo.get()

    inicio = time.time()

    if algoritmo == "Subida de Encosta":
        solucao, estados, caminho = subida_encosta(estado_atual)
        texto_extra = ""

    elif algoritmo == "Subida com Reinício":
        solucao, reinicios, estados, caminho = subida_encosta_reinicio(estado_atual)
        texto_extra = f"Reinícios: {reinicios}"

    elif algoritmo == "Têmpera Simulada":
        solucao, estados, caminho = tempera_simulada(estado_atual)
        texto_extra = ""

    else:
        resultado.set("Algoritmo não implementado.")
        return

    tempo = time.time() - inicio

    movimentos = len(caminho) - 1

    desenhar_tabuleiro(solucao)

    resultado.set(f"""
Estado inicial: {estado_inicial}

Algoritmo: {algoritmo}
Conflitos finais: {conflitos(solucao)}

Estados testados: {estados}
Movimentos (total): {movimentos}
{texto_extra}

Tempo: {tempo:.4f}s
""")


# =========================
# INTERFACE
# =========================
janela = tk.Tk()
janela.title("Problema das 8 Rainhas")
janela.geometry("900x900")

titulo = tk.Label(janela, text="8 Rainhas", font=("Arial", 18, "bold"))
titulo.pack(pady=10)

combo_algoritmo = ttk.Combobox(janela, values=[
    "Subida de Encosta",
    "Subida com Reinício",
    "Têmpera Simulada"
])
combo_algoritmo.current(0)
combo_algoritmo.pack(pady=10)

frame_botoes = tk.Frame(janela)
frame_botoes.pack()

btn_gerar = tk.Button(frame_botoes, text="Gerar Estado Inicial", command=gerar_estado)
btn_gerar.grid(row=0, column=0, padx=5)

btn_resolver = tk.Button(frame_botoes, text="Resolver", command=executar)
btn_resolver.grid(row=0, column=1, padx=5)

frame_tabuleiro = tk.Frame(janela)
frame_tabuleiro.pack(pady=20)

labels = []

for i in range(8):
    linha = []
    for j in range(8):
        lbl = tk.Label(frame_tabuleiro, text="", width=4, height=2,
                       font=("Arial", 18, "bold"))
        lbl.grid(row=i, column=j)
        linha.append(lbl)
    labels.append(linha)

resultado = tk.StringVar()
label_resultado = tk.Label(janela, textvariable=resultado, justify="left")
label_resultado.pack(pady=10)

janela.mainloop()