import random
import math

N = 8

def estado_aleatorio():
    return [random.randint(0, N-1) for _ in range(N)]

def conflitos(tabuleiro):
    conflitos = 0
    for i in range(N):
        for j in range(i + 1, N):
            if tabuleiro[i] == tabuleiro[j]:
                conflitos += 1
            if abs(tabuleiro[i] - tabuleiro[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def gerar_vizinhos(tabuleiro):
    vizinhos = []
    for col in range(N):
        for linha in range(N):
            if linha != tabuleiro[col]:
                novo = tabuleiro.copy()
                novo[col] = linha
                vizinhos.append(novo)
    return vizinhos


# =========================
# SUBIDA DE ENCOSTA
# a subida de encosta é um algoritmo de busca local que sempre tenta melhorar a solução atual
# ele começa com um estado inicial e gera todos os vizinhos possíveis
# a cada passo, escolhe o vizinho com menor número de conflitos (melhor estado)
# se não existir um vizinho melhor, o algoritmo para (fica preso em um mínimo local)
# esse algoritmo é muito rápido e simples, porém não garante encontrar a solução ideal

def subida_encosta(estado):
    atual = estado.copy()
    estados_testados = 0
    caminho = [atual.copy()]

    while True:
        # gera todos os vizinhos do estado atual
        vizinhos = gerar_vizinhos(atual)

        # assume inicialmente que o melhor é o estado atual
        melhor = atual
        melhor_conflito = conflitos(atual)

        # percorre todos os vizinhos buscando o melhor
        for v in vizinhos:
            estados_testados += 1
            c = conflitos(v)

            # se encontrar um estado melhor, atualiza
            if c < melhor_conflito:
                melhor = v
                melhor_conflito = c

        # se encontrar um estado melhor, atualiza
        if melhor_conflito >= conflitos(atual):
            return atual, estados_testados, caminho

        # move para o melhor vizinho encontrado
        atual = melhor
        caminho.append(atual.copy())


# =========================
# SUBIDA COM REINÍCIO
# a subida de encosta com reinício é uma extensão da subida de encosta tradicional
# ela foi criada para resolver o problema dos mínimos locais
# quando a busca fica presa (não encontra solução melhor), o algoritmo reinicia com um novo estado aleatório
# esse processo é repetido várias vezes até encontrar uma solução com 0 conflitos ou atingir um limite de reinícios
# isso aumenta muito a chance de encontrar a solução, porém aumenta o custo computacional

def subida_encosta_reinicio(estado_inicial=None, max_reinicios=100):

    total_reinicios = 0
    total_estados = 0
    caminho_total = []

    # o algoritmo tenta várias vezes até atingir o limite de reinícios
    while total_reinicios < max_reinicios:

        # na primeira tentativa usa o estado inicial fornecido
        if total_reinicios == 0 and estado_inicial is not None:
            estado = estado_inicial.copy()
        else:
            # nas próximas tentativas gera um novo estado aleatório (reinício)
            estado = estado_aleatorio()

        # executa a subida de encosta a partir do estado escolhido
        resultado, estados, caminho = subida_encosta(estado)

        # acumula a quantidade total de estados testados
        total_estados += estados

        # acumula todos os caminhos percorridos (incluindo reinícios)
        # isso representa o esforço total do algoritmo
        caminho_total.extend(caminho)

        # se encontrou solução perfeita (0 conflitos), finaliza
        if conflitos(resultado) == 0:
            return resultado, total_reinicios, total_estados, caminho_total

        # caso contrário, incrementa o número de reinícios e tenta novamente
        total_reinicios += 1

    # se não encontrou solução dentro do limite, retorna o melhor resultado obtido
    return resultado, total_reinicios, total_estados, caminho_total

# =========================
# TÊMPERA SIMULADA (PASSO A PASSO)
# a têmpera simulada é um algoritmo de busca local probabilístico
# ela permite aceitar soluções piores no início para escapar de mínimos locais
# com o tempo, vai ficando mais "exigente", reduzindo essa aceitação

def tempera_simulada(estado_inicial=None, temperatura_inicial=1000, resfriamento=0.95, limite=10000):

    # define o estado inicial (ou gera um aleatório)
    atual = estado_inicial.copy() if estado_inicial else estado_aleatorio()

    # guarda o melhor estado encontrado até agora
    melhor = atual.copy()

    # armazena o caminho percorrido para análise
    caminho = [atual.copy()]

    # contador de estados testados
    estados_testados = 0

    # temperatura inicial -- controla a aleatoriedade
    T = temperatura_inicial


    # loop principal executa ate o limite
    for _ in range(limite):

        # incrementa o número de estados avaliados
        estados_testados += 1

        # se encontrou solução perfeita, encerra
        if conflitos(atual) == 0:
            return atual, estados_testados, caminho

        # escolhe uma coluna aleatória (rainha)
        col = random.randint(0, N-1)

        # escolhe uma nova linha aleatória
        linha = random.randint(0, N-1)

        # cria novo estado modificando apenas uma rainha
        novo = atual.copy()
        novo[col] = linha

        # calcula a diferença de conflitos entre estados
        delta = conflitos(novo) - conflitos(atual)

        #regra de decisao
        # se o novo estado for melhor, aceita sempre
        if delta < 0:
            atual = novo
            caminho.append(atual.copy())

        else:
            # se for pior, aceita com uma probabilidade
            # essa probabilidade diminui conforme a temperatura diminui
            prob = math.exp(-delta / T)

            # sorteia um valor aleatório entre 0 e 1
            if random.random() < prob:
                atual = novo
                caminho.append(atual.copy())

        # atualiza melhor solucao
        # guarda o melhor estado já encontrado
        if conflitos(atual) < conflitos(melhor):
            melhor = atual.copy()

        # diminui a temperatura gradualmente
        T *= resfriamento

        # se a temperatura ficar muito baixa, encerra
        if T < 0.001:
            break


    # retorna o melhor estado encontrado (caso não tenha solução perfeita)
    return melhor, estados_testados, caminho