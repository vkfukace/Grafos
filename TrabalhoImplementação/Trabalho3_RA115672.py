# Algoritmos em Grafos
# Trabalho 1
# Geração de árvores aleatórias usando grafos
#
# Aluno: Vinícius Kenzo Fukace
# RA: 115672

from typing import ClassVar, List, Dict, Tuple, Union, final
from collections import deque
import random
import time


# Definição de Dados
#
# Por convenção, as chaves ligadas aos vértices serão do tipo int.
# Para os grafos que serão utilizados na construção das árvores, será utilizada
# matriz de adjacência, pois serão grafos completos.
# Para as árvores resultantes, será utilizada lista de adjacência.


# Classes Auxiliares


# Classe auxiliar para randomTreeRandomWalk.
# Permite remover e pegar um elemento aleatório em tempo constante.
#
# Baseado na estrutura de dados descrita em:
# https://www.geeksforgeeks.org/design-a-data-structure-that-supports-insert-delete-search-and-getrandom-in-constant-time/
class ListaMapeada:
    # Inicializa a lista mapeada com n elementos [0, 1, ..., n-1].
    # Assume que n > 0.
    def __init__(self, n: int) -> None:
        self.lista: List[int] = []
        self.hash: Dict[int, int] = {}
        for i in range(n):
            self.lista.append(i)
            self.hash[i] = i

    # Remove o elemento x da estrutura.
    # Assume que x está presente na lista.
    def remove(self, x: int) -> None:
        # Pega o índice em que x se encontra
        # pop() em Dict tem tempo de execução médio O(1).
        posX = self.hash.pop(x)
        # Troca x e o último elemento de lugar.
        tam = len(self.lista)
        ultimo = self.lista[tam-1]
        self.lista[posX], self.lista[tam-1] = \
            self.lista[tam-1], self.lista[posX]
        # pop() em lista tem tempo de execução O(1).
        self.lista.pop()
        self.hash[ultimo] = posX

    # Retorna um elemento aleatório da lista e o remove no processo.
    # Assume que há elementos na lista.
    def popAleatorio(self) -> int:
        indice = random.randint(0, len(self.lista) - 1)
        numRetorno = self.lista[indice]
        self.remove(numRetorno)
        return numRetorno


# Classe auxiliar para Kruskal
#
# Baseado na estrutura de dados descrita em:
# https://en.wikipedia.org/wiki/Disjoint-set_data_structure
class ConjuntoDisjunto:
    # Inicializa um conjunto disjunto de n elementos [0, 1, ..., n-1].
    # Assume que n > 0
    def __init__(self, n: int) -> None:
        self.pai: List[int] = [i for i in range(n)]
        self.rank: List[int] = [0 for i in range(n)]

    # Retorna o vértice pai do conjunto de v.
    # Assume que v está na estrutura.
    def findSet(self, v: int) -> None:
        if self.pai[v] != v:
            self.pai[v] = self.findSet(self.pai[v])
        return self.pai[v]

    # Junta os conjuntos de u e v.
    # Assume que u e v estejam na estrutura.
    #
    # Caso u e v estejam no mesmo conjunto, retorna False.
    # Caso contrário, retorna True.
    def union(self, u: int, v: int) -> bool:
        u = self.findSet(u)
        v = self.findSet(v)

        if u == v:
            return False

        if self.rank[u] < self.rank[v]:
            self.rank[u], self.rank[v] = self.rank[v], self.rank[u]
        self.pai[v] = u

        if self.rank[u] == self.rank[v]:
            self.rank[u] += 1

        return True


# Classes Principais


class Vertice:
    # Inicializa o vértice com todos seus atributos sendo None
    # e lista de adjacência vazia.
    def __init__(self) -> None:
        self.d: Union[int, None] = None
        self.f: Union[int, None] = None
        self.pai: Union[str, None] = None
        self.cor: Union[str, None] = None
        self.adj: List[int] = []


