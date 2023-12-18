from pysat.solvers import Glucose4

# Entrada
desafioSudoku = [[5,3,0],[0,7,0],[0,0,0],
                 [6,0,0],[1,9,5],[0,0,0],
                 [0,9,8],[0,0,0],[0,6,0],

                 [8,0,0],[0,6,0],[0,0,3],
                 [4,0,0],[8,0,3],[0,0,1],
                 [7,0,0],[0,2,0],[0,0,6],
                 
                 [0,6,0],[0,0,0],[2,8,0],
                 [0,0,0],[4,1,9],[0,0,5],
                 [0,0,0],[0,8,0],[0,7,9]]

# Recebe como entrada uma lista e um número 'n'.
# Serão criadas 'n' novas listas apartir desta lista, dividindo os elementos da lista da entrada.
def spliter(n, lista):
    novaLista = []
    tamanhoDaLista = len(lista)
    for i in range(n):
        inicio = int(i * tamanhoDaLista / n)
        fim = int((i + 1)* tamanhoDaLista / n)
        novaLista.append(lista[inicio : fim])
    return(novaLista)

# Recebe como entrada uma lista contendo apenas as proposições verdadeiras(na forma de inteiro).
# A função faz com que seja realizada uma troca entre cada linha do sudoku e cada linha de um determinado quadrante.
# Isso envolverá todas as linhas e quadrantes do sudoku.
def trocarLinhaSporLinhaQ(novasProposicoesVerdadeiras):
    corte = spliter(27, novasProposicoesVerdadeiras)

    solucaoSudoku = []
    a = 0
    b = 9
    for i in range(3):
      for j in range(a,b,3):
        solucaoSudoku.append(corte[j])
      for k in range(a+1,b+1,3):
        solucaoSudoku.append(corte[k])
      for l in range(a+2,b+2,3):
        solucaoSudoku.append(corte[l])
      a += 9
      b += 9

    return solucaoSudoku

# Recebe uma lista L e retorna uma lista de todos os elementos aninhados em L.
def achatar(L):
    finalL = L
    AindaTemLista = True
    while AindaTemLista:
        novaL = []
        for i in finalL:
            if type(i) is list:
                for item in i:
                    novaL.append(item)
            else:
                novaL.append(i)
        finalL = novaL
        AindaTemLista = False
        for item in finalL:
            if type(item) is list:
                AindaTemLista = True
    return finalL

# Achatando entrada do sudoku (mantendo apenas uma lista de inteiros).
entradaDoSudoku = achatar(desafioSudoku)

# Criando todas as posições possíveis do sudoku.
posicoesNoSudoku = []
for quadrante_i in [1,2,3]:
  for linhaDoQua_i in [1,2,3]:
    for quadrante_j in [1,2,3]:
      for colunaDoQua_j in [1,2,3]:
        posicoesNoSudoku.append(f"{linhaDoQua_i}_{colunaDoQua_j}_{quadrante_i}_{quadrante_j}")

# Adicionando elementos e suas devidas posições já preenchidas no sudoku.
elementosJaPreenchidos = []
for i in range(0,81):
  if entradaDoSudoku[i] > 0:
    elementosJaPreenchidos.append(f"{entradaDoSudoku[i]}_{posicoesNoSudoku[i]}")

# Criando os símbolos proposicionais.
mapeandoParaInteiro = {}
mapeandoDoInteiro = {}
aux = 1
for quadrante_i in [1, 2, 3]:
    for quadrante_j in [1, 2, 3]:
        for linhaDoQua_i in [1, 2, 3]:
            for colunaDoQua_j in [1, 2, 3]:
                for elemento in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    proposicao = f"{elemento}_{linhaDoQua_i}_{colunaDoQua_j}_{quadrante_i}_{quadrante_j}"
                    mapeandoParaInteiro[proposicao] = aux
                    mapeandoDoInteiro[aux] = proposicao
                    aux += 1

# Lista que terá as cláusulas.
formula = []

# Inserindo clausulas dos elementos que já estão na entrada do sudoku.
for mapeamento in elementosJaPreenchidos:
  literal = mapeandoParaInteiro[mapeamento]
  formula.append([literal, literal])

# Garantir que cada quadradinho do sudoku tenha no máximo um número de 1 a 9.
for quadrante_i in [1, 2, 3]:
    for quadrante_j in [1, 2, 3]:
        for linhaDoQua_i in [1, 2, 3]:
            for colunaDoQua_j in [1, 2, 3]:
                for elemento in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    for elementoDiferente in list(range(elemento+1, 10)):
                        literal1 = mapeandoParaInteiro[f"{elemento}_{linhaDoQua_i}_{colunaDoQua_j}_{quadrante_i}_{quadrante_j}"]
                        literal2 = mapeandoParaInteiro[f"{elementoDiferente}_{linhaDoQua_i}_{colunaDoQua_j}_{quadrante_i}_{quadrante_j}"]
                        formula.append([-literal1, -literal2])

