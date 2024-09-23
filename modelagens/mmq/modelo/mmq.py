import numpy as np

def mmq(entradas: np.ndarray,
        saidas: np.ndarray,
        g:int) -> np.ndarray:
    
    """
    Função que calcula o método dos mínimos quadrados para um polinômio de grau 'g'.

    Args:
    entradas (np.ndarray): Array de entradas do polinômio que se deseja ajustar.
    saidas (np.ndarray): Array de saídas do polinômio que se deseja ajustar.
    g (int): Grau do polinômio que se deseja ajustar.

    Returns:
    np.ndarray: Array com os coeficientes do polinômio ajustado.
    (a, b, c, ...)
    """
    
    if g < 1:
        raise Exception(f"Não é possível usar o mmq para g < 0. {g}")
    
    if not isinstance(g, int):
        raise Exception(f"O objeto no parametro 'g' deve ser um 'int'. Foi fornecido um objeto do tipo {type(g)}")
    
    matriz_coefs = np.zeros(shape=(g+1, g+1))
    matriz_resultados = np.zeros(shape=g + 1)
    matriz_somatorios = np.zeros(shape=2 * g + 1)

    for i in range(2 * g, -1, -1):
        matriz_somatorios[i] = (entradas ** i).sum()

    matriz_somatorios = matriz_somatorios[::-1]

    for i in range(0, g + 1, 1):
        matriz_coefs[i, :] = matriz_somatorios[i:i + g + 1]

    for i in range(0, g + 1, 1):
        array_x = entradas ** i
        array_y = saidas ** 1
        array_mult = array_x * array_y
        somatoria = array_mult.sum()

        matriz_resultados[i] = somatoria
    
    matriz_resultados = matriz_resultados[::-1]
    matriz_coefs_inv = np.linalg.inv(matriz_coefs)

    coefs = matriz_coefs_inv.dot(matriz_resultados)

    return coefs