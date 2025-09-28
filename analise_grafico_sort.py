# Importando bibliotecas necessárias
import time
import random
import math
import matplotlib.pyplot as plt
import numpy as np

# --- Implementação do Algoritmo Merge Sort ---
def merge_sort_custom(arr, key):
    # Caso base: se o tamanho do array for maior que 1, executa a divisão
    if len(arr) > 1:
        
        # Encontra o meio do array para dividi-lo em duas metades
        meio = len(arr) // 2
        metade_esquerda = arr[:meio]  # Primeira metade do array
        metade_direita = arr[meio:]  # Segunda metade do array

        # Chama recursivamente o merge_sort_custom para ordenar ambas as metades
        merge_sort_custom(metade_esquerda, key)
        merge_sort_custom(metade_direita, key)

        # Inicializa os índices para percorrer as metades e o array original
        i = j = k = 0

        # Enquanto houver elementos em ambas as metades para comparar
        while i < len(metade_esquerda) and j < len(metade_direita):
            # Comparação dos elementos usando a função 'key' fornecida
            if key(metade_esquerda[i]) < key(metade_direita[j]):
                arr[k] = metade_esquerda[i]  # Atribui o elemento da metade esquerda
                i += 1  # Avança para o próximo elemento na metade esquerda
            else:
                arr[k] = metade_direita[j]  # Atribui o elemento da metade direita
                j += 1  # Avança para o próximo elemento na metade direita
            k += 1  # Avança para a próxima posição no array original

        # Se ainda houver elementos na metade esquerda, copia-os para o array
        while i < len(metade_esquerda):
            arr[k] = metade_esquerda[i]
            i += 1
            k += 1

        # Se ainda houver elementos na metade direita, copia-os para o array
        while j < len(metade_direita):
            arr[k] = metade_direita[j]
            j += 1
            k += 1

# --- Funções para o Experimento ---
def gerar_dados_alunos(num_alunos):
    dados = [{"nome": f"Aluno {i}", "ira": round(random.uniform(5.0, 10.0), 2)} for i in range(num_alunos)]
    return dados

def executar_experimento():
    tamanhos_n = [1000, 5000, 10000, 25000, 50000, 100000, 200000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 2000000]
    tempos_medidos = []
    print("Executando experimento para o artigo...")
    print("\n| Tamanho da Entrada (n) | Tempo de Execução (s) |")
    print("| :--------------------- | :-------------------- |")
    for n in tamanhos_n:
        dados_teste = gerar_dados_alunos(n)
        inicio = time.time()
        merge_sort_custom(dados_teste, key=lambda aluno: aluno["ira"])
        fim = time.time()
        tempo_gasto = fim - inicio
        tempos_medidos.append(tempo_gasto)
        print(f"| {n:<22} | {tempo_gasto:<21.6f} |")
    print("\nExperimento concluído.")
    return tamanhos_n, tempos_medidos

def gerar_grafico_experimental_simples(tamanhos_n, tempos_medidos):
    """
    Gera um gráfico simples apenas com os dados experimentais.
    Este será a "Figura 1" do artigo.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(10, 6))

    # Plota os pontos e uma linha conectando-os para mostrar a tendência
    plt.plot(tamanhos_n, tempos_medidos, 'o-', color='blue', markersize=8, label='Tempo Experimental Medido')

    plt.xlabel("Tamanho da Entrada (n)")
    plt.ylabel("Tempo de Execução (segundos)")
    plt.title("Desempenho Experimental do Merge Sort")
    plt.legend()
    plt.ylim(bottom=0); plt.xlim(left=0)
    plt.savefig('grafico_experimental_simples.png', dpi=300)
    plt.show()

def gerar_grafico_final_artigo(tamanhos_n, tempos_medidos):
    n_array = np.array(tamanhos_n, dtype=np.float64)
    t_array = np.array(tempos_medidos)

    # Pega o último ponto do experimento para ajustar as curvas teóricas
    ultimo_n = n_array[-1]
    ultimo_tempo = t_array[-1]

    # Calcula as constantes 'c' para cada curva de complexidade
    c_n_log_n = ultimo_tempo / (ultimo_n * np.log2(ultimo_n))
    c_n_quadrado = ultimo_tempo / (ultimo_n**2)
    c_n_linear = ultimo_tempo / ultimo_n

    # Cria um eixo X contínuo para desenhar as curvas
    eixo_x_suave = np.linspace(n_array.min(), n_array.max(), 400)

    # Calcula os valores Y para cada curva teórica ajustada
    y_n_log_n = c_n_log_n * eixo_x_suave * np.log2(eixo_x_suave + 1e-9) # Adicionado 1e-9 para evitar log(0)
    y_n_quadrado = c_n_quadrado * eixo_x_suave**2
    y_n_linear = c_n_linear * eixo_x_suave
    y_n_omega = c_n_log_n * eixo_x_suave * np.log2(eixo_x_suave + 1e-9)  # Big Omega (O mesmo de O(n log n))
    y_n_theta = c_n_log_n * eixo_x_suave * np.log2(eixo_x_suave + 1e-9)  # Big Theta (O mesmo de O(n log n))

    # --- Plotagem Profissional para o Artigo ---
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(10, 6))
    
    # Plot dos dados experimentais como pontos distintos
    plt.plot(n_array, t_array, 'o', markersize=8, color='blue', label='Desempenho Experimental')

    # Plot das curvas teóricas
    plt.plot(eixo_x_suave, y_n_log_n, '-', color='green', linewidth=2, label=r'Pior caso $O(n \log n)$')
    plt.plot(eixo_x_suave, y_n_omega, '--', color='orange', linewidth=1.5, label=r'Melhor caso $\Omega(n \log n)$')
    plt.plot(eixo_x_suave, y_n_theta, ':', color='brown', linewidth=1.5, label=r'Complexidade média $\Theta(n \log n)$')
    
    plt.xlabel("Tamanho da Entrada (n)")
    plt.ylabel("Tempo de Execução (segundos)")
    plt.title("Análise Comparativa do Desempenho do Merge Sort")
    plt.legend(loc='upper left')
    plt.ylim(bottom=0); plt.xlim(left=0)
    plt.savefig('grafico_artigo_final.png', dpi=300)
    plt.show()

# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    n, tempos = executar_experimento()
    gerar_grafico_final_artigo(n, tempos)
    gerar_grafico_experimental_simples(n, tempos)