class Arvore:
    # Inicializa a árvore com nenhum vértice.
    def __init__(self) -> None:
        self.vertices: Dict[int, Vertice] = {}
        self.numArestas: int = 0

    # Adiciona um vértice v à árvore.
    #
    # Caso um vértice com a mesma chave já exista, não é adicionado
    # e retorna False.
    # Caso contrário, retorna True.
    def addVertice(self, v: int) -> bool:
        if v not in self.vertices:
            self.vertices[v] = Vertice()
            return True
        else:
            return False

    # Remove um vértice v da árvore.
    #
    # Caso um vértice com a mesma chave não exista, retorna false.
    # Caso contrário, remove o vértice e retorna True.
    def removeVertice(self, v: int) -> bool:
        if v in self.vertices:
            for u in self.vertices[v].adj:
                self.vertices[u].adj.remove(v)
            del self.vertices[v]
            return True
        else:
            return False

    # Adiciona uma aresta (u, v) à árvore.
    #
    # Caso a aresta já exista, não é adicionada e retorna False.
    # Caso não existam vértices com chaves u ou v, não é adicionada
    # e retorna False.
    def addAresta(self, u: int, v: int) -> bool:
        if u not in self.vertices or v not in self.vertices:
            return False
        if u in self.vertices[v].adj:
            return False

        self.vertices[u].adj.append(v)
        self.vertices[v].adj.append(u)
        self.numArestas += 1
        return True

    # Remove uma aresta (u, v) da árvore.
    #
    # Caso a aresta não exista, retorna False.
    # Caso contrário, remove a aresta e retorna True.
    def removeAresta(self, u: int, v: int) -> bool:
        if u in self.vertices[v].adj:
            self.vertices[v].adj.remove(u)
            self.vertices[u].adj.remove(v)
            self.numArestas -= 1
            return True
        else:
            return False

    # Inicializa todos os vértices da árvore com os valores padrão e a cor dada.
    def __inicializaVertices(self, cor):
        for u in self.vertices:
            self.vertices[u].cor = cor
            self.vertices[u].pai = None
            self.vertices[u].d = None
            self.vertices[u].f = None

    # Função auxiliar de isArvore().
    #
    # Caso encontre um ciclo na árvore, retorna False.
    # Caso contrário, retorna True.
    #
    # Baseado no pseudocódigo dos slides.
    def __dfsVisit(self, u: int) -> bool:
        resultado = True
        self.vertices[u].cor = "cinza"

        for v in self.vertices[u].adj:
            if self.vertices[v].cor == "branco":
                self.vertices[v].pai = u
                resultado = resultado and self.__dfsVisit(v)
            elif v != self.vertices[u].pai:
                # Se o vértice não for branco e não for o pai de v,
                # ele já foi visitado antes, e forma um ciclo.
                resultado = False

        self.vertices[u].cor = "preto"
        return resultado

    # Verifica se a árvore tem as propriedades de uma árvore
    #
    # Caso não haja vértices na árvore, retorna False.
    # Caso encontre componentes disconexos ou ciclos, retorna False.
    # Caso contrário, retorna True.
    #
    # Baseado no pseudocódigo dos slides do DFS.
    def isArvore(self) -> bool:
        if not self.vertices:
            return False

        self.__inicializaVertices("branco")
        ehPrimeiraExecucao: bool = True

        # Depois da primeira execução de dfsVisit(), todos os outros elementos
        # devem estar coloridos. Se esse não for o caso, há elementos desconexos.
        for u in self.vertices:
            if self.vertices[u].cor == "branco":
                if not ehPrimeiraExecucao:
                    return False
                if self.__dfsVisit(u) == False:
                    return False
                ehPrimeiraExecucao = False
        return True

    # Executa a busca em largura na árvore começando no vértice s.
    # Grava o pai e a distância até s de cada vértice.
    # Retorna uma tupla com o primeiro vértice descoberto com a distância máxima
    # até s e sua distância.
    #
    # Caso não exista vértice com nome s na árvore, retorna (None, 0).
    #
    # Baseado no pseudocódigo dos slides.
    def bfs(self, s: int) -> Tuple[int, int]:
        maior = (None, 0)

        if s in self.vertices:
            self.__inicializaVertices("branco")
            self.vertices[s].d = 0
            self.vertices[s].cor = "cinza"
            fila = deque([])
            fila.append(s)

            while fila:
                u = fila.popleft()
                for v in self.vertices[u].adj:
                    if self.vertices[v].cor == "branco":
                        self.vertices[v].cor = "cinza"
                        self.vertices[v].d = self.vertices[u].d + 1
                        self.vertices[v].pai = u
                        fila.append(v)
                    self.vertices[u].cor = "preto"
                if self.vertices[u].d > maior[1]:
                    maior = (u, self.vertices[u].d)
        return maior

    # Retorna o comprimento do maior caminho da árvore
    #
    # Caso a árvore não for conexa e acíclica, retorna -1
    # Caso a árvore não tenha vértices, retorna -1
    #
    # Baseado no pseudocódigo dos slides.
    def diametro(self) -> int:

        if self.isArvore() == False:
            return -1
        # Pega a primeira chave de self.vertices
        v = next(iter(self.vertices))
        a = self.bfs(v)
        return self.bfs(a[0])[1]

    # Gera uma árvore aleatória com n vértices.
    # Sobrescreve os dados da árvore anteriores à execução.
    #
    # Caso n < 1, a operação não é executada.
    #
    # Baseado no pseudocódigo dos slides.
    def randomTreeRandomWalk(self, n: int) -> None:
        if n < 1:
            return

        self.__init__()
        # Descrição da ListaMapeada está no início da definição de dados.
        listaDisponiveis: ListaMapeada = ListaMapeada(n)
        for i in range(n):
            self.vertices[i] = Vertice()
            self.vertices[i].cor = 'branco'
        u = 0
        self.vertices[u].cor = 'preto'
        listaDisponiveis.remove(0)
        buscarLista: bool = False

        # Tentei diminuir as desvantagens da seleção aleatória.
        #
        # Por padrão, o algoritmo gera números aleatórios e verifica se
        # o vértice já foi visitado.
        # No momento que um vértice já visitado é selecionado, a flag
        # buscarLista é ativada e o algoritmo busca um vértice na lista
        # de disponíveis.
        # Depois de buscar na lista de disponíveis, a flag volta a ser False
        # e a seleção volta a ser aleatória.
        while listaDisponiveis.lista:
            if buscarLista:
                v = listaDisponiveis.popAleatorio()
                self.addAresta(u, v)
                self.vertices[v].cor = 'preto'
                buscarLista = False
            else:
                v = random.randint(0, n - 1)
                if self.vertices[v].cor == 'branco':
                    self.addAresta(u, v)
                    self.vertices[v].cor = 'preto'
                    listaDisponiveis.remove(v)
                else:
                    buscarLista = True
            u = v

    # Gera uma árvore aleatória com n vértices usando o algoritmo de Kruskal.
    # Sobrescreve os dados da árvore anteriores à execução.
    #
    # Caso n < 1, a operação não é executada.
    #
    # Baseado no pseudocódigo dos slides.
    def randomTreeKruskal(self, n: int) -> None:
        if n < 1:
            return

        self.__init__()
        for i in range(n):
            self.vertices[i] = Vertice()

        g = GrafoAleatorio(n)
        listaArestas: List[Tuple[int, int]] = g.kruskal()

        for aresta in listaArestas:
            self.addAresta(aresta[0], aresta[1])


