from Functions import *
import seaborn as sns
import scipy.stats as sp

# Need to manually set the number of cities
do_graph = True
RUN_THROUGH_AMOUNT = 30
NUMBER_OF_CITIES = 194
POP_SIZE = 101
GEN_SIZE = 2000
SELECTION_SIZE = 31
MUT_CHANCE = 70
CROSS_CHANCE = 20
MUT_TYPE = 0    # 0 for swap, 1 for shuffle
avg_fitness_array, best_fitness_array, best_at_end_swap_31, best_at_end_swap_15, best_at_end_shuffle_31, best_at_end_shuffle_15 = [], [], [], [], [], []

# Can also open a file directly containing a distance matrix using open_file_distance_matrix()
# Don't use calculate_distance() or read_coordinates_only() if doing that
# Need to stop running draw_graph() in this case due to lack of coordinates

# The boolean at end is for if it needs to skip the first spot of each line or if it needs to skip first line
coordinates = read_coordinates_only("qa194.tsp", NUMBER_OF_CITIES, True, False)
distances_matrix = calculate_distances(coordinates)
print("Distance Matrix Done")

for runthrough in range(RUN_THROUGH_AMOUNT):
    population = initialize(NUMBER_OF_CITIES, POP_SIZE)
    # Getting graph figure set up for drawing and draw the paths for a random starting permutation in the first run
    if do_graph and runthrough == 0:
        fig, axs = plt.subplots(1, 2, figsize=(12, 7))
        fig.subplots_adjust(left=0.03, bottom=0.05, right=0.97, top=0.95, wspace=0.05)
        axs[0].set_title("Random Beginning Path")
        axs[1].set_title("Best Final Path")
        draw_graph(population[0], coordinates, axs[0])  # Draw path for one of the random initial permutations
    pop_fitness = fitnessFunction(distances_matrix, population, NUMBER_OF_CITIES)
    for i in range(GEN_SIZE):
        population, avg_fitness, best_fitness, pop_fitness = generation(MUT_CHANCE, CROSS_CHANCE, SELECTION_SIZE, POP_SIZE, population, distances_matrix, NUMBER_OF_CITIES, pop_fitness, MUT_TYPE)
        avg_fitness_array.append(avg_fitness)
        best_fitness_array.append(best_fitness)
        # Showing output at 50% through each run
        if i % (GEN_SIZE * 0.5) == 0:
            print("Runthrough  " + str(runthrough) + ": " + str(int(i / GEN_SIZE * 100)) + '%')
    best_at_end_swap_31.append(min(best_fitness_array))
    # Graph the best fitness and the average fitness over the generations
    if do_graph and runthrough == 0:
        draw_graph(population[pop_fitness.index(min(best_fitness_array))], coordinates, axs[1])    # Draw best final path
    plt.figure("Swap Size 31")
    plt.title("Fitness Over Generation Using Swap 31 Selection Size")
    plt.plot(best_fitness_array)
    plt.xlabel("Generation Number")
    plt.ylabel("Fitness")
    avg_fitness_array = []
    best_fitness_array = []
# Histogram showing the best fitness after each run of the settings
sns.displot(best_at_end_swap_31).set(title="Histogram of Best Fitness Each Run with Swap amd 31 Selection Size")

print("Swap Selection Size 15")
avg_fitness_array, best_fitness_array = [], []
SELECTION_SIZE = 15
for runthrough in range(RUN_THROUGH_AMOUNT):
    population = initialize(NUMBER_OF_CITIES, POP_SIZE)
    pop_fitness = fitnessFunction(distances_matrix, population, NUMBER_OF_CITIES)
    for i in range(GEN_SIZE):
        population, avg_fitness, best_fitness, pop_fitness = generation(MUT_CHANCE, CROSS_CHANCE, SELECTION_SIZE, POP_SIZE, population, distances_matrix, NUMBER_OF_CITIES, pop_fitness, MUT_TYPE)
        avg_fitness_array.append(avg_fitness)
        best_fitness_array.append(best_fitness)
        # Showing output at 50% through each run
        if i % (GEN_SIZE * 0.5) == 0:
            print("Runthrough  " + str(runthrough) + ": " + str(int(i / GEN_SIZE * 100)) + '%')
    best_at_end_swap_15.append(min(best_fitness_array))
    plt.figure("Swap Size 15")
    plt.title("Fitness Over Generation Using Swap 15 Selection Size")
    plt.plot(best_fitness_array)
    plt.xlabel("Generation Number")
    plt.ylabel("Fitness")
    avg_fitness_array = []
    best_fitness_array = []
