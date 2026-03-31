from collections import deque
import heapq


# ESTADO OBJETIVO
OBJETIVO = (1, 2, 3,
            4, 5, 6,
            7, 8, 0)


# MOVIMENTOS
MOVIMENTOS = {
    "Cima": -3,
    "Baixo": 3,
    "Esquerda": -1,
    "Direita": 1
}

def validar_entrada(numeros):

    if len(numeros) != 9:
        return False

    if any(n < 0 or n > 8 for n in numeros):
        return False

    if len(set(numeros)) != 9:
        return False

    return True


def contar_inversoes(estado):
    lista = [x for x in estado if x != 0]
    inversoes = 0

    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j]:
                inversoes += 1

    return inversoes


def tem_solucao(estado):
    return contar_inversoes(estado) % 2 == 0


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



def heuristica(estado):
    distancia = 0

    for i, valor in enumerate(estado):

        if valor == 0:
            continue

        objetivo_pos = OBJETIVO.index(valor)

        linha_atual, col_atual = i // 3, i % 3
        linha_obj, col_obj = objetivo_pos // 3, objetivo_pos % 3

        distancia += abs(linha_atual - linha_obj) + abs(col_atual - col_obj)

    return distancia


# =========================
# A*
# =========================
def aestrela(estado_inicial):

    fila = []
    heapq.heappush(fila, (0, estado_inicial, []))

    visitados = set()
    visitados.add(estado_inicial)

    estados_testados = 0

    while fila:

        custo, estado, caminho = heapq.heappop(fila)
        estados_testados += 1

        if estado == OBJETIVO:
            return caminho, estados_testados

        pos = estado.index(0)

        for mov in movimentos_validos(pos):

            novo_estado = aplicar_movimento(estado, mov)

            if novo_estado not in visitados:

                visitados.add(novo_estado)

                novo_caminho = caminho + [mov]

                g = len(novo_caminho)
                h = heuristica(novo_estado)
                f = g + h

                heapq.heappush(fila, (f, novo_estado, novo_caminho))

    return None, estados_testados