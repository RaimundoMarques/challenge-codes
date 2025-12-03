# Desafio 1 - Ordenação de arrays
# 1. Sabendo que você tem dois arrays de números inteiros, crie um terceiro array com a junção dos dois anteriores em
# ordem crescente.

# Arrays
array1 = [1, 2, 3, 4, 5]
array2 = [6, 7, 8, 9, 10]

# Concatena os dois arrays em outra lista
out = array1 + array2

# Verifica o tamanho da lista para saber quantas vezes vai ser preciso verificar a iteração
len_out = len(out)
for i in range(len_out):
    # len_out - i - 1: a cada passada, o último elemento já está na posição correta
    # então não precisamos comparar com ele novamente
    for j in range(0, len_out - i - 1):
        
        # Se o elemento atual for maior que o próximo, eles estão fora de ordem
        if out[j] > out[j + 1]:
            # Troca os elementos: o maior "borbulha" para a direita
            out[j], out[j + 1] = out[j + 1], out[j]

print(out)

