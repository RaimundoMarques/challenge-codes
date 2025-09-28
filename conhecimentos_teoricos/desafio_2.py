# Desafio 2 - Ordenação de arrays
# 2. Imagine que você tenha uma tela com duas entradas, uma com o texto e outra com a string a ser encontrada. Monte um
# algoritmo para encontrar a posição dessa string nesse texto. Caso não encontre, retornar -1.

# Texto e string
text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry."
string = "is"

# Caso não encontre, retornar -1
found = -1
print("Texto: ", text)
print("String à ser encontrada: ", string)

# Flag usada para verificar se houve correspondência na iteração atual
step = True


 # Percorre o texto para encontrar uma string válida dentro do texto onde cabe a string
for i in range(len(text) - len(string)):
    print("--------------------------------")
    print("Iteração: ", i)

    #Separa uma parte do texto para verificar se a string está presente nessa parte
    print("Texto completo: ", text[i:i+len(string)])
    step = True

    # Compara caractere por caractere a string com a parte do texto
    for j in range(len(string)):
        if text[i + j] != string[j]:
            step = False
            break
    # Se encontrar a string, atualiza a flag e para o loop com a posição so texto encontrado
    if step:
        print("Texto encontrado: ", text[i:i+len(string)])
        print("String: ", string)
        # Guarda a posição do texto econtrado
        found = i
        break

print("Texto encontrado na iteração: ", found)