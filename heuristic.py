import copy
import random
import math
import time


def first_fit_decreasing(bin_capacity, items):
    items.sort(reverse=True)
    bins = []
    
    for item in items:
        """ fit_found = False
        for bin in bins:
            if sum(bin) + item <= bin_capacity:
                bin.append(item)
                fit_found = True
                break
        if not fit_found:
            bins.append([item]) """
        bins.append([item])

    return bins

def read_input(file_name):
    with open(file_name, 'r') as file:
        n = int(file.readline())
        capaity = int(file.readline())
        weights = []
        for line in file:
            weight = int(line.strip())
            weights.append(weight)
        return n, capaity, weights
    
n, capacity, weights = read_input('entradas/BPP_100_150_0.1_0.7_0.txt')

def swap_items(bins):
    current_bins = remove_empty_sub_lists(copy.deepcopy(bins))
    origin_sublist = random.randint(0, len(current_bins)-1)
    sublista_destino = random.randint(0, len(current_bins)-1)
    
    if not origin_sublist or not sublista_destino:
        return current_bins 

    indice_elemento_1 = random.randint(0, len(current_bins[origin_sublist])-1)
    indice_elemento_2 = random.randint(0, len(current_bins[sublista_destino])-1)

    current_bins[sublista_destino][indice_elemento_2],  current_bins[origin_sublist][indice_elemento_1]  = current_bins[origin_sublist][indice_elemento_1], current_bins[sublista_destino][indice_elemento_2]



    return current_bins

def swap_item(bins):
    current_bins = copy.deepcopy(bins)

    origin_sublist = random.choice(current_bins)
    
    if not origin_sublist:
        return current_bins 

    element_index = random.randint(0, len(origin_sublist)-1)

    element = origin_sublist.pop(element_index)

    destination_sublist = random.choice(current_bins)

    destination_sublist.append(element)

    return current_bins

def remove_empty_sub_lists(list):
    return [sub_list for sub_list in list if sub_list]

def cost(bins):
    total =  0
    for bin in bins:
        if bin != []:
            total+=1
    return total

def valid_solution(bins, max_weight): 
    for bin in bins:
        wT = 0
        for w in bin:
            wT+=w
        if wT > max_weight:
            return False
    return True
#TODO corrigir vizinhança.
def metropolis_algorithm(current_solution, max_weight, initial_temperature, temperature, max_iterations):
    b = copy.deepcopy(current_solution)
    for _ in range(max_iterations):
        new_solution = copy.deepcopy(b)

        if((temperature/initial_temperature) < 0.40):
            new_solution = swap_items(new_solution)
        else:
            new_solution = swap_item(new_solution)
        
        
        current_cost = cost(b)
        new_cost = cost(new_solution)  if valid_solution(new_solution, max_weight) else cost(new_solution) + 1000

        cost_difference = new_cost - current_cost
        a = random.random()
        

        if ((cost_difference < 0) == True or (a < math.exp(-cost_difference / temperature)) == True):
            b.clear()
            b = [row[:] for row in new_solution]
        
        
    return b


def simulated_annealing(initial_solution, max_weight, max_iterations, initial_temperature, cooling_rate):
    init = time.perf_counter()
    current_solution = copy.deepcopy(initial_solution)
    current_cost = cost(initial_solution)
    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost
    final_temperature = 0.1

    temperature = initial_temperature
    
    while temperature >= final_temperature:
        #Gera uma nova solução a partir do metrópolis
        current_solution = metropolis_algorithm(best_solution, max_weight, initial_temperature, temperature, max_iterations)
        current_cost = cost(current_solution)

        # Atualiza a melhor solução
        if current_cost < best_cost and valid_solution(current_solution, max_weight):
            best_solution = copy.deepcopy(current_solution)
            best_cost = current_cost

        #Diminui a temperatura
        temperature *= cooling_rate

    result = time.perf_counter() - init
    return remove_empty_sub_lists(best_solution), best_cost, result

bins = first_fit_decreasing(capacity, weights)

max_iterations = 1000

initial_temperature = 1000.0 
cooling_rate = 0.95

print(bins)
print(cost(bins))
print(valid_solution(bins, capacity))

solution, best_cost, time = simulated_annealing(bins, capacity,  max_iterations, initial_temperature, cooling_rate)

print(solution)
print(valid_solution(solution, capacity))

print(best_cost)
print(time)