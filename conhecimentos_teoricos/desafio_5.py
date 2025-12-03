# Desafio 5 - Multiplicação de números primos seguidos
# Informando uma entrada numérica N, informe o total da multiplicação de N números primos seguidos.

# Obs: Levando em consideração que 1 não é um número primo

# Número de entrada
primeNumberCalc = 4

# Função para verificar se o número é primo
def primo(numero):
    if numero < 2:
        return False
    
    # Se o número é divisível por algum número entre 2 e sua raiz quadrada
    # o número é primo
    for i in range(2, int(numero ** 0.5) + 1):
        # Se o resto da divisão for 0, o número não é primo
        if numero % i == 0:
            return False
    
    # Retorna True se o número é primo (debug)
    print(f"Primo: {numero}")
    return True

def multiplicaPrimos(n):
    # Inicializa o total com 1 para começar a multiplicação
    total = 1
    
    # Contador de primos encontrados
    primos_encontrados = 0
    
    # Número atual que estamos testando (começando pelo 2, primeiro primo)
    numero_atual = 2
    
    # Continua procurando primos até encontrar N primos
    while primos_encontrados < n:
        # Se o número atual for primo
        if primo(numero_atual):
            # Multiplica o total pelo primo encontrado
            total *= numero_atual
            
            # Incrementa o contador dos números primos encontrados
            primos_encontrados += 1
        
        # Testa o próximo número
        numero_atual += 1
    
    # Retorna o resultado da multiplicação de todos os primos
    return total

# Multiplica os primeiros N números primos
print(f"Multiplicando os primeiros {primeNumberCalc} números primos:")
resultado = multiplicaPrimos(primeNumberCalc)
print(f"Números multiplicados: {resultado}")
