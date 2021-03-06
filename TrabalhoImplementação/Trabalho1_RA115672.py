# Algoritmos em Grafos
# Trabalho 1
# Geração de árvores aleatórias usando grafos
#
# Aluno: Vinícius Kenzo Fukace
# RA: 115672

from typing import List, Dict, Tuple
from collections import deque


# Definição de Dados
#
# Por convenção, as chaves ligadas aos vértices serão do tipo int.
# Para os grafos que serão utilizados na construção das árvores, será utilizada
# matriz de adjacência, pois serão grafos completos.
# Para as árvores resultantes, será utilizada lista de adjacência.

class Vertice:
    def __init__(self) -> None:
        self.d: int = None
        self.f: int = None
        self.pai: str = None
        self.cor: str = None
        self.adj: List[int] = []


class Arvore:
    def __init__(self) -> None:
        self.vertices: Dict[int, Vertice] = {}
        tempo: int = 0
        # tempo é usado no DFS, não sei como fazer recursão passando
        # tempo por referência em python

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
        return True

    # Remove uma aresta (u, v) da árvore.
    #
    # Caso a aresta não exista, retorna False.
    # Caso contrário, remove a aresta e retorna True.
    def removeAresta(self, u: int, v: int) -> bool:
        if u in self.vertices[v].adj:
            self.vertices[v].adj.remove(u)
            self.vertices[u].adj.remove(v)
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

    # Função auxiliar de dfs().
    #
    # Baseado no pseudocódigo dos slides.
    #
    # Caso encontre um ciclo na árvore, retorna False.
    # Caso contrário, retorna True.
    def __dfsVisit(self, u: int) -> bool:
        self.tempo += 1
        resultado = True
        self.vertices[u].d = self.tempo
        self.vertices[u].cor = "cinza"

        for v in self.vertices[u].adj:
            if self.vertices[v].cor == "branco":
                self.vertices[v].pai = u
                resultado = resultado and self.__dfsVisit(v)
            elif v != self.vertices[u].pai:
                # Se o vértice não for branco e não for o pai de v,
                # ele já foi visitado antes, e forma um ciclo.
                resultado = False and self.__dfsVisit(v)

        self.vertices[u].cor = "preto"
        self.tempo += 1
        self.vertices[u].f = self.tempo
        return resultado

    # Executa a busca em profundidade na árvore, gravando o pai e os tempos de
    # descoberta e término de cada vértice.
    #
    # Baseado no pseudocódigo dos slides.
    #
    # Caso não haja vértices na árvore, retorna False.
    # Caso encontre componentes disconexos ou ciclos, retorna False.
    # Caso contrário, retorna True.
    #
    # É possível interromper a execução quando encontrar componentes disconexos
    # ou ciclos, mas decidi deixar executar o dfs por completo para manter
    # consistência nos valores das arestas do grafo.
    def dfs(self) -> bool:
        if not self.vertices:
            return False

        self.__inicializaVertices("branco")
        self.tempo = 0
        ehPrimeiraExecucao: bool = True
        flag: bool = True

        # Depois da primeira execução de dfsVisit(), todos os outros elementos
        # devem estar coloridos. Se esse não for o caso, há elementos desconexos.
        for u in self.vertices:
            if self.vertices[u].cor == "branco":
                if not ehPrimeiraExecucao:
                    flag = False
                if self.__dfsVisit(u) == False:
                    flag = False
                ehPrimeiraExecucao = False
        return flag

    # Executa a busca em largura na árvore começando no vértice s.
    # Grava o pai e a distância até s de cada vértice.
    # Retorna uma tupla com o primeiro vértice descoberto com a distância máxima
    # até s e sua distância.
    #
    # Baseado no pseudocódigo dos slides.
    #
    # Caso não exista vértice com nome s na árvore, retorna (None, 0).
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
    # Baseado no pseudocódigo dos slides.
    #
    # Caso a árvore não for conexa e acíclica, retorna -1
    # Caso a árvore não tiver vértices, retorna -1
    def diametro(self) -> int:
        if self.dfs() == False:
            return -1
        # Pega a primeira chave de self.vertices
        v = next(iter(self.vertices))
        a = self.bfs(v)
        return self.bfs(a[0])[1]


class Grafo:
    def __init__(self, n) -> None:
        self.matrizAdj = [[-1 for i in range(n)] for j in range(n)]


def main():
    a = Arvore()

    # Operações em árvore vazio
    assert a.diametro() == -1
    assert a.bfs(1) == (None, 0)
    assert a.dfs() == False

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

    assert a.dfs() == True

    a.addVertice(5)
    assert a.dfs() == False                 # 5 não está conexo à árvore

    a.addAresta(1, 5)
    assert a.dfs() == True
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
    assert a.dfs() == False                 # dfs encontra o ciclo
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

    exit


if __name__ == '__main__':
    main()
