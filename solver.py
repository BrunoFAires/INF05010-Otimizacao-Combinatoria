import pulp

def ler_entradas(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        n = int(arquivo.readline())
        w = int(arquivo.readline())
        weights = []
        for linha in arquivo:
            weight = int(linha.strip())
            weights.append(weight)
        return n, w, weights

n,w, costs = ler_entradas('entradas/N1W1B1R0.txt')

model = pulp.LpProblem("BinPacking", pulp.LpMinimize)

y = pulp.LpVariable.dicts("y", [i for i in range(n)], cat=pulp.LpBinary)
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(n) for j in range(n)], cat=pulp.LpBinary)

model += pulp.lpSum(y[i] for i in range(n))


for i in range(n):
        model += pulp.lpSum(x[i, j] for j in range(n)) == 1

for j in range(n):
    model += pulp.lpSum(costs[i] * x[i, j] for i in range(n)) <= w*y[j]


model.solve()
print(model.status)


print(f"Custo Total: {pulp.value(model.objective.value())}")
