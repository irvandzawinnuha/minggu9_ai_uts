import random
import math

# Parameter dasar
BITS_PER_VAR = 16
CHROM_LENGTH = BITS_PER_VAR * 2
MIN_X, MAX_X = -10, 10
POP_SIZE = 50
GENERATIONS = 100
CROSSOVER_RATE = 0.9
MUTATION_RATE = 1 / CHROM_LENGTH
TOURNAMENT_SIZE = 3

# Fungsi decode biner ke nilai real
def decode_gene(binary_str, min_val, max_val):
    integer_value = int(binary_str, 2)
    max_int = (1 << len(binary_str)) - 1
    real_value = min_val + (max_val - min_val) * (integer_value / max_int)
    return real_value

# Fungsi objektif
def objective_function(x1, x2):
    try:
        return -(math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + 0.75 * math.exp(1 - abs(x1)))
    except:
        return float('inf')  # handle nilai tan yang tidak terdefinisi

# Mutasi bit-flip
def mutate_bitstring(bitstring):
    bits = list(bitstring)
    for i in range(len(bits)):
        if random.random() < MUTATION_RATE:
            bits[i] = '1' if bits[i] == '0' else '0'
    return ''.join(bits)

# Seleksi turnamen
def tournament_select(population, fitness_values):
    candidates = random.sample(list(zip(population, fitness_values)), TOURNAMENT_SIZE)
    winner = max(candidates, key=lambda item: item[1])
    return winner[0]

# One-point crossover
def crossover(p1, p2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, CHROM_LENGTH - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    else:
        return p1, p2

# Inisialisasi populasi awal
population = [''.join(random.choice('01') for _ in range(CHROM_LENGTH)) for _ in range(POP_SIZE)]
best_chrom, best_fval, best_decoded = None, float('inf'), (None, None)

# Proses evolusi
for gen in range(GENERATIONS):
    fitness_values = []
    for chrom in population:
        x1 = decode_gene(chrom[:BITS_PER_VAR], MIN_X, MAX_X)
        x2 = decode_gene(chrom[BITS_PER_VAR:], MIN_X, MAX_X)
        fval = objective_function(x1, x2)
        fitness = -fval
        fitness_values.append(fitness)

        if fval < best_fval:
            best_fval = fval
            best_chrom = chrom
            best_decoded = (x1, x2)

    new_population = []
    while len(new_population) < POP_SIZE:
        p1 = tournament_select(population, fitness_values)
        p2 = tournament_select(population, fitness_values)
        c1, c2 = crossover(p1, p2)
        c1, c2 = mutate_bitstring(c1), mutate_bitstring(c2)
        new_population.extend([c1, c2])

    population = new_population[:POP_SIZE]

    if (gen + 1) % 10 == 0:
        print(f"Generasi {gen+1} - Nilai terbaik: {best_fval:.5f}")

# Tampilkan hasil terbaik
print("\n=== Hasil Terbaik ===")
print(f"Kromosom terbaik: {best_chrom}")
print(f"x1 = {best_decoded[0]:.5f}, x2 = {best_decoded[1]:.5f}")
print(f"f(x1,x2) = {best_fval:.5f}")
