from itertools import combinations
from typing import Callable

def po_vertices(fo: Callable, restricoes: list, tipo: str="max"):
    """
    Função para resolver um problema de programação linear com duas variáveis de decisão
    usando o método dos vértices

    Args:
        fo (function): função objetivo
        restricoes (list): lista de dicionários contendo as restrições
        tipo (str, opcional): Tipo de problema. "max" ou "min".

    Returns:
        tuple: tupla contendo o ponto que maximiza ou minimiza a função objetivo e o valor da função objetivo
    """

    # encontra os coeficientes angulares e lineares das retas -------------------------------------
    retas = []
    for restricao in restricoes:
        a = round(-restricao["alpha"] / restricao["beta"], 7)
        b = round(restricao["gama"] / restricao["beta"], 7)
        retas.append({"a": a, "b": b})
    # -----------------------------------------------------------------------------------------------

    # encontra os pontos de interseção das retas com os eixos 'functus' e 'dominus' -----------------
    pontos_solucoes = []
    for reta in retas:
        vertice_v = (0, reta["b"])
        vertice_h = (round(-reta["b"] / reta["a"], 7), 0)
        pontos_solucoes.append(vertice_v)
        pontos_solucoes.append(vertice_h)
    # -----------------------------------------------------------------------------------------------

    # encontra os pontos de interseção entre as retas -----------------------------------------------
    comb = combinations(retas, 2)
    for reta1, reta2 in comb:

        a1, b1 = reta1["a"], reta1["b"]
        a2, b2 = reta2["a"], reta2["b"]

        if a1 == a2:
            continue

        x1_cruzamento = round((b2 - b1) / (a1 - a2), 7)
        x2_cruzamento = round(a1 * x1_cruzamento + b1, 7)

        if x1_cruzamento < 0 or x2_cruzamento < 0:
            continue

        pontos_solucoes.append((x1_cruzamento, x2_cruzamento))
    # -----------------------------------------------------------------------------------------------

    # filtra os pontos de solução que respeitam TODAS as restrições ---------------------------------
    lambda_restricao = \
        lambda alpha, x1, beta, x2, gama: alpha * x1 + beta * x2 <= gama if tipo == "max" \
            else alpha * x1 + beta * x2 >= gama

    pontos_solucoes_filtrados = []
    for x1, x2 in pontos_solucoes:
        for restricao in restricoes:
            alpha = restricao["alpha"]
            beta = restricao["beta"]
            gama = restricao["gama"]

            respeita_rest = lambda_restricao(alpha=alpha, x1=x1, beta=beta, x2=x2, gama=gama)
            if not respeita_rest:
                break
        else:
            # a execução só entra aqui se o loop for concluído SEM passar pelo BREAK
            pontos_solucoes_filtrados.append((x1, x2))
    # -----------------------------------------------------------------------------------------------
    
    # encontra o ponto que maximiza ou minimiza a função objetivo dentre os pontos restantes --------
    valor_solucao = float("-inf") if tipo == "max" else float("inf")
    ponto_solucao = None
    for x1, x2 in pontos_solucoes_filtrados:
        valor_vertice = fo(x1=x1, x2=x2)
        print(f"O ponto: ({x1}, {x2}) tem valor: {valor_vertice}")
        if tipo == "max" and valor_vertice > valor_solucao:
            valor_solucao = valor_vertice
            ponto_solucao = (x1, x2)
        elif tipo == "min" and valor_vertice < valor_solucao:
            valor_solucao = valor_vertice
            ponto_solucao = (x1, x2)
    # -----------------------------------------------------------------------------------------------

    return ponto_solucao, valor_solucao, retas

if __name__ == "__main__":

    coefs = []
    for _ in range(2):
        coef = float(input("Digite o coeficiente de x1 na FO: "))
        coefs.append(coef)

    fo = lambda x1, x2: coefs[0] * x1 + coefs[1] * x2

    tipo = input("Digite o tipo do problema (0: max ou 1: min): ")
    tipo = "max" if tipo == "0" else "min"
    qtd_restricoes = int(input("Digite a quantidade de restrições: "))
    restricoes = []
    for i in range(qtd_restricoes):
        alpha = float(input(f"Digite o coeficiente de x1 na restrição {i + 1}: "))
        beta = float(input(f"Digite o coeficiente de x2 na restrição {i + 1}: "))
        gama = float(input(f"Digite o valor da restrição {i + 1}: "))
        restricao = {"alpha": alpha, "beta": beta, "gama": gama}
        restricoes.append(restricao)
    
    print("-" * 100)
    print("Resolvendo o problema...")
    solucao, resultado_final, retas = po_vertices(fo=fo, restricoes=restricoes, tipo=tipo)
    print("Problema resolvido!")
    print("-" * 100)

    print(f"A solução é: x1={solucao[0]} e x2={solucao[1]} com valor: {resultado_final}")
    print(f"As retas são: {retas}")
