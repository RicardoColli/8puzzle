from collections import deque

# Estado final desejado
OBJETIVO = (1,2,3,
            4,5,6,
            7,8,0)

# movimentos possíveis do espaço vazio
MOVIMENTOS = {
    "Cima": -3,
    "Baixo": 3,
    "Esquerda": -1,
    "Direita": 1
}

def movimentos_validos(pos):
    validos = []

    linha = pos // 3
    coluna = pos % 3

    if linha > 0:
        validos.append("Cima")
    if linha < 2:
        validos.append("Baixo")
    if coluna > 0:
        validos.append("Esquerda")
    if coluna < 2:
        validos.append("Direita")

    return validos


def aplicar_movimento(estado, movimento):
    pos = estado.index(0)
    nova_pos = pos + MOVIMENTOS[movimento]

    lista = list(estado)

    lista[pos], lista[nova_pos] = lista[nova_pos], lista[pos]

    return tuple(lista)


def bfs(estado_inicial):

    fila = deque()
    fila.append((estado_inicial, []))

    visitados = set()
    visitados.add(estado_inicial)

    estados_testados = 0

    while fila:

        estado, caminho = fila.popleft()

        estados_testados += 1

        if estado == OBJETIVO:
            return caminho, estados_testados

        pos = estado.index(0)

        for mov in movimentos_validos(pos):

            novo_estado = aplicar_movimento(estado, mov)

            if novo_estado not in visitados:

                visitados.add(novo_estado)

                fila.append((novo_estado, caminho + [mov]))

    return None, estados_testados


def imprimir_tabuleiro(estado):

    for i in range(0,9,3):
        print(estado[i], estado[i+1], estado[i+2])
    print()


def main():

    entrada = input("Digite o estado inicial (ex: 1 2 3 4 5 6 7 0 8): ")

    numeros = list(map(int, entrada.split()))

    estado_inicial = tuple(numeros)

    print("\nEstado inicial:")
    imprimir_tabuleiro(estado_inicial)

    caminho, estados_testados = bfs(estado_inicial)

    if caminho is None:
        print("Não foi encontrada solução.")
        return

    print("Movimentos para resolver:")

    for i, mov in enumerate(caminho,1):
        print(f"{i}. {mov}")

    print("\nNúmero de movimentos:", len(caminho))
    print("Número de estados testados:", estados_testados)


if __name__ == "__main__":
    main()