# Histogram showing the best fitness after each run of the settings
sns.displot(best_at_end_swap_15).set(title="Histogram of Best Fitness Each Run with Swap and 15 Selection Size")


# Does the same as above but with the shuffle mutation instead
print("Now for shuffle")
avg_fitness_array, best_fitness_array = [], []
SELECTION_SIZE = 31
MUT_TYPE = 1
for runthrough in range(RUN_THROUGH_AMOUNT):
    population = initialize(NUMBER_OF_CITIES, POP_SIZE)
    pop_fitness = fitnessFunction(distances_matrix, population, NUMBER_OF_CITIES)
    for i in range(GEN_SIZE):
        population, avg_fitness, best_fitness, pop_fitness = generation(MUT_CHANCE, CROSS_CHANCE, SELECTION_SIZE, POP_SIZE, population, distances_matrix, NUMBER_OF_CITIES, pop_fitness, MUT_TYPE)
        avg_fitness_array.append(avg_fitness)
        best_fitness_array.append(best_fitness)
        if i % (GEN_SIZE * 0.5) == 0:
            print("Runthrough  " + str(runthrough) + ": " + str(int(i / GEN_SIZE * 100)) + '%')
    best_at_end_shuffle_31.append(min(best_fitness_array))
    plt.figure("Shuffle Size 31")
    plt.title("Fitness Over Generation Using Shuffle 31 Selection Size")
    plt.plot(best_fitness_array)
    plt.xlabel("Generation Number")
    plt.ylabel("Fitness")
    avg_fitness_array = []
    best_fitness_array = []
sns.displot(best_at_end_shuffle_31).set(title="Histogram of Best Fitness Each Run with Shuffle and 31 Selection Size")

print("Shuffle Selection Size 15")
avg_fitness_array, best_fitness_array = [], []
SELECTION_SIZE = 15
for runthrough in range(RUN_THROUGH_AMOUNT):
    population = initialize(NUMBER_OF_CITIES, POP_SIZE)
    pop_fitness = fitnessFunction(distances_matrix, population, NUMBER_OF_CITIES)
    for i in range(GEN_SIZE):
        population, avg_fitness, best_fitness, pop_fitness = generation(MUT_CHANCE, CROSS_CHANCE, SELECTION_SIZE, POP_SIZE, population, distances_matrix, NUMBER_OF_CITIES, pop_fitness, MUT_TYPE)
        avg_fitness_array.append(avg_fitness)
        best_fitness_array.append(best_fitness)
        if i % (GEN_SIZE * 0.5) == 0:
            print("Runthrough  " + str(runthrough) + ": " + str(int(i / GEN_SIZE * 100)) + '%')
    best_at_end_shuffle_15.append(min(best_fitness_array))
    plt.figure("Shuffle Size 15")
    plt.title("Fitness Over Generation Using Shuffle 15 Selection Size")
    plt.plot(best_fitness_array)
    plt.xlabel("Generation Number")
    plt.ylabel("Fitness")
    avg_fitness_array = []
    best_fitness_array = []
sns.displot(best_at_end_shuffle_15).set(title="Histogram of Best Fitness Each Run with Shuffle and 15 Selection Size")

print("Information about Swap with selection size 31: " + str(sp.describe(best_at_end_swap_31)))
print("Information about Swap with selection size 15: " + str(sp.describe(best_at_end_swap_15)))
print("Information about Shuffle with selection size 31: " + str(sp.describe(best_at_end_shuffle_31)))
print("Information about Shuffle with selection size 15: " + str(sp.describe(best_at_end_shuffle_15)))
print("Mann-Whitney U test: Swap Selection Size 31 vs Selection Size 15" + str(sp.mannwhitneyu(best_at_end_swap_31, best_at_end_swap_15)))
print("Mann-Whitney U test: Shuffle Selection Size 31 vs Selection Size 15" + str(sp.mannwhitneyu(best_at_end_shuffle_31, best_at_end_shuffle_15)))
plt.show()


