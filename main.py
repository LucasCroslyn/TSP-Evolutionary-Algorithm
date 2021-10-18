from Functions import *
import seaborn as sns
import scipy.stats as sp
import matplotlib.pyplot as plt

do_graph = True
RUN_THROUGH_AMOUNT = 1
NUMBER_OF_CITIES = 400  # Need to manually set the number of cities
GEN_SIZE = 3500
SELECTION_SIZE = 20
MUT_CHANCE = 60
CROSS_CHANCE = 10
MUT_TYPE = 0    # 0 for swap, 1 for shuffle
ADDITIONAL_POP = False  # False for no chance of additional population through generations, True for the chance.
# It will be a 1% chance to generate 20 random permutations to add to population increasing capacity
# Starting population amount is found below in the first for loop, it may be moved out if not doing additional population

# Can also open a file directly containing a distance matrix using open_file_distance_matrix()
# Don't use calculate_distance() or read_coordinates_only() if doing that
# Need to stop running draw_graph() in this case due to lack of coordinates

# The booleans at end is for if it needs to skip the first spot of each line, in this code skip if city num or name is given (first boolean) or if it needs to skip first line (second boolean)
coordinates = read_coordinates_only("Competition.cords", NUMBER_OF_CITIES, True, False)
distances_matrix = calculate_distances(coordinates)
print("Distance Matrix Done")

best_fitness_array = []
best_at_end = []
best_pops = []
for runthrough in range(RUN_THROUGH_AMOUNT):
    POP_SIZE = 121  # Here in case the additional population parameter is turned on
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
        population, best_fitness, pop_fitness = generation(MUT_CHANCE, CROSS_CHANCE, SELECTION_SIZE, POP_SIZE, population, distances_matrix, NUMBER_OF_CITIES, pop_fitness, MUT_TYPE, ADDITIONAL_POP)
        best_fitness_array.append(best_fitness)
        # Showing output at 50% through each run
        if i % (GEN_SIZE * 0.1) == 0:
            print("Runthrough  " + str(runthrough) + ": " + str(int(i / GEN_SIZE * 100)) + '%')
    best_at_end.append(min(best_fitness_array))
    # Graph the best fitness and the average fitness over the generations
    if do_graph and runthrough == 0:
        draw_graph(population[pop_fitness.index(min(best_fitness_array))], coordinates, axs[1])    # Draw best final path
    # plt.figure("Swap No Additional Population")
    # plt.title("Fitness Over Generation")
    # plt.plot(best_fitness_array)
    # plt.xlabel("Generation Number")
    # plt.ylabel("Fitness")
    best_pops.append(population[pop_fitness.index(best_fitness)])
    best_fitness_array = []
# Histogram showing the best fitness after each run of the settings
#sns.displot(best_at_end).set(title="Histogram of Best Fitness Each Run")
print(min(best_at_end))
print(best_pops[best_at_end.index(min(best_at_end))])
plt.show()