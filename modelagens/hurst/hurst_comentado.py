import numpy as np
import statistics
import math
from mmq import metodo_minimos_quadrados

def gerar_sequencia_N(serie_dados, tipo="pow2"):

    """
    Esta função gera uma sequência de valores N para serem utilizados

    param.:
    serie_dados: serie de dados para calcular o coef. de aleatoriedade
    tipo: tipo de sequência a ser gerada. Pode ser 'pow2' ou 'inc'

    return:
    esta função retorna uma lista contendo os valores de N para serem
    utilizados no cálculo do coeficiente de aleatoriedade
    """
    
    # quantidade de dados na série
    comprimento_lista = len(serie_dados)

    # se o tipo de sequência for 'inc', a sequência é gerada de forma
    # incremental a partir de 2 [2, 3, 4, 5, ...]
    if tipo == "inc":
        return list(range(2, comprimento_lista + 1))

    # se o tipo de sequência for 'pow2', a sequência é gerada de forma
    # exponencial a partir de 2 [2, 4, 8, 16, ...]    

    # lista para armazenar os valores de N (comeca apenas com o valor 2)
    sequencia_N = [2]
    while sequencia_N[-1] * 2 <= comprimento_lista:
        sequencia_N.append(sequencia_N[-1] * 2)
    
    if comprimento_lista not in sequencia_N:
        sequencia_N.append(comprimento_lista)
    
    return sequencia_N

def hurst(serie_dados: list | np.ndarray, tipo: str = "pow2") -> float:
    """
    Esta função calcula o coeficiente de aleatoriedade da series
    de dados fornecida no parametro 'serie_dados'.

    param.:
    series_dados: serie para calcular o coef. de aleatoriedade
    tipo: tipo de sequência a ser gerada. Pode ser 'pow2' ou 'inc'

    return:
    esta funcao retorna uma objeto do tipo float que representa a alea
    """

    # gera uma lista com a sequencia de valores N, em que cada numero dentro
    # desta lista representa cada iteração do algoritmo
    sequencia_N = gerar_sequencia_N(serie_dados, tipo)

    # gera as listas que armazenarao os valores de dominus e functus (pontos)    
    serie_dominus = []
    serie_functus = []
    for N in sequencia_N:

        # pega os primeiros N valores da serie de dados
        dados = serie_dados[:N]
        
        # calcula a media e o desvio padrao populacional dos N primeiros valores
        media_N = statistics.mean(dados)
        dp_N = statistics.pstdev(dados)

        # se o desvio padrão for zero, pula para a próxima iteração
        if dp_N == 0:
            continue
        
        # encontra a coleção de y's para calcular o 'range'
        colecao_y = [0]
        for n in range(N):
            subtracao = dados[n] - media_N
            y = subtracao + colecao_y[-1]
            colecao_y.append(y)

        colecao_y.pop(0)

        # maximo e minimo da colecao de y's
        max_y = max(colecao_y)
        min_y = min(colecao_y)

        # range da colecao de y's
        range_N = max_y - min_y

        # calcula o logaritmo de N
        log_N = math.log2(N)

        # calcula o logaritmo do range dividido pelo desvio padrao
        log_r_dp = math.log2(range_N / dp_N)

        # adiciona os pontos na serie de dados
        serie_dominus.append(log_N)
        serie_functus.append(log_r_dp)

    # se as series de dados estão vazias, é pq a series de dados
    # possui dados com desvio padrão igual a zero
    if serie_dominus == [] or serie_functus == []:
        return 1

    # se a serie de dados possui apenas um ponto, é pq a serie de dados
    # possui pouca variação
    if len(serie_dominus) == 1 or len(serie_functus) == 1:
        raise Exception("""Sua série de dados possui muito pouca variação
                            de dados. Somente um ponto foi gerado""")

    # transforma as listas em arrays numpy para serem utilizadas no
    # método dos mínimos quadrados
    arr_dominus = np.array(serie_dominus)
    arr_functus = np.array(serie_functus)

    # calcula os coeficientes da reta que melhor se ajusta aos pontos
    coefs = metodo_minimos_quadrados.mmq(
        arr_dominus,
        arr_functus,
        1)
    
    # retorna apenas o coeficiente angular da reta (coeficiente de Hurst)
    return coefs[0]

# o 'if' abaixo filtra os comandos dentro dele. Esses comandos só serão
# executados se o script for executado diretamente. Se o script for importado
# por outro script, os comandos dentro do 'if' não serão executados
if __name__ == "__main__":

    # usando a função 'hurst' para teste

    # o usuário deve digitar a quantidade de dados e o tipo de sequência
    qtd_dados = ""
    # enquanto o usuário não digitar um número, o programa pedirá para
    # digitar novamente
    while not qtd_dados.isdigit():
        qtd_dados = input("Digite a quantidade de dados desejada: ")

    # converte a quantidade de dados para inteiro, pois a função 'input'
    # retorna uma SEMPRE string    
    qtd_dados = int(qtd_dados)

    # o usuário deve digitar o tipo de sequência desejada
    tipo = ""
    # enquanto o usuário não digitar 'inc' ou 'pow2', o programa pedirá
    # para digitar novamente
    while tipo not in ["pow2", "inc"]:
        tipo = input("Digite o tipo de sequência desejada (inc ou pow2): ")

    # gerando uma série de dados aleatórios para testar a função 'hurst'
    serie = np.random.rand(qtd_dados)

    # chamando a função 'hurst' e armazenando o resultado em uma variável
    coef_hurst = hurst(serie, tipo)

    # imprimindo o resultado
    print(f"O Coeficiente de Hurst é: {coef_hurst}")
