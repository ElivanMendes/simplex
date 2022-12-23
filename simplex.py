import numpy as np
import copy


# Função para Ler a Quantidade de Variaveis e Restrições. #
def ler_info(msg):
    while True:
        try:
            quant = int(input(msg))
            return quant
        except ValueError:
            print('\nInforme Somente Números.\n')
            continue


# Fução para Ler as Equações. #
def ler_equacoes(restr):
    lista_eq = []
    print('\nInforme as Equações na Forma Padrão como no Exemplo:')
    print('Somente Números e Sínais sem Espaços.\n')
    print('Eq 1: 5+20+1+0=400\nEq 2: 10+15+0+1=450\nF.O: -45-80-0-0\n')
    for i in range(restr):
        lista_eq.append(input(f'Eq {i+1}: '))
    lista_eq.append(input('F.O: '))
    return lista_eq


# Função para Converter as Equações para Float. #
def converter_valores(equacao):
    try:
        lista = equacao.split('=')
        temp = lista.pop()
        lista = lista[0].split('+')
        lista.append(temp)
        return [float(v) for v in lista]
    except Exception:
        print('\nErro na Inserção das Equacões na Forma Padrão.')


# Função para Converter a F.O para Float. #
def converter_valores_fo(fo):
    try:
        lista = fo.split('-')
        lista.pop(0)
        return [float(v) for v in lista]
    except Exception:
        print('\nErro na Inserção da F.O na Forma Padrão.')


# Função para Adicionar Valores na Matriz A. #
def matriz_a(lista_eq, lin):
    A = []
    for i in range(lin):
        A.append(converter_valores(lista_eq[i]))
    return A


# Função para Adicionar Valores na Matriz R. #
def matriz_r(mat_a, lin, col):
    R = []
    for i in range(lin):
        R.append(mat_a[i][:col])
    return R


# Função para Adicionar Valores na Matriz B. #
def matriz_b(mat_a, lin, col):
    B = []
    for i in range(lin):
        B.append(mat_a[i][col:-1])
    return B


# Função para Adicionar Valores na Matriz b. #
def matriz_bzin(mat_a, lin):
    b = []
    for i in range(lin):
        b.append([mat_a[i][-1]])
    return b


# Função para Adicionar Valores na Matriz cR. #
def matriz_cr(C, col):
    cr = C[:col]
    cr = [v * (-1) for v in cr]
    return cr


# Função para Adicionar Valores na Matriz cB. #
def matriz_cb(C, col):
    cb = C[col:]
    return cb


# Função que Verifica se a Solução é Ótima. #
def verificar_solucao_otima(matriz):
    return min(matriz)


# Função que Verifica quem sai da Base. #
def sair_da_base(i, R, b, lin):
    lista = []
    for j in range(lin):
        lista.append(b[j][0] / R[j][i])
    return lista.index(min(lista))


# Função que Atualiza as Matrizes R e B. #
def atualizar_matrizes_rb(R, B, i_e, i_s, lin):
    novo_R = copy.deepcopy(R)
    novo_B = copy.deepcopy(B)
    for i in range(lin):
        novo_R[i][i_e] = B[i][i_s]
        novo_B[i][i_s] = R[i][i_e]
    return novo_R, novo_B


# Função que Atualiza as Matrizes cR e cB. #
def atualizar_matrizes_crcb(cR, cB, i_e, i_s):
    novo_cR = copy.deepcopy(cR)
    novo_cB = copy.deepcopy(cB)
    novo_cR[i_e] = cB[i_s]
    novo_cB[i_s] = cR[i_e]
    return novo_cR, novo_cB


# Função que Calcula o Novo cR. #
def calcular_novo_cr(cR, cB, B, R, col):
    cR_t = np.matrix([v for v in cR])
    cB_t = np.matrix([v for v in cB])
    B_t = np.matrix([v for v in B])
    R_t = np.matrix([v for v in R])
    result = cR_t - cB_t * np.linalg.inv(B_t) * R_t
    lista = []
    for i in range(col):
        lista.append(result[0, i])
    return lista


