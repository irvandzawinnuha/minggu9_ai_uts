# Implementasi Algoritma Genetika (GA) untuk minimasi fungsi
# f(x1, x2) = - (sin(x1) * cos(x2) * tan(x1 + x2) + 3/4 * exp(1 - sqrt(x1^2)))
# Domain: -10 <= x1 <= 10, -10 <= x2 <= 10
# Seluruh proses GA diimplementasikan manual tanpa library khusus GA.
# Termasuk: inisialisasi populasi, representasi kromosom biner & decode, 
# perhitungan fitness, seleksi (turnamen), crossover satu titik, mutasi bit-flip,
# loop evolusi antar generasi, dan keluaran akhir.
# Komentar ditulis dalam Bahasa Indonesia sesuai poin penilaian UTS.

import math
import random

# Parameter-parameter GA
POP_SIZE = 50         # Ukuran populasi (jumlah individu/kromosom dalam populasi)
BIT_LENGTH = 16       # Jumlah bit untuk representasi masing-masing variabel (presisi encoding)
MAX_GENERATIONS = 100 # Jumlah generasi (iterasi evolusi) maksimum
P_CROSSOVER = 0.8     # Probabilitas terjadinya crossover pada pasangan orangtua
P_MUTATION = 0.01     # Probabilitas mutasi per bit
X_MIN = -10           # Batas bawah domain pencarian untuk x1 dan x2
X_MAX = 10            # Batas atas domain pencarian untuk x1 dan x2

# Panjang kromosom dalam bit (menggabungkan representasi x1 dan x2)
CHROMOSOME_LENGTH = BIT_LENGTH * 2

# Fungsi objektif yang akan diminimumkan
def objective_function(x1, x2):
    """Menghitung nilai fungsi f(x1, x2) sesuai definisi persoalan."""
    # f(x1, x2) = - (sin(x1)*cos(x2)*tan(x1+x2) + 3/4 * exp(1 - |x1|))
    value = - (math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + 0.75 * math.exp(1 - abs(x1)))
    return value

# Inisialisasi populasi secara acak
def initialize_population():
    """Membuat populasi awal dengan kromosom acak berukuran POP_SIZE."""
    population = []
    for _ in range(POP_SIZE):
        # Membuat kromosom acak berupa list bit (0/1) sepanjang CHROMOSOME_LENGTH
        chromosome = [random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)]
        population.append(chromosome)
    return population

# Fungsi decode kromosom biner menjadi pasangan nilai real (x1, x2)
def decode_chromosome(chromosome):
    """Mengubah representasi biner kromosom menjadi nilai x1 dan x2 dalam domain aslinya."""
    # Membagi kromosom menjadi dua bagian: untuk x1 dan x2
    x1_bits = chromosome[:BIT_LENGTH]
    x2_bits = chromosome[BIT_LENGTH:]
    # Konversi bit-bit menjadi bilangan integer untuk x1 dan x2
    x1_int = 0
    x2_int = 0
    for bit in x1_bits:
        x1_int = (x1_int << 1) | bit  # geser ke kiri lalu tambahkan bit (membangun bilangan dari bit)
    for bit in x2_bits:
        x2_int = (x2_int << 1) | bit
    # Nilai maksimum integer yang dapat direpresentasikan dengan BIT_LENGTH bit
    max_int = (1 << BIT_LENGTH) - 1  # 2^BIT_LENGTH - 1
    # Mapping linear dari integer ke rentang [X_MIN, X_MAX]
    x1 = X_MIN + (X_MAX - X_MIN) * (x1_int / max_int)
    x2 = X_MIN + (X_MAX - X_MIN) * (x2_int / max_int)
    return x1, x2

# Fungsi perhitungan fitness untuk kromosom
def calculate_fitness(chromosome):
    """Menghitung nilai fitness untuk satu kromosom. 
    Karena kita melakukan minimasi fungsi, fitness didefinisikan sebagai negatif dari nilai fungsi (agar minimasi f setara dengan memaksimalkan fitness)."""
    # Decode kromosom menjadi nilai x1 dan x2
    x1, x2 = decode_chromosome(chromosome)
    # Hitung nilai fungsi objektif f(x1, x2)
    f_value = objective_function(x1, x2)
    # Karena yang dicari adalah minimum f, maka untuk fitness (yang akan dimaksimalkan GA) digunakan -f_value
    fitness = -f_value
    return fitness

# Seleksi orangtua dengan metode Tournament Selection
def tournament_selection(population, fitnesses, tournament_size=2):
    """Memilih satu individu (kromosom) dari population menggunakan tournament selection.
    Beberapa individu dipilih acak (ukuran turnamen), lalu yang terbaik (fitness tertinggi) di antara mereka terpilih."""
    best_index = None
    best_fitness = None
    # Memilih 'tournament_size' individu secara acak
    for _ in range(tournament_size):
        i = random.randrange(0, len(population))  # indeks individu acak
        # Cek apakah individu ini lebih baik dari kandidat sebelumnya
        if best_index is None or fitnesses[i] > best_fitness:
            best_index = i
            best_fitness = fitnesses[i]
    # Kembalikan individu (kromosom) dengan fitness terbaik dari turnamen
    return population[best_index]