class GrafoAleatorio:
    # Inicializa o grafo como uma matriz de adjacência n x n.
    # Todos os vértices (u,v) = (v,u) recebem um peso aleatório [0, 1),
    # com exceção dos vértices (u, u), que recebem 1.0.
    # Assume que n > 0.
    def __init__(self, n: int) -> None:
        self.matrizAdj: List[List[float]] = [
            [1.0 for i in range(n)]for j in range(n)]

        self.numVert: int = n

        for u in range(self.numVert):
            for v in range(u+1, self.numVert):
                self.matrizAdj[u][v] = random.random()
                self.matrizAdj[v][u] = self.matrizAdj[u][v]

        for u in range(self.numVert):
            self.matrizAdj[u][u] = 1.0

    # Retorna uma lista das arestas contidas no grafo e seus pesos, com
    # exceção das arestas do tipo (u, u).
    # Para cada aresta (u, v), a entrada na lista é do tipo [w(u, v), u, v].
    def criaListaArestas(self) -> List[Tuple[int, int, int]]:
        # Como metade das arestas são repetidas, os vértices adicionados na
        # lista serão do tipo [(u, v), u < v].
        listaArestas: List[Tuple[int, int, int]] = []
        if self.matrizAdj:
            for u in range(self.numVert):
                for v in range(u+1, self.numVert):
                    listaArestas.append((self.matrizAdj[u][v], u, v))
        return listaArestas

    # Gera a árvore geradora mínima do grafo usando o algoritmo de Kruskal.
    # Retorna uma lista com as arestas da árvore.
    # Caso o grafo esteja vazio, retorna [].
    #
    # Baseado no pseudocódigo dos slides.
    def kruskal(self) -> List[Tuple[int, int]]:
        arestasMinimas: List[Tuple[int, int]] = []
        if self.matrizAdj:
            conjDisj: ConjuntoDisjunto = ConjuntoDisjunto(self.numVert)

            # Decidi criar a lista de arestas no Kruskal porque
            # ela é usada somente aqui.
            listArestas: List[Tuple[int, int, int]] = self.criaListaArestas()

            # .sort() tem complexidade O(n lg(n)), mesmo com key
            # https://en.wikipedia.org/wiki/Timsort
            # https://docs.python.org/3/howto/sorting.html
            listArestas.sort(key=lambda aresta: aresta[0])

            for aresta in listArestas:
                if conjDisj.union(aresta[1], aresta[2]) == True:
                    arestasMinimas.append((aresta[1], aresta[2]))

        return arestasMinimas


