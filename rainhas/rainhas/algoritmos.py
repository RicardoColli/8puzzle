# =========================
# IMPORTAÇÕES
# =========================
import random
import math

N = 8


# =========================
# GERAR ESTADO ALEATÓRIO
# =========================
def estado_aleatorio():
    return [random.randint(0, N-1) for _ in range(N)]


# =========================
# FUNÇÃO DE CONFLITOS
# =========================
def conflitos(tabuleiro):
    conflitos = 0

    for i in range(N):
        for j in range(i + 1, N):

            # mesma linha
            if tabuleiro[i] == tabuleiro[j]:
                conflitos += 1

            # diagonal
            if abs(tabuleiro[i] - tabuleiro[j]) == abs(i - j):
                conflitos += 1

    return conflitos


# =========================
# GERAR VIZINHOS
# =========================
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
# =========================
# a subida de encosta sempre tenta melhorar o estado atual
# ela gera todos os vizinhos possíveis e escolhe o que possui menos conflitos
# caso nenhum vizinho seja melhor, o algoritmo para em um mínimo local
def subida_encosta(estado):

    atual = estado.copy()

    estados_testados = 0

    caminho = [atual.copy()]

    while True:

        vizinhos = gerar_vizinhos(atual)

        melhor = atual
        melhor_conflito = conflitos(atual)

        for v in vizinhos:

            estados_testados += 1

            c = conflitos(v)

            if c < melhor_conflito:

                melhor = v
                melhor_conflito = c

        # se não encontrou melhora, para
        if melhor_conflito >= conflitos(atual):
            return atual, estados_testados, caminho

        atual = melhor

        caminho.append(atual.copy())


# =========================
# SUBIDA COM REINÍCIO
# =========================
# executa a subida de encosta várias vezes
# quando o algoritmo trava em mínimo local, reinicia com um novo estado aleatório
# isso aumenta muito a chance de encontrar solução perfeita
def subida_encosta_reinicio(estado_inicial=None, max_reinicios=100):

    total_reinicios = 0

    total_estados = 0

    caminho_total = []

    while total_reinicios < max_reinicios:

        if total_reinicios == 0 and estado_inicial is not None:
            estado = estado_inicial.copy()

        else:
            estado = estado_aleatorio()

        resultado, estados, caminho = subida_encosta(estado)

        total_estados += estados

        caminho_total.extend(caminho)

        if conflitos(resultado) == 0:
            return resultado, total_reinicios, total_estados, caminho_total

        total_reinicios += 1

    return resultado, total_reinicios, total_estados, caminho_total


# =========================
# TÊMPERA SIMULADA
# =========================
# a têmpera simulada permite aceitar estados piores no início
# isso ajuda o algoritmo a escapar de mínimos locais
# conforme a temperatura diminui, ele fica mais seletivo
def tempera_simulada(
        estado_inicial=None,
        temperatura_inicial=2000,
        resfriamento=0.98,
        limite=20000
):

    atual = estado_inicial.copy() if estado_inicial else estado_aleatorio()

    melhor = atual.copy()

    caminho = [atual.copy()]

    estados_testados = 0

    T = temperatura_inicial

    for _ in range(limite):

        estados_testados += 1

        if conflitos(atual) == 0:
            return atual, estados_testados, caminho

        # escolhe uma rainha aleatória
        col = random.randint(0, N-1)

        # escolhe nova linha aleatória
        linha = random.randint(0, N-1)

        novo = atual.copy()
        novo[col] = linha

        delta = conflitos(novo) - conflitos(atual)

        # se melhorou, aceita sempre
        if delta < 0:

            atual = novo

            caminho.append(atual.copy())

        else:

            # aceita solução pior com probabilidade
            prob = math.exp(-delta / T)

            if random.random() < prob:

                atual = novo

                caminho.append(atual.copy())

        # guarda melhor solução encontrada
        if conflitos(atual) < conflitos(melhor):
            melhor = atual.copy()

        # reduz temperatura
        T *= resfriamento

        # encerra se temperatura muito baixa
        if T < 0.001:
            break

    return melhor, estados_testados, caminho


# =========================
# ALGORITMO GENÉTICO
# =========================
# o algoritmo genético trabalha com uma população de soluções
# a cada geração, os melhores indivíduos possuem maior chance de reprodução
# novos indivíduos são criados através de crossover e mutação
# isso permite explorar várias soluções ao mesmo tempo
def algoritmo_genetico(
        tamanho_populacao=100,
        geracoes=1000,
        taxa_mutacao=0.1
):

    # =========================
    # POPULAÇÃO INICIAL
    # =========================
    populacao = [estado_aleatorio() for _ in range(tamanho_populacao)]

    estados_testados = 0

    caminho = []

    # =========================
    # FITNESS
    # =========================
    # quanto menos conflitos, melhor o indivíduo
    def fitness(individuo):

        return 28 - conflitos(individuo)

    # =========================
    # SELEÇÃO
    # =========================
    # escolhe os melhores indivíduos
    def selecionar(pop):

        pop_ordenada = sorted(
            pop,
            key=lambda x: conflitos(x)
        )

        return pop_ordenada[:tamanho_populacao // 2]

    # =========================
    # CROSSOVER
    # =========================
    # mistura genes de dois pais
    def crossover(pai1, pai2):

        ponto = random.randint(1, N - 2)

        filho = pai1[:ponto] + pai2[ponto:]

        return filho

    # =========================
    # MUTAÇÃO
    # =========================
    # altera aleatoriamente uma rainha
    def mutacao(individuo):

        if random.random() < taxa_mutacao:

            col = random.randint(0, N-1)

            individuo[col] = random.randint(0, N-1)

        return individuo

    # =========================
    # LOOP PRINCIPAL
    # =========================
    for _ in range(geracoes):

        estados_testados += len(populacao)

        # ordena população pelo melhor indivíduo
        populacao = sorted(populacao, key=lambda x: conflitos(x))

        melhor = populacao[0]

        caminho.append(melhor.copy())

        # solução encontrada
        if conflitos(melhor) == 0:

            return melhor, estados_testados, caminho

        # seleciona melhores indivíduos
        selecionados = selecionar(populacao)

        nova_populacao = []

        # gera nova geração
        while len(nova_populacao) < tamanho_populacao:

            pai1 = random.choice(selecionados)
            pai2 = random.choice(selecionados)

            filho = crossover(pai1, pai2)

            filho = mutacao(filho)

            nova_populacao.append(filho)

        populacao = nova_populacao

    # retorna melhor solução encontrada
    populacao = sorted(populacao, key=lambda x: conflitos(x))

    return populacao[0], estados_testados, caminho