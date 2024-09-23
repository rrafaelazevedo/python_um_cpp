import streamlit as st
from modelo.mmq import mmq
import numpy as np
import matplotlib.pyplot as plt

def desenha_tela():
    st.title("Modelo MMQ")
    st.write("""O modelo MMQ é um modelo matemático que busca encontrar a melhor 
             reta que se ajusta aos dados fornecidos. Para isso, é necessário informar as 
             entradas e saídas, bem como o grau do polinômio que se deseja ajustar aos dados.""")

    # cria um campo de inserção de texto na barra lateral (sidebar)
    # aqui que for preenchido neste campo será armazenado na variável "entradas"
    entradas = \
    st.sidebar.text_input(label="Insira as entradas:",
                          value="1 2 3 4 5",
                          placeholder="Entradas (x)",
                          help="Insira números separados por espaço")
    
    if not entradas.replace(" ", "").replace(".", "").isnumeric():
        st.error("Insira apenas números separados por espaço no campo 'entradas'")
        return
    
    # cria um campo de inserção de texto na barra lateral (sidebar)
    # aqui que for preenchido neste campo será armazenado na variável "saidas"
    saidas = \
    st.sidebar.text_input(label="Insira as saídas:",
                          value="1 4 9 16 25",
                          placeholder="Saídas (y)",
                          help="Insira números separados por espaço")
    
    if not saidas.replace(" ", "").replace(".", "").isnumeric():
        st.error("Insira apenas números separados por espaço no campo 'saidas'")
        return

    # cria um campo de deslizamento na barra lateral (sidebar)
    # aqui que for preenchido neste campo será armazenado na variável "g"
    g = st.sidebar.slider(
        label="Insira o grau do polinomio",
        min_value=1,
        value=2,
        max_value=6)
    
    # cria um botão na barra lateral (sidebar)
    # se o botão for pressionado, a variável "botao" será
    # armazenada como True
    botao = st.sidebar.button(
        label="Rodar"
    )

    if botao == True:

        # transforma a string de entradas e saídas em listas separando a string
        # nas ocorrencias dos espaços
        entradas_lista = entradas.split(" ")
        saidas_lista = saidas.split(" ")

        # print(entradas_lista)
        # print(saidas_lista)

        # transforma as listas de strings em array de inteiros
        entradas_array = np.array(entradas_lista, 
                                  dtype=float)
        
        # transforma as listas de strings em array de inteiros
        saidas_array = np.array(saidas_lista,
                                dtype=float)
        # print(entradas_array)
        # print(saidas_array)
        # print(type(g))
        
        # chama a função mmq que retorna os coeficientes do polinômio
        coefs = mmq(entradas=entradas_array,
                    saidas=saidas_array,
                    g=g)
        
        # arredonda os coeficientes para duas casas decimais
        coefs = coefs.round(2)

        # cria a figura do gráfico
        fig, ax = plt.subplots()

        # adiciona título ao gráfico
        ax.title.set_text("Modelo MMQ")

        # adiciona rótulos aos eixos
        ax.set_xlabel("Entradas")
        ax.set_ylabel("Saídas")

        # plota os pontos no gráfico
        ax.scatter(entradas_array, saidas_array, color="red")

        # gera os valores de x para mostrar a curva entre os valores
        valores_x = np.linspace(start=entradas_array.min(), stop=entradas_array.max(), num=100)

        # calcula a função polinomial para cada valor de x
        valores_y = np.polyval(coefs, valores_x)

        # plota a curva no gráfico
        ax.plot(valores_x, valores_y)

        # exibe o gráfico na tela
        st.pyplot(fig)

        # gerando os caracteres dos coeficientes do polinomio (a, b, c, ...)        
        caracteres = []
        for i in range(97, 97 + g + 1):
            caracteres.append(chr(i))

        # a função 'zip' pareia os elementos de duas colecoes (caracteres e coefs)
        texto = ":white_check_mark: |  "
        for letra, coef in zip(caracteres, coefs):
            texto += f"{letra}: {coef}  |  "

        # mostra na tela um subtitulo com os coeficientes encontrados
        st.subheader("Coeficientes")
        st.success(texto)
                    


if __name__ == "__main__":
    desenha_tela()
