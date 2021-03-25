v = [1, 2, 3, 4, 5, 6]
#    0,1,2,3,4,5
tam = len(v)

# a incios
# b final
# 0<=a <= b <= len(v)


def busca(v, n: int, a: int, b: int):
    if b == a:
        return False
    elif v[(b+a)//2] > n:
        return busca(v, n, a, (b+a)//2)
    elif v[(b+a)//2] < n:
        return busca(v, n, (b+a)//2+1, b)
    else:
        return True


assert busca(v, 1, 0, tam) == True
assert busca(v, 7, 0, tam) == False
assert busca(v, 3, 0, tam) == True
assert busca(v, 4, 0, tam) == True
assert busca(v, 5, 0, tam) == True
assert busca(v, 6, 0, tam) == True

print("Recursivo Completo")


def buscai(v, n: int, a: int, b: int):
    while b != a:
        if v[(b + a) // 2] > n:
            b = (b+a)//2
        elif v[(b + a) // 2] < n:
            a = (b + a) // 2 + 1
        else:
            return True
    return False


assert buscai(v, 1, 0, tam) == True
assert buscai(v, 7, 0, tam) == False
assert buscai(v, 3, 0, tam) == True
assert buscai(v, 4, 0, tam) == True
assert buscai(v, 5, 0, tam) == True
assert buscai(v, 6, 0, tam) == True

print("Iterativo Completo")