# Função que Calcula o Novo bzin. #
def calcular_novo_bzin(B, b, lin):
    B_t = np.matrix([v for v in B])
    b_t = np.matrix([v for v in b])
    result = np.linalg.inv(B_t) * b_t
    lista = []
    for i in range(lin):
        lista.append([result[i, 0]])
    return lista


# Função que Calcular a F.O. #
def calcular_fo(cB, B, b):
    cB_t = np.matrix([v for v in cB])
    B_t = np.matrix([v for v in B])
    b_t = np.matrix([v for v in b])
    result = cB_t * np.linalg.inv(B_t) * b_t
    return result[0, 0] * -1


# Função que Calcula o Novo R. #
def calcular_novo_r(B, R, lin, col):
    B_t = np.matrix([v for v in B])
    R_t = np.matrix([v for v in R])
    result = np.linalg.inv(B_t) * R_t
    lista = []
    for i in range(lin):
        lista_t = []
        for j in range(col):
            lista_t.append(result[i, j])
        lista.append(lista_t)
    return lista


# Criar as Varias X do R. #
def criar_var_r(col):
    lista = []
    for i in range(col):
        lista.append('x' + str(i+1))
    return lista


# Criar as Variaveis X do B. #
def criar_var_b(lin, col):
    lista = []
    for i in range(lin):
        lista.append('x' + str(col + 1 + i))
    return lista


# Atualizar as Variaveis X do R e B. #
def atualizar_var_vr(var_R, var_B, i_e, i_s):
    novo_var_R = copy.deepcopy(var_R)
    novo_var_B = copy.deepcopy(var_B)
    novo_var_R[i_e] = var_B[i_s]
    novo_var_B[i_s] = var_R[i_e]
    return novo_var_R, novo_var_B


# Função para Imprimir Matriz R. #
def imprimir_matriz_r(R, var_R, lin):
    print('\nR:')
    print(var_R)
    for i in range(lin):
        print(R[i])


# Função para Imprimir Matriz B. #
def imprimir_matriz_b(B, var_B, lin):
    print('\nB:')
    print(var_B)
    for i in range(lin):
        print(B[i])


# Função para Imprimir Matriz bzin. #
def imprimir_matriz_bzin(bzin, var_bzin, lin):
    print('\nbzin:')
    for i in range(lin):
        print(var_bzin[i], bzin[i])


# Função para Imprimir Matriz bzin. #
def imprimir_matriz_cr(cR, var_cR):
    print('\ncR:')
    print(var_cR)
    print(cR)


# Função para Imprimir Matriz bzin. #
def imprimir_matriz_cb(cB, var_cB):
    print('\ncB:')
    print(var_cB)
    print(cB)


# Função para Imprimir Resultado. #
def imprimir_result(bzin, var_bzin, lin, col):
    lista = []
    for i in range(col):
        lista.append('x' + str(i + 1))
    lista2 = []
    for i in range(len(lista)):
        for j in range(len(var_bzin)):
            if lista[i] == var_bzin[j]:
                lista2.append(j)
    dic = {}
    for i in range(len(lista2)):
        dic.update({lista[i]: bzin[lista2[i]]})
    for i in range(lin, col):
        dic.update({lista[i]: [0.0]})
    print()
    for k, v in dic.items():
        print(f'{k}: {round(v[0])}')