# Funções de Teste


# Executa uma série de testes para as funções implementadas.
def testesGeral():
    # Operações em Árvore
    a = Arvore()

    # Operações em árvore vazia
    assert a.diametro() == -1
    assert a.bfs(1) == (None, 0)
    assert a.isArvore() == False

    # Adição de vértices
    assert a.addVertice(1) == True
    assert a.addVertice(2) == True
    assert a.addVertice(3) == True
    assert a.addVertice(4) == True
    assert a.addVertice(1) == False         # Vértice já existe

    # Adição de arestas
    assert a.addAresta(1, 2) == True
    assert a.addAresta(1, 3) == True
    assert a.addAresta(3, 4) == True
    assert a.addAresta(1, 2) == False       # Aresta já existe
    assert a.addAresta(1, 9) == False       # Vértice 9 não existe

    # Representação da árvore
    #      4
    #      |
    #   2  3
    #    \ |
    #      1

    assert a.isArvore() == True

    a.addVertice(5)
    assert a.isArvore() == False            # 5 não está conexo à árvore

    a.addAresta(1, 5)
    assert a.isArvore() == True
    assert a.bfs(9) == (None, 0)            # Aresta 9 não existe
    assert a.bfs(1) == (4, 2)

    assert a.vertices[1].d == 0
    assert a.vertices[2].d == 1
    assert a.vertices[3].d == 1
    assert a.vertices[4].d == 2
    assert a.vertices[5].d == 1

    assert a.diametro() == 3                # Caminho de 2 ou 5 -> 4

    # Representação da árvore
    #      4
    #      |
    #   2  3  5
    #    \ | /
    #      1

    assert a.addAresta(3, 5) == True        # Cria um ciclo

    assert a.bfs(1) == (4, 2)
    assert a.isArvore() == False                 # isArvore encontra o ciclo
    assert a.diametro() == -1               # a tem um ciclo

    assert a.removeAresta(3, 5) == True     # remove uma aresta do ciclo
    assert a.addVertice(6) == True
    assert a.addAresta(5, 6) == True
    assert a.diametro() == 4                # Caminho de 4 -> 6

    # Representação da árvore
    #      4    6
    #      |   /
    #   2  3  5
    #    \ | /
    #      1

    # Operações em lista mapeada

    l = ListaMapeada(10)
    l.remove(9)
    assert len(l.lista) == 9

    x = l.popAleatorio()
    assert x >= 0 and x < 9
    assert len(l.lista) == 8

    # RandomWalk

    a.randomTreeRandomWalk(50)
    assert a.diametro() != -1

    # Operações em grafo

    g = GrafoAleatorio(10)
    assert len(g.matrizAdj) == 10
    arestasG = g.criaListaArestas()
    # Total de arestas em g é um somatório de 1 + 2 + ... + len(g)-1
    totalArestasG = 0
    for i in range(10):
        totalArestasG += i
    assert len(arestasG) == totalArestasG

    # Operações em conjunto disjunto

    conj = ConjuntoDisjunto(5)
    assert conj.union(0, 1) == True
    assert conj.pai[1] == conj.findSet(1) and conj.pai[1] == 0
    assert conj.union(2, 1) == True
    assert conj.findSet(2) == 2
    assert conj.union(0, 2) == False        # 0 e 2 estão no mesmo conjunto
    assert conj.union(3, 4) == True
    assert conj.union(1, 4) == True
    assert conj.findSet(2) == 2
    assert conj.findSet(3) == 2
    assert conj.union(2, 3) == False        # 2 e 3 estão no mesmo conjunto

    # Kruskal

    a.randomTreeKruskal(50)
    assert a.diametro() != -1


