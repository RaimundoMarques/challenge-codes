# Desafio 4 - Encontrar o maior número em uma matriz AxB
# Crie uma função ou procedimento que receba uma matriz AxB do tipo numérico 
# e dois parâmetros que indicam o tamanho da matriz A, B. Encontre o maior número dessa matriz.


# Matriz
l_1 = [1, 5, 3]
l_2 = [9, 2, 7]
l_3 = [4, 38, 6]
l_4 = [10, 10, 2]

# Matriz
matriz = [l_1, l_2, l_3, l_4]

# Detecta automaticamente as dimensões da matriz
linhas = len(matriz)
colunas = len(matriz[0])

print(f"Dimensão da matriz: {linhas}x{colunas}")

print("\nMatriz:")
for linha in matriz:
    print(linha)

# Detecta números repetidos sem append
print("\n=== NÚMEROS REPETIDOS ===")
tem_repetidos = False

# Para cada número único na matriz
num_unicos = set()
for i in range(linhas):
    for j in range(colunas):
        num_unicos.add(matriz[i][j])

# Para cada número único, conta ocorrências
for numero in num_unicos:
    contador = 0
    posicoes_str = ""
    
    for i in range(linhas):
        for j in range(colunas):
            if matriz[i][j] == numero:
                contador += 1
                if posicoes_str:
                    posicoes_str += f", ({i},{j})"
                else:
                    posicoes_str += f"({i},{j})"
    
    if contador > 1:
        print(f"Número {numero} aparece {contador} vezes nas posições: {posicoes_str}")
        tem_repetidos = True

if not tem_repetidos:
    print("Nenhum número repetido encontrado.")

# Encontra o maior número
print("\n=== MAIOR NÚMERO ===")
maior = matriz[0][0]
for i in range(linhas):
    for j in range(colunas):
        if matriz[i][j] > maior:
            maior = matriz[i][j]

print(f"Maior número da matriz: {maior}")

# Mostra posições do maior número
print(f"Coordenadas do maior número ({maior}):")
for i in range(linhas):
    for j in range(colunas):
        if matriz[i][j] == maior:
            print(f"  ({i},{j})")