# Garantir que cada quadradinho do sudoku tenha pelo menos um número de 1 a 9.
for quadrante_i in [1, 2, 3]:
    for quadrante_j in [1, 2, 3]:
        for linhaDoQua_i in [1, 2, 3]:
            for colunaDoQua_j in [1, 2, 3]:
                clausula = []
                for elemento in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    proposicao = mapeandoParaInteiro[f"{elemento}_{linhaDoQua_i}_{colunaDoQua_j}_{quadrante_i}_{quadrante_j}"]
                    clausula.append(proposicao)
                formula.append(clausula)

# Garantir que não haverão elementos repetidos em cada quadrante do sudoku.
for quadrante_i in [1, 2, 3]:
    for quadrante_j in [1, 2, 3]:
        for linhaDoQua_i in [1, 2, 3]:
            for colunaDoQua_j in [1, 2, 3]:
                for linhaDoQua_i_Aux in [1, 2, 3]:
                    for colunaDoQua_j_Aux in [1, 2, 3]:
                        for elemento in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            if linhaDoQua_i != linhaDoQua_i_Aux or colunaDoQua_j != colunaDoQua_j_Aux:
                                literal1 = mapeandoParaInteiro[f"{elemento}_{linhaDoQua_i}_{colunaDoQua_j}_{quadrante_i}_{quadrante_j}"]
                                literal2 = mapeandoParaInteiro[f"{elemento}_{linhaDoQua_i_Aux}_{colunaDoQua_j_Aux}_{quadrante_i}_{quadrante_j}"]
                                formula.append([-literal1, -literal2])

# # Garantir que não haverão elementos repetidos em cada linha do sudoku. SOLUÇÃO DAVI.
# # -10, -19, -82, -91, -100, -163, -172, -181
# for quadrante_i in [1, 2, 3]:
#     for quadrante_j in [1, 2, 3]:
#         for linhaDoQua_i in [1, 2, 3]:
#             for colunaDoQua_j in [1, 2, 3]:
#                 for quadrante_j_Aux in [1, 2, 3]:
#                     for colunaDoQua_j_Aux in [1, 2, 3]:
#                         for elemento in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
#                             # Se for um quadrante DIFERENTE e que está na mesma linha do quadrante em questão,
#                             # e a coluna do quadrante em questão for IGUAL a coluna dos outros quadrantes que estão na mesma linha.
#                             possibilidade1 = quadrante_j != quadrante_j_Aux and colunaDoQua_j == colunaDoQua_j_Aux
#                             # Se for um quadrante DIFERENTE e que está na mesma linha do quadrante em questão,
#                             # e a coluna do quadrante em questão for DIFERENTE da coluna dos outros quadrantes que estão na mesma linha.
#                             possibilidade2 = quadrante_j != quadrante_j_Aux and colunaDoQua_j != colunaDoQua_j_Aux
#                             # Se for O MESMO quadrante e se está na mesma linha do quadrante em questão,
#                             # e a coluna do quadrante em questão for DIFERENTE das outras colunas deste mesmo quadrante.
#                             possibilidade3 = quadrante_j == quadrante_j_Aux and colunaDoQua_j != colunaDoQua_j_Aux
#                             if possibilidade1 or possibilidade2 or possibilidade3:
#                                 literal1 = mapeandoParaInteiro[f"{elemento}_{linhaDoQua_i}_{colunaDoQua_j}_{quadrante_i}_{quadrante_j}"]
#                                 literal2 = mapeandoParaInteiro[f"{elemento}_{linhaDoQua_i}_{colunaDoQua_j_Aux}_{quadrante_i}_{quadrante_j_Aux}"]
#                                 if literal1 != literal2:
#                                     formula.append([-literal1, -literal2])

