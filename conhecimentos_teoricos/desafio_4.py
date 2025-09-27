# Desafio 4 - Encontrar o maior número em uma matriz AxB
# Crie uma função ou procedimento que receba uma matriz AxB do tipo numérico 
# e dois parâmetros que indicam o tamanho da matriz A, B. Encontre o maior número dessa matriz.



# Matriz de exemplo
l_1 = [1, 35, 3]
l_2 = [9, 2, 7]
l_3 = [4, 8, 16]
l_4 = [10, 101, 12]

# Matriz
matriz_exemplo = [l_1, l_2, l_3, l_4]

# Detecta automaticamente as dimensões da matriz
linhas = len(matriz_exemplo)           # Número de linhas (A)
colunas = len(matriz_exemplo[0])       # Número de colunas (B)

# Exibe as dimensões detectadas
print(f"Dimensão da matriz: {linhas}x{colunas}")

# Exibe a matriz
print("\nMatriz:")
for linha in matriz_exemplo:
    print(linha)



def maiorNumero(matriz, linhas, colunas):
    # Inicializa com o primeiro elemento
    maior = matriz[0][0]
    
    # Percorre a matriz
    for i in range(linhas):
        for j in range(colunas):
            if matriz[i][j] > maior:
                maior = matriz[i][j]

    return maior


# Encontra o maior número
maior_numero = maiorNumero(matriz_exemplo, linhas, colunas)
print(f"\nMaior número da matriz: {maior_numero}")
