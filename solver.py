from pulp import LpProblem, LpMinimize, LpBinary, LpVariable, lpSum, getSolver, HiGHS_CMD
import sys

def intialBinsSize(bin_capacity, items):
    items.sort(reverse=True)
    bins = []

    for item in items:
        fit_found = False
        for bin in bins:
            if sum(bin) + item <= bin_capacity:
                bin.append(item)
                fit_found = True
                break
        if not fit_found:
            bins.append([item])

    return len(bins)

def ler_entradas(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        n = int(arquivo.readline())
        w = int(arquivo.readline())
        weights = []
        for linha in arquivo:
            weight = int(linha.strip())
            weights.append(weight)
        return n, w, weights
    
if len(sys.argv) < 3:
    print("Por favor, informe o nome do arquivo e o path do solver HiGHS")
    sys.exit(1)

filename = sys.argv[1]
highsPath = sys.argv[2]
hours = int(sys.argv[3]) if len(sys.argv) > 3 else 1

n,w, costs = ler_entradas(f'entradas/{filename}')
model = LpProblem("BinPacking", LpMinimize)
model.solver = getSolver('PULP_CBC_CMD')

binUpperBound = intialBinsSize(w, costs)

y = LpVariable.dicts("y", [i for i in range(binUpperBound)], cat=LpBinary)
x = LpVariable.dicts("x", [(i, j) for i in range(n) for j in range(binUpperBound)], cat=LpBinary)

model += lpSum(y[i] for i in range(binUpperBound))


#Um item só pode estar contido em uma caixa
for i in range(n):
    model += lpSum(x[i, j] for j in range(binUpperBound)) == 1
    for j in range(binUpperBound):
        model += x[i, j] <= y[j]  #Otimização. Um item só pode ser considerado num pacote caso ele tenha sido utilizado.

#A soma dos pesos dos pacotes de uma caixa não devem ultrapassar a capacidade da caixa.
for j in range(binUpperBound):
    model += lpSum(costs[i] * x[i, j] for i in range(n)) <= w*y[j]

#Os pacotes são selecionados contiguamente
for i in range(1, binUpperBound-1):
    model += y[i+1] <= y[i]


model.solve(HiGHS_CMD(timeLimit=3600*hours, logPath=f"Saídas/Solver/{filename}", path=highsPath))