# # Garantir que não haverão elementos repetidos em cada coluna do sudoku. SOLUÇÃO DAVI.
# # -28, -55, -244, 271, -298, -487, -514, -541
# for quadrante_i in [1, 2, 3]:
#     for quadrante_i_Aux in [1, 2, 3]:
#         for quadrante_j in [1, 2, 3]:
#             for linhaDoQua_i in [1, 2, 3]:
#                 for linhaDoQua_i_Aux in [1, 2, 3]:
#                     for colunaDoQua_j in [1, 2, 3]:
#                         for elemento in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
#                             # Se for um quadrante DIFERENTE e que está na mesma coluna do quadrante em questão,
#                             # e a linha do quadrante em questão for IGUAL a linha dos outros quadrantes que estão na mesma coluna.
#                             possibilidade1 = quadrante_i != quadrante_i_Aux and linhaDoQua_i == linhaDoQua_i_Aux
#                             # Se for um quadrante DIFERENTE e que está na mesma coluna do quadrante em questão,
#                             # e a linha do quadrante em questão for DIFERENTE da linha dos outros quadrantes que estão na mesma coluna.
#                             possibilidade2 = quadrante_i != quadrante_i_Aux and linhaDoQua_i != linhaDoQua_i_Aux
#                             # Se for O MESMO quadrante e se está na mesma coluna do quadrante em questão,
#                             # e a linha do quadrante em questão for DIFERENTE das outras linhas deste mesmo quadrante.
#                             possibilidade3 = quadrante_i == quadrante_i_Aux and linhaDoQua_i != linhaDoQua_i_Aux
#                             if possibilidade1 or possibilidade2 or possibilidade3:
#                                 literal1 = mapeandoParaInteiro[
#                                     f"{elemento}_{linhaDoQua_i}_{colunaDoQua_j}_{quadrante_i}_{quadrante_j}"]
#                                 literal2 = mapeandoParaInteiro[
#                                     f"{elemento}_{linhaDoQua_i_Aux}_{colunaDoQua_j}_{quadrante_i_Aux}_{quadrante_j}"]
#                                 formula.append([-literal2, -literal1])

# Garantir que não haverão elementos repetidos em cada linha do sudoku. SOLUÇÃO BRUNO.
for quadrant_i in [1, 2, 3]:
    for quadrante_j in [1, 2, 3]:
        for linhaDoQua_i in [1, 2, 3]:
            for colunaDoQua_j in [1, 2, 3]:
              for elemento in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                for colunaDoQua_j_1 in [1, 2, 3]:
                    for colunaDoQua_j_2 in [1, 2, 3]:
                      literal1 = mapeandoParaInteiro[f"{elemento}_{linhaDoQua_i}_{colunaDoQua_j}_{quadrant_i}_{quadrante_j}"]
                      literal2 = mapeandoParaInteiro[f"{elemento}_{linhaDoQua_i}_{colunaDoQua_j_2}_{quadrant_i}_{colunaDoQua_j_1}"]
                      if literal1 != literal2:
                        formula.append([-literal1, -literal2])

# Garantir que não haverão elementos repetidos em cada coluna do sudoku. SOLUÇÃO BRUNO.
for quadrante_j in [1, 2, 3]:
    for quadrant_i in [1, 2, 3]:
        for colunaDoQua_j in [1, 2, 3]:
            for linhaDoQua_i in [1, 2, 3]:
              for elemento in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                for quadrant_i_1 in [1, 2, 3]:
                    for quadrant_i_2 in [1, 2, 3]:
                      literal1 = mapeandoParaInteiro[f"{elemento}_{linhaDoQua_i}_{colunaDoQua_j}_{quadrant_i}_{quadrante_j}"]
                      literal2 = mapeandoParaInteiro[f"{elemento}_{quadrant_i_2}_{colunaDoQua_j}_{quadrant_i_1}_{quadrante_j}"]
                      if literal1 != literal2:
                        formula.append([-literal1, -literal2])

# Adiciona cláusulas da fórmula.
formulaSolver = Glucose4()
for clausula in formula:
    formulaSolver.add_clause(clausula)

# Verifica se existe solução.
if formulaSolver.solve():
    print("O Sudoku tem solucao :). Segue ela abaixo.\n")

    # Pega apenas as proposições que são verdadeiras (positivas).
    proposicoesVerdadeiras = []
    for x in formulaSolver.get_model():
        if x > 0:
            proposicoesVerdadeiras.append(x)
            
    # Pega apenas os elementos das proposições verdadeiras.
    novasProposicoesVerdadeiras = []
    for x in proposicoesVerdadeiras:
        novasProposicoesVerdadeiras.append(mapeandoDoInteiro[x][0])

    # Prepara o sudoku para ser impresso.
    solucaoSudoku = trocarLinhaSporLinhaQ(novasProposicoesVerdadeiras)
    solucaoSudoku = achatar(solucaoSudoku)

    # Imprime o sudoku <3.
    i = 0
    for x in solucaoSudoku:
        if i % 3 == 0:
            print(f'| ', end='')

        if f"{solucaoSudoku[i]}_{posicoesNoSudoku[i]}" in elementosJaPreenchidos:
            print(f'\033[34m{x}\033[0m ', end='')
        else:
            print(f'\033[32m{x}\033[0m ', end='')

        i += 1
        if i % 9 == 0:
            print(f'|', end='')
            print(f'', end='\n')
        if i % 27 == 0 and x != solucaoSudoku[-1]:
            print(' ------- ------- ------- ')
else:
  print("O Sudoku não tem solução :( Coloque uma entrada que seja possivel resolver X(")