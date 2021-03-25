# Projete um programa que receba como entrada dois caminhos (arranjos de número inteiros)
# e verifique se os dois caminhos formam o mesmo ciclo.
# Você deve assumir que os arranjos de entrada formam caminhos válidos.

# Para este programa não é necessário fazer a entrada de dados, basta escrever a função e os testes automatizados.

def mesmoCiclo(caminho1, caminho2):
    tam1 = len(caminho1)
    tam2 = len(caminho2)
    numVertices = tam1 - 1

    # Se não tiverem o mesmo tamanho ou não tiverem elementos, não tem como serem equivalentes
    if tam1 == tam2 and tam1 > 0:
        # Caso de caminho de tamanho 1, causava problemas com numVertices
        if tam1 == 1:
            if caminho1[0] == caminho2[0]:
                return True
            else:
                return False

        for i in range(numVertices):
            # Se achar um vértice igual a o primeiro
            if caminho1[0] == caminho2[i]:
                # O caminho é tratado como equivalente até ser provado o contrário
                for j in range(1, numVertices):
                    if caminho1[j] != caminho2[(j+i) % numVertices]:
                        break
                # Se j foi até o final, não há diferença
                if j == numVertices - 1:
                    return True

    return False


assert mesmoCiclo([1, 2, 5, 1], [2, 5, 1, 2]) == True
assert mesmoCiclo([1, 5, 2, 1], [2, 5, 1, 2]) == False
assert mesmoCiclo([1, 2, 1], [2]) == False
assert mesmoCiclo([1], [1]) == True
assert mesmoCiclo([1, 2, 3, 1, 2, 4, 1], [2, 3, 1, 2, 4, 1, 2]) == True
assert mesmoCiclo([1, 2, 3, 1, 2, 4, 1], [2, 3, 1, 2, 1, 4, 2]) == False
assert mesmoCiclo([7, 8, 9, 7, 8, 9, 7], [8, 9, 7, 8, 9, 7, 8]) == True
