import tkinter as tk

MOVIMENTOS = {
    "Cima": -3,
    "Baixo": 3,
    "Esquerda": -1,
    "Direita": 1
}

def mostrar_interface(estado_inicial, caminho):

    janela = tk.Tk()
    janela.title("8 Puzzle - Solução")

    estado_atual = list(estado_inicial)
    passo = [0]

    labels = []

    # criar grade 3x3
    for i in range(3):
        linha = []
        for j in range(3):
            lbl = tk.Label(
                janela,
                text="",
                font=("Arial", 24),
                width=4,
                height=2,
                borderwidth=2,
                relief="solid"
            )
            lbl.grid(row=i, column=j)
            linha.append(lbl)
        labels.append(linha)

    def atualizar_tabuleiro():
        for i in range(3):
            for j in range(3):
                valor = estado_atual[i*3 + j]
                labels[i][j].config(text=str(valor) if valor != 0 else "")

    def aplicar_movimento_interface(mov):
        pos = estado_atual.index(0)
        nova_pos = pos + MOVIMENTOS[mov]
        estado_atual[pos], estado_atual[nova_pos] = estado_atual[nova_pos], estado_atual[pos]

    def proximo_passo():
        if passo[0] < len(caminho):
            mov = caminho[passo[0]]
            aplicar_movimento_interface(mov)
            passo[0] += 1
            atualizar_tabuleiro()

    botao = tk.Button(janela, text="Próximo passo", command=proximo_passo)
    botao.grid(row=3, column=0, columnspan=3)

    atualizar_tabuleiro()

    janela.mainloop()