# Gera árvores aleatórias usando randomTreeRandomWalk e grava a média dos
# diâmetros dessas árvores em "randomwalk.txt".
# Para cada n em tamanhos, são geradas numExec árvores de tamanho n.
# Mostra o tempo de execução para cada tamanho n.
def testesRandomWalk(tamanhos: List[int], numExec: int) -> None:
    acumulador: float = 0
    resultado: int
    media: float
    arvore: Arvore = Arvore()
    tempoInicio: float = time.time()
    tempoExec: float

    try:
        arqRandomWalk = open("randomwalk.txt", 'w')
        print(f'Tempo de execução do Random Walk ({numExec} vezes):')
        for i in tamanhos:
            tempoExec = time.time()
            for j in range(numExec):
                arvore.randomTreeRandomWalk(i)
                resultado = arvore.diametro()
                if resultado == -1:
                    print("Erro na geração de árvore")
                    arqRandomWalk.close()
                    return
                acumulador += resultado
            media = acumulador/numExec
            arqRandomWalk.write(str(i) + ' ' + str(media) + '\n')
            acumulador = 0
            tempoExec = time.time() - tempoExec
            print(f'{i:4} Elementos: {tempoExec:.2f}s')
        print(f'Tempo Total: {time.time()-tempoInicio:.2f}s')
    finally:
        arqRandomWalk.close()


# Gera árvores aleatórias usando randomTreeKruskal e grava a média dos
# diâmetros dessas árvores em "kruskal.txt".
# Para cada n em tamanhos, são geradas numExec árvores de tamanho n.
# Mostra o tempo de execução para cada tamanho n.
def testesKruskal(tamanhos: List[int], numExec: int) -> None:
    acumulador: float = 0
    resultado: int
    media: float
    arvore: Arvore = Arvore()
    tempoInicio: float = time.time()
    tempoExec: float

    try:
        arqKruskal = open("kruskal.txt", 'w')
        print(f'Tempo de execução do kruskal ({numExec} vezes):')
        for i in tamanhos:
            tempoExec = time.time()
            for j in range(numExec):
                arvore.randomTreeKruskal(i)
                resultado = arvore.diametro()
                if resultado == -1:
                    print("Erro na geração de árvore")
                    arqKruskal.close()
                    return
                acumulador += resultado
            media = acumulador/numExec
            arqKruskal.write(str(i) + ' ' + str(media) + '\n')
            acumulador = 0
            tempoExec = time.time() - tempoExec
            print(f'{i:4} Elementos: {tempoExec:.2f}s')
        print(f'Tempo Total: {time.time()-tempoInicio:.2f}s')
    finally:
        arqKruskal.close()


# Funcão Principal


def main():
    tamanhos: List[int] = [x * 250 for x in range(1, 9)]
    # tamanhos: List[int] = [x * 250 for x in range(1, 5)]
    numExec: int = 500

    # testesRandomWalk(tamanhos, numExec)
    testesKruskal(tamanhos, numExec)

    testesGeral()

    exit


if __name__ == '__main__':
    main()
