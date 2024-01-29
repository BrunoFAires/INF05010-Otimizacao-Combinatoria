# Resolução do problema de empacotamento binário utilizando formulação inteira e Simulated Annealing.
## Definição
Considere n itens, cada um com um respectivo peso, e C sendo a capacidade máxima de caixasque serão utilizadas. Deseja-se minimizar o número de caixas necessárias para encaixotar todos os itens de maneira que o peso dos itens presentes em uma caixa não extrapole a capacidade C da caixa.
## Formulação inteira
A implementação da formulação inteira foi criada utilizando a biblioteca de formulação lieanr PuLP com a linguagem Python. Em relação ao solver, estamos utilizando o HiGHS.</br></br>
Antes de executar o arquivo solver.py para a formulação inteira, deve-se instalar o solucionador HiGHS. O processo de instalação pode ser encontrado em: https://github.com/ERGO-Code/HiGHS
### Execução
A execução da formulação inteira dá-se por:</br>
```
python solver.py fileName highsPath hours 
```
</br>
<b>Onde: </b><br>
fileName: Nome de uma instância contida na pasta "entradas".<br>
highsPath: Path onde está localizado o arquivo binário do solucionador Highs.<br>
hours (default = 1): Tempo limite do solver em horas.<br></br>
Exemplos:<br>

```
python solver.py N1W1B1R0.txt ../HiGHS/build/bin/highs
```
<br>

```
python solver.py N1W1B1R0.txt ../HiGHS/build/bin/highs 2
```

## Meta-heurística
O Simulated Annealing é um algoritmo que utiliza uma abordagem inspirada no recozimento de materiais. Ele simula variações de temperatura no sistema para encontrar um mínimo local da função objetivo. O algoritmo também permite escapar de mínimos locais ao aceitar soluções localmente piores com base em uma probabilidade de aceitação, calculada usando a fórmula 𝑒^(-Δ𝑆/𝑘𝑇), onde Δ𝑆 é a diferença entre a nova solução proposta e a solução atual, k é uma constante positiva e T é a temperatura atual do sistema, À medida que o algoritmo progride em busca do mínimo global, a temperatura do sistema diminui, reduzindo a probabilidade de aceitar soluções piores.<br><br>
	A decisão de aceitar ou rejeitar uma nova solução é baseada em duas condições: se ela reduz o valor da função objetivo ou se é aceita conforme a probabilidade definida anteriormente.<br><br>
	Além disso, o critério de parada do algoritmo é determinado com base na temperatura inicial, temperatura final e um fator de resfriamento entre 0 e 1. O algoritmo itera até que a temperatura do sistema seja menor que a temperatura final, sendo que a temperatura é reduzida multiplicativamente pelo fator de resfriamento ao final de cada iteração.
### Execução
A execução da meta-heurística dá-se por:</br>
```
python3 heuristic.py maxInterations initialTemperature coolingRate fileName randomSeed
```
</br>
<b>Onde:</b><br>
maxInterations: Máximo de iterações que o algoritmo de metrópolis irá executar.<br>
initialTemperature: Temperatura inicial considerado no Simulated Annealing<br>
coolingRate: Taxa de resfriamento do Simulated Annealing<br>
fileName: Nome de uma instância contida na pasta "entradas".<br>
randomSeed: Semente de aleatoriedade<br></br>
Exemplos:<br>

```
python3 heuristic.py 1000 1500 0.90 N1W1B1R0.txt 0
```
<br>

```
python3 heuristic.py 1000 1000 0.95 N1W1B1R0.txt 10
```