# Operasi crossover satu titik (one-point crossover)
def one_point_crossover(parent1, parent2):
    """Melakukan operasi crossover satu titik pada dua parent untuk menghasilkan dua child."""
    # Inisialisasi child sebagai salinan parent (jika tidak terjadi crossover, anak sama dengan orangtua)
    child1 = parent1.copy()
    child2 = parent2.copy()
    # Lakukan crossover dengan probabilitas P_CROSSOVER
    if random.random() < P_CROSSOVER:
        # Pilih titik crossover secara acak (antara 1 hingga length-1, agar kedua segmen tidak kosong)
        point = random.randint(1, CHROMOSOME_LENGTH - 1)
        # Membentuk child dengan menukar bagian setelah titik crossover
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Operasi mutasi bit-flip
def bit_flip_mutation(chromosome):
    """Melakukan mutasi pada kromosom dengan membalik setiap bit dengan probabilitas P_MUTATION."""
    for j in range(CHROMOSOME_LENGTH):
        # Setiap bit memiliki peluang P_MUTATION untuk dibalik (0 -> 1 atau 1 -> 0)
        if random.random() < P_MUTATION:
            chromosome[j] = 1 - chromosome[j]
    return chromosome

# Algoritma Genetika - loop evolusi generasi
def genetic_algorithm():
    """Menjalankan proses evolusi GA hingga mencapai generasi maksimum.
    Mengembalikan kromosom terbaik yang ditemukan beserta nilai decode x1, x2 dan nilai f terbaik."""
    # Inisialisasi populasi awal
    population = initialize_population()
    # Hitung fitness awal populasi
    fitnesses = [calculate_fitness(chrom) for chrom in population]
    # Inisialisasi pencatatan solusi terbaik
    best_chromosome = None
    best_fitness = -float('inf')  # fitness sangat kecil sebagai pembanding awal
    best_f_value = None

    # Loop evolusi generasi
    for gen in range(1, MAX_GENERATIONS + 1):
        # Membentuk populasi baru (next generation)
        new_population = []
        # **Optional**: Elitisme - mempertahankan individu terbaik (dapat diaktifkan jika diinginkan)
        # Contoh: jika elitism, lakukan:
        # if best_chromosome is not None:
        #     new_population.append(best_chromosome.copy())
        # lalu lanjutkan pengisian new_population mulai dari individu ke-2.
        
        # Isi populasi baru hingga ukuran POP_SIZE
        while len(new_population) < POP_SIZE:
            # Seleksi dua orangtua menggunakan turnamen
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            # Crossover untuk menghasilkan dua anak
            child1, child2 = one_point_crossover(parent1, parent2)
            # Mutasi pada kedua anak
            child1 = bit_flip_mutation(child1)
            child2 = bit_flip_mutation(child2)
            # Tambahkan anak ke populasi baru
            new_population.append(child1)
            if len(new_population) < POP_SIZE:
                # Jika masih ada slot, tambahkan anak kedua
                new_population.append(child2)
        # Jika ukuran populasi baru melebihi POP_SIZE (misal POP_SIZE ganjil), potong list ke ukuran POP_SIZE
        new_population = new_population[:POP_SIZE]

        # Pergantian generasi: populasi lama digantikan populasi baru
        population = new_population
        # Hitung fitness populasi baru
        fitnesses = [calculate_fitness(chrom) for chrom in population]
        # Update solusi terbaik jika ada individu dengan fitness lebih tinggi (f lebih rendah)
        for i, fit in enumerate(fitnesses):
            if fit > best_fitness:
                best_fitness = fit
                best_chromosome = population[i].copy()  # simpan salinan kromosom terbaik
                best_f_value = -fit  # nilai f sebenarnya (ingat fit = -f)
        # (Opsional) Cetak info generasi, misal setiap 10 generasi:
        # if gen % 10 == 0:
        #     print(f"Generasi {gen} - best f: {best_f_value}")
    
    # Setelah evolusi selesai, decode kromosom terbaik
    best_x1, best_x2 = decode_chromosome(best_chromosome)
    # Kembalikan hasil terbaik
    return best_chromosome, best_x1, best_x2, best_f_value

# Jalankan algoritma genetika dan tampilkan hasil akhirnya
if __name__ == '__main__':
    best_chrom, best_x1, best_x2, best_f = genetic_algorithm()
    # Ubah kromosom terbaik (list bit) menjadi string untuk output
    best_chrom_str = ''.join(str(bit) for bit in best_chrom)
    # Tampilkan kromosom terbaik dan hasil decode-nya
    print("Kromosom terbaik:", best_chrom_str)
    print("Nilai x1 hasil decode:", best_x1)
    print("Nilai x2 hasil decode:", best_x2)
    print("Nilai f(x1, x2) minimum:", best_f)
