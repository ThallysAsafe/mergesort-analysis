import time
import math
import random
import matplotlib.pyplot as plt
import numpy as np


def merge_sort_custom(arr, key, reverse=False):
    if len(arr) > 1:
        meio = len(arr) // 2
        metade_esquerda = arr[:meio]
        metade_direita = arr[meio:]

        merge_sort_custom(metade_esquerda, key, reverse)
        merge_sort_custom(metade_direita, key, reverse)

        i = j = k = 0
        while i < len(metade_esquerda) and j < len(metade_direita):
            valor_esquerda = key(metade_esquerda[i])
            valor_direita = key(metade_direita[j])

            if not reverse:
                if valor_esquerda < valor_direita:
                    arr[k] = metade_esquerda[i]; i += 1
                else:
                    arr[k] = metade_direita[j]; j += 1
            else:
                if valor_esquerda > valor_direita:
                    arr[k] = metade_esquerda[i]; i += 1
                else:
                    arr[k] = metade_direita[j]; j += 1
            k += 1

        while i < len(metade_esquerda):
            arr[k] = metade_esquerda[i]; i += 1; k += 1
        while j < len(metade_direita):
            arr[k] = metade_direita[j]; j += 1; k += 1

def gerar_dados_alunos(num_alunos=50):
    dados = []
    for i in range(num_alunos):
        aluno = { "nome": f"Aluno {i}", "ira": round(random.uniform(5.0, 10.0), 2) }
        dados.append(aluno)
    return dados

def analisar_e_plotar_sem_escala():
    tamanhos_n = [1000, 2000, 4000, 8000, 12000, 16000, 20000, 24000, 28000, 32000, 100000, 120000, 140000, 160000, 180000, 200000, 360000, 400000, 500000]
    tempos_medidos = []

    print("Iniciando análise de performance do Merge Sort Customizado...")
    print("-" * 30)
    print("Tamanho (n)\t| Tempo (s)")
    print("-" * 30)

    for n in tamanhos_n:
        dados_teste = gerar_dados_alunos(n)
        inicio = time.time()
        merge_sort_custom(dados_teste, key=lambda aluno: aluno["ira"], reverse=True)
        fim = time.time()
        tempo_gasto = fim - inicio
        tempos_medidos.append(tempo_gasto)
        print(f"{n}\t\t| {tempo_gasto:.6f}")

    print("\nAnálise concluída. Gerando gráfico sem escala...")

    eixo_x_continuo = np.linspace(min(tamanhos_n), max(tamanhos_n), 400)
    
    y_n_log_n = eixo_x_continuo * np.log2(eixo_x_continuo + 1e-9)
    y_n_quadrado = eixo_x_continuo**2
    y_n_linear = eixo_x_continuo

    fig, ax1 = plt.subplots(figsize=(12, 8))

    ax1.set_xlabel('Tamanho da Entrada (n)')
    ax1.set_ylabel('Tempo de Execução (segundos)', color='tab:blue')
    ax1.plot(tamanhos_n, tempos_medidos, 'o', color='tab:blue', markersize=8, label='Merge Sort (Experimental)')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True, linestyle='--')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Número de Operações (Escala Teórica)', color='tab:orange')
    
    ax2.plot(eixo_x_continuo, y_n_log_n, '-', color='tab:orange', label=r'Complexidade $O(n \log n)$')
    ax2.plot(eixo_x_continuo, y_n_quadrado, '--', color='tab:green', label=r'Complexidade $O(n^2)$')
    ax2.plot(eixo_x_continuo, y_n_linear, ':', color='tab:red', label=r'Complexidade $O(n)$')
    ax2.tick_params(axis='y', labelcolor='tab:orange')


    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left')

    plt.title('Desempenho Experimental vs. Curvas de Complexidade Puras')
    fig.tight_layout()

    plt.savefig('comparativo_sem_escala.png')
    print("Gráfico 'comparativo_sem_escala.png' salvo com sucesso!")
    plt.show()


if __name__ == "__main__":
    analisar_e_plotar_sem_escala()