def main():
    qt_var = ler_info('\nQuantas Variaveis de Decisão tem o Problema: ')  # Quantidade de Variaveis de Decisão.
    qt_restr = ler_info('Quantas Restrições tem o Problema: ')  # Quantidade de Restrições.
    lista_eq = ler_equacoes(qt_restr)

    # Definindo e Separandos Matrizes. #
    A = matriz_a(lista_eq, qt_restr)
    R = matriz_r(A, qt_restr, qt_var)
    B = matriz_b(A, qt_restr, qt_var)
    bzin = matriz_bzin(A, qt_restr)
    C = converter_valores_fo(lista_eq[-1])
    cR = matriz_cr(C, qt_var)
    cB = matriz_cb(C, qt_var)

    # Copias. #
    R_cpy = copy.deepcopy(R)
    B_cpy = copy.deepcopy(B)
    bzin_cpy = copy.deepcopy(bzin)
    cR_cpy = copy.deepcopy(cR)
    cB_cpy = copy.deepcopy(cB)

    # Criando Variaveis X. #
    var_R = criar_var_r(qt_var)
    var_B = criar_var_b(qt_restr, qt_var)
    var_bzin = criar_var_b(qt_restr, qt_var)
    var_cR = criar_var_r(qt_var)
    var_cB = criar_var_b(qt_restr, qt_var)

    # Imprimirndo Matrizes. #
    print('\n###################################################')
    imprimir_matriz_r(R, var_R, qt_restr)
    imprimir_matriz_b(B, var_B, qt_restr)
    imprimir_matriz_bzin(bzin, var_bzin, qt_restr)
    imprimir_matriz_cr(cR, var_cR)
    imprimir_matriz_cb(cB, var_cB)
    # Calculando a Função Objetiva. #
    FO = calcular_fo(cB, B, bzin)
    print('\nF.O:', FO * -1)
    print('\n###################################################')

    # Calculando o Valor do Novo cR. #
    cR = calcular_novo_cr(cR, cB, B, R, qt_var)
    # Imprimindo Matriz cR. #
    imprimir_matriz_cr(cR, var_cR)

    while True:
        # Verificando Solução Ótima. #
        valor = verificar_solucao_otima(cR)
        if valor >= 0:
            print('\n------------------ SOLUÇÃO ÓTIMA ------------------')
            print('###################################################')
            # Calculando o Valor da F.O. #
            FO = calcular_fo(cB, B, bzin)
            print(f'\nSolução Ótima: {round(FO)}')
            # Calculando o Valor do Novo bzin. #
            bzin = calcular_novo_bzin(B, bzin, qt_restr)
            # Imprimindo Resultado Final. #
            imprimir_result(bzin, var_bzin, qt_restr, qt_var)
            print('\n###################################################')
            return

        # Encontrando Indice do Menor Valor. #
        i_entra_base = cR.index(valor)
        # Encontrando Indice de Quem sai da Base. #
        i_sair_base = sair_da_base(i_entra_base, R, bzin, qt_restr)

        # Atualizando Matrizes R e B, trocando quem Entra e quem sai da Base. #
        novo_R_B_cpy = atualizar_matrizes_rb(R_cpy, B_cpy, i_entra_base, i_sair_base, qt_restr)
        R_cpy = novo_R_B_cpy[0]
        B_cpy = novo_R_B_cpy[1]

        # Atualizando Variaveis R e B. Mudando quen Entra e Quem sai da Base. #
        novo_var_R_B = atualizar_var_vr(var_R, var_B, i_entra_base, i_sair_base)
        var_R = novo_var_R_B[0]
        var_B = novo_var_R_B[1]
        # Atualizando Variavel bzin. #
        var_bzin = novo_var_R_B[1]

        # Atualizando Matrizes cR e cB, Trocando quem Entra e quem sai da Base. #
        novo_cR_cR_cpy = atualizar_matrizes_crcb(cR_cpy, cB_cpy, i_entra_base, i_sair_base)
        cR_cpy = novo_cR_cR_cpy[0]
        cB_cpy = novo_cR_cR_cpy[1]

        # Atualizando Variavel cR e cB. #
        var_cR = novo_var_R_B[0]
        var_cB = novo_var_R_B[1]

        # Copias. #
        R = copy.deepcopy(R_cpy)
        B = copy.deepcopy(B_cpy)
        bzin = copy.deepcopy(bzin_cpy)
        cR = copy.deepcopy(cR_cpy)
        cB = copy.deepcopy(cB_cpy)

        # Imprimirndo Matrizes. #
        print('\n###################################################')
        imprimir_matriz_r(R, var_R, qt_restr)
        imprimir_matriz_b(B, var_B, qt_restr)
        imprimir_matriz_bzin(bzin, var_bzin, qt_restr)
        imprimir_matriz_cr(cR, var_cR)
        imprimir_matriz_cb(cB, var_cB)
        # Calculando a Função Objetiva. #
        FO = calcular_fo(cB, B, bzin)
        print(f'\nF.O: {round(FO)}')
        print('\n###################################################')

        # Calculando o Valor do Novo cR. #
        cR = calcular_novo_cr(cR, cB, B, R, qt_var)
        # Imprimindo Matriz cR. #
        imprimir_matriz_cr(cR, var_cR)


main()
