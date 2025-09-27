# Desafio 3 - Ordenação de arrays
# 3. Dado um número N inteiro, escreva um algoritmo que descreva os N números da sequência de Fibonacci.

# Obs:A soma do próximo termo é igual ao termo anterior

# Quantidade de termos que queremos gerar
number = 11

# Lista para guardar a sequência de Fibonacci
result_fibonacci = []

print("Número:", number)

# Foi preciso definir os dois primeiros números da sequência
a, b = 0, 1

# Loop de iteração 
result_fibonacci = [0] * number  # Cria uma lista de tamanho 'number' preenchida com zeros
for i in range(number):
    result_fibonacci[i] = a   # Atribui o número atual (a) na posição correta da lista
    a, b = b, a + b       # Atualiza os valores: o "a" vira "b" e o "b" vira "a+b"

# Exibe o resultado
print("Sequência de Fibonacci:", result_fibonacci)
