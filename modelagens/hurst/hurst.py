import numpy as np
import statistics
import math
from mmq import metodo_minimos_quadrados

def gerar_sequencia_N(serie_dados: list | np.ndarray, tipo: str) -> list:

    """
    Esta função gera uma sequência de valores N para serem utilizados

    param.:
    serie_dados: serie de dados a serem utilizados
    tipo: tipo de sequência a ser gerada, pode ser "pow2" ou "inc"

    return:
    esta funcao retorna uma lista contendo os valores de N
    """
    
    comprimento_lista = len(serie_dados)

    if tipo == "inc":
        return list(range(2, comprimento_lista + 1))
    
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
    tipo: tipo de execucao do algoritmo, pode ser "pow2" ou "inc"

    return:
    esta funcao retorna uma objeto do tipo float que representa a alea
    """

    sequencia_N = gerar_sequencia_N(serie_dados, tipo)
    
    serie_dominus = []
    serie_functus = []
    for N in sequencia_N:

        # pega os primeiros N dados da serie
        dados = serie_dados[:N]
        
        # calcula a media e o desvio padrao
        media_N = statistics.mean(dados)
        dp_N = statistics.pstdev(dados)

        # se o desvio padrao for 0, pula para o proximo N
        if dp_N == 0:
            continue
        
        # calcula a serie y
        colecao_y = [0]
        for n in range(N):
            subtracao = dados[n] - media_N
            y = subtracao + colecao_y[-1]
            colecao_y.append(y)

        colecao_y.pop(0)

        # calcula o range da serie y
        max_y = max(colecao_y)
        min_y = min(colecao_y)
        range_N = max_y - min_y

        # calcula o ponto log2(N) e log2(r/dp)
        log_N = math.log2(N)
        log_r_dp = math.log2(range_N / dp_N)

        serie_dominus.append(log_N)
        serie_functus.append(log_r_dp)

    # se a serie_dominus ou serie_functus estiver vazia, é pq não há variação
    # de dados ou a série não possui dados
    if serie_dominus == [] or serie_functus == []:
        return 1

    # se a serie_dominus ou serie_functus tiverem apenas um ponto, é pq não há
    # variação de dados suficiente para calcular o coeficiente de Hurst
    if len(serie_dominus) == 1 or len(serie_functus) == 1:
        raise Exception("""Sua série de dados possui muito pouca variação
                            de dados. Somente um ponto foi gerado""")

    # converte as listas em arrays
    arr_dominus = np.array(serie_dominus)
    arr_functus = np.array(serie_functus)
    
    # acha a reta média entre os pontos
    coefs = metodo_minimos_quadrados.mmq(
        arr_dominus,
        arr_functus,
        1)
    
    # retorna o coeficiente angular da reta
    return coefs[0]

if __name__ == "__main__":

    qtd_dados = ""
    # enquanto o usuário não digitar um número, o programa pedirá para digitar um número
    while not qtd_dados.isnumeric():
        qtd_dados = input("Digite a quantidade de dados desejada: ")
    qtd_dados = int(qtd_dados)

    tipo = ""
    # enquanto o usuário não digitar um tipo válido, o programa pedirá para digitar um tipo válido
    while tipo not in ["pow2", "inc"]:
        tipo = input("Digite o tipo de execucao desejado (pow2, inc): ")

    # gerando uma série de dados aleatória para testar o cálculo do coeficiente de Hurst
    serie = np.random.rand(qtd_dados)

    # chama a funcao
    coef_hurst = hurst(serie, tipo)

    # printa o resultado
    print(f"O Coeficiente de Hurst é: {coef_hurst}")
