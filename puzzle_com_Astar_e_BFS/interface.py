import tkinter as tk
from tkinter import messagebox
import time

from puzzle import bfs, aestrela, tem_solucao

# =========================
# VARIÁVEIS
# =========================
estado_atual = None
caminho_animacao = []
passo = 0

# =========================
# FUNÇÕES
# =========================

def atualizar_tabuleiro(estado):
    for i in range(9):
        valor = estado[i]
        texto = "" if valor == 0 else str(valor)
        botoes[i].config(text=texto)


def executar():
    global estado_atual, caminho_animacao, passo

    entrada = entry.get()

    try:
        numeros = list(map(int, entrada.split()))
    except:
        messagebox.showerror("Erro", "Digite apenas números.")
        return

    if len(numeros) != 9 or len(set(numeros)) != 9 or any(n < 0 or n > 8 for n in numeros):
        messagebox.showerror("Erro", "Digite 9 números únicos entre 0 e 8.")
        return

    estado_inicial = tuple(numeros)
    estado_atual = estado_inicial
    atualizar_tabuleiro(estado_atual)

    if not tem_solucao(estado_inicial):
        messagebox.showerror("Erro", "Esse puzzle não tem solução.")
        return

    # ================= BFS =================
    inicio = time.time()
    caminho_bfs, estados_bfs = bfs(estado_inicial)
    tempo_bfs = time.time() - inicio

    # ================= A* =================
    inicio = time.time()
    caminho_aestrela, estados_aestrela = aestrela(estado_inicial)
    tempo_aestrela = time.time() - inicio

    passo = 0

    if caminho_bfs is None:
        resultado.set("Sem solução.")
        return

    # animação usando A*
    caminho_animacao = caminho_aestrela

    texto = f"""
===== BFS =====
Movimentos: {len(caminho_bfs)}
Estados: {estados_bfs}
Tempo: {tempo_bfs:.4f}s

===== A* =====
Movimentos: {len(caminho_aestrela)}
Estados: {estados_aestrela}
Tempo: {tempo_aestrela:.4f}s
"""
    resultado.set(texto)


def proximo_passo():
    global estado_atual, caminho_animacao, passo

    if not caminho_animacao or passo >= len(caminho_animacao):
        return

    movimento = caminho_animacao[passo]
    estado_atual = aplicar_movimento(estado_atual, movimento)

    atualizar_tabuleiro(estado_atual)
    passo += 1


def aplicar_movimento(estado, movimento):
    MOVIMENTOS = {
        "Cima": -3,
        "Baixo": 3,
        "Esquerda": -1,
        "Direita": 1
    }

    pos = estado.index(0)
    nova_pos = pos + MOVIMENTOS[movimento]

    lista = list(estado)
    lista[pos], lista[nova_pos] = lista[nova_pos], lista[pos]

    return tuple(lista)


# =========================
# INTERFACE
# =========================

janela = tk.Tk()
janela.title("8 Puzzle Solver")
janela.geometry("380x550")

titulo = tk.Label(janela, text="8 Puzzle Solver", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

entry = tk.Entry(janela, width=25, justify="center")
entry.pack(pady=10)

btn_resolver = tk.Button(janela, text="Resolver", command=executar, bg="#4CAF50", fg="white")
btn_resolver.pack(pady=5)

# Tabuleiro
frame_tabuleiro = tk.Frame(janela)
frame_tabuleiro.pack(pady=20)

botoes = []
for i in range(9):
    btn = tk.Label(frame_tabuleiro, text="", width=4, height=2,
                   font=("Arial", 18), borderwidth=2, relief="solid")
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    botoes.append(btn)

btn_passo = tk.Button(janela, text="Próximo passo", command=proximo_passo, bg="#2196F3", fg="white")
btn_passo.pack(pady=10)

resultado = tk.StringVar()
label_resultado = tk.Label(janela, textvariable=resultado, justify="left")
label_resultado.pack(pady=10)

janela.mainloop()

#exemplo de sequencia sem solucao: 0 2 4 6 8 1 7 5 3
#exemplo de funcionamento: 1, 0, 3, 2, 4, 5, 6, 8, 7