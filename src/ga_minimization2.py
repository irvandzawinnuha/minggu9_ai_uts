# Implementasi Algoritma Genetika untuk minimasi fungsi
# f(x1, x2) = - (sin(x1) * cos(x2) * tan(x1 + x2) + 3/4 * exp(1 - sqrt(x1^2)))
# Domain: -10 <= x1 <= 10, -10 <= x2 <= 10
# perhitungan fitness, seleksi (turnamen), crossover satu titik, mutasi bit-flip,
# loop evolusi antar generasi, dan keluaran akhir.

import math
import random

# Parameter-parameter Algoritma Genetika
POP_SIZE = 50      
BIT_LENGTH = 16
MAX_GENERATIONS = 100
P_CROSSOVER = 0.8
P_MUTATION = 0.01
X_MIN = -10
X_MAX = 10

CHROMOSOME_LENGTH = BIT_LENGTH * 2

# Fungsi objektif yang akan diminimumkan
def objective_function(x1, x2):
    value = - (math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + 0.75 * math.exp(1 - abs(x1)))
    return value

# Inisialisasi populasi secara acak
def initialize_population():
    population = []
    for _ in range(POP_SIZE):
        chromosome = [random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)]
        population.append(chromosome)
    return population

def decode_chromosome(chromosome):
    x1_bits = chromosome[:BIT_LENGTH]
    x2_bits = chromosome[BIT_LENGTH:]

    x1_int = 0
    x2_int = 0
    for bit in x1_bits:
        x1_int = (x1_int << 1) | bit
    for bit in x2_bits:
        x2_int = (x2_int << 1) | bit

    max_int = (1 << BIT_LENGTH) - 1
    x1 = X_MIN + (X_MAX - X_MIN) * (x1_int / max_int)
    x2 = X_MIN + (X_MAX - X_MIN) * (x2_int / max_int)
    return x1, x2

# Fungsi perhitungan fitness untuk kromosom
def calculate_fitness(chromosome):
    x1, x2 = decode_chromosome(chromosome)
    f_value = objective_function(x1, x2)
    fitness = -f_value
    return fitness

# Seleksi orangtua dengan metode Tournament Selection
def tournament_selection(population, fitnesses, tournament_size=2):
    best_index = None
    best_fitness = None

    for _ in range(tournament_size):
        i = random.randrange(0, len(population))

        if best_index is None or fitnesses[i] > best_fitness:
            best_index = i
            best_fitness = fitnesses[i]

    return population[best_index]

# Operasi crossover satu titik (one-point crossover)
def one_point_crossover(parent1, parent2):
    child1 = parent1.copy()
    child2 = parent2.copy()
    
    if random.random() < P_CROSSOVER:
        point = random.randint(1, CHROMOSOME_LENGTH - 1)

        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Operasi mutasi bit-flip
def bit_flip_mutation(chromosome):
    for j in range(CHROMOSOME_LENGTH):
        if random.random() < P_MUTATION:
            chromosome[j] = 1 - chromosome[j]
    return chromosome

# Algoritma Genetika - loop evolusi generasi
def genetic_algorithm():
    population = initialize_population()
    fitnesses = [calculate_fitness(chrom) for chrom in population]
    best_chromosome = None
    best_fitness = -float('inf')
    best_f_value = None

    for gen in range(1, MAX_GENERATIONS + 1):
        new_population = []
        while len(new_population) < POP_SIZE:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
        
            child1, child2 = one_point_crossover(parent1, parent2)
    
            child1 = bit_flip_mutation(child1)
            child2 = bit_flip_mutation(child2)
        
            new_population.append(child1)
            if len(new_population) < POP_SIZE:
                new_population.append(child2)
    
        new_population = new_population[:POP_SIZE]

        population = new_population
        fitnesses = [calculate_fitness(chrom) for chrom in population]
        for i, fit in enumerate(fitnesses):
            if fit > best_fitness:
                best_fitness = fit
                best_chromosome = population[i].copy() 
                best_f_value = -fit
    
    best_x1, best_x2 = decode_chromosome(best_chromosome)

    return best_chromosome, best_x1, best_x2, best_f_value

if __name__ == '__main__':
    best_chrom, best_x1, best_x2, best_f = genetic_algorithm()
    best_chrom_str = ''.join(str(bit) for bit in best_chrom)

    print("Kromosom terbaik:", best_chrom_str)
    print("Nilai x1 hasil decode:", best_x1)
    print("Nilai x2 hasil decode:", best_x2)
    print("Nilai f(x1, x2) minimum:", best_f)
