linhas = 3
colunas = 4

# Criando uma matriz preenchida com zeros
matriz = []

for i in range(linhas):
    linha = [] # 1. Cria uma lista vazia para ser a "linha" atual
    for j in range(colunas):
        linha.append(0) # 2. Adiciona um zero para cada "coluna" desejada
    matriz.append(linha) # 3. Coloca a linha completa dentro da matriz

# Exibindo o resultado
for l in matriz:
    print(l)