# Encontrar o valor máximo e mínimo de um arranjo não vazio por divisão e conquista

# 1- Escrever o algoritmo
# 2- Obter a recorrência com o número de comparações
# 3- Resolver a recorrência e obter o número de comparações

def max_min(v, a: int, b: int) -> (int, int):
    if(a == b):
        return v[a], v[a]
    else:
        meio = (a+b)//2
        i, j = max_min(v, a, meio)
        k, l = max_min(v, meio+1, b)
        return max(i, k), min(j, l)


x, y = max_min([1, 2, 3, 4, 5, 6, 7, 8], 0, 7)
print(x, y)

x, y = max_min([1, 2], 0, 1)
print(x, y)

x, y = max_min([1], 0, 0)
print(x, y)

x, y = max_min("abacaxi", 0, 6)
print(x, y)
