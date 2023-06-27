def padronização(lista):
    máximo = max(lista)
    mínimo = min(lista)
    return list(map(lambda x: (x-mínimo)/(máximo-mínimo) if (máximo-mínimo) != 0 else 0.5,lista))