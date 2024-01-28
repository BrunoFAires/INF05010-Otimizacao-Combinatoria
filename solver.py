from pulp import pulp, LpProblem, LpMinimize, PULP_CBC_CMD, LpBinary, LpVariable, lpSum, value, getSolver, HiGHS, HiGHS_CMD

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

filenames = ["N1W1B1R0.txt", "Falkenauer_t60_00.txt", "BPP_100_150_0.1_0.7_0.txt", "Hard28_BPP645.txt", "402_10000_DI_18.txt", "BPP_500_300_0.2_0.8_6.txt", "Falkenauer_u1000_00.txt",  "1002_80000_NR_27.txt"]

for filename in filenames:

    n,w, costs = ler_entradas(f'entradas/{filename}')
    model = LpProblem("BinPacking", LpMinimize)
    model.solver = getSolver('PULP_CBC_CMD')

    binUpperBound = intialBinsSize(w, costs)

    y = LpVariable.dicts("y", [i for i in range(binUpperBound)], cat=LpBinary)
    x = LpVariable.dicts("x", [(i, j) for i in range(n) for j in range(binUpperBound)], cat=LpBinary)

    model += lpSum(y[i] for i in range(binUpperBound))


    for i in range(n):
            model += lpSum(x[i, j] for j in range(binUpperBound)) == 1

    for j in range(binUpperBound):
        model += lpSum(costs[i] * x[i, j] for i in range(n)) <= w*y[j]

    for i in range(1, binUpperBound-1):
        model += y[i+1] <= y[i]

    model.solve(HiGHS_CMD(timeLimit=3600, logPath=f"Saídas/Solver/{filename}", path="../HiGHS/build/bin/highs"))