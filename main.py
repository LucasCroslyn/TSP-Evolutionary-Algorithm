# Need to do functions for calculating total distance (fitness) and also doing crossover
# Need to set up so there's multiple permutations and generations
# Need selection too?
import matplotlib.pyplot as plt

from Functions import *
from TimeWindowFunctions import *
import seaborn as sns


NUMBER_OF_CITIES = 21
POP_SIZE = 21
GEN_SIZE = 500
SELECTION_SIZE = 4
MUT_CHANCE = 60
CROSS_CHANCE = 10
population, avg_fitness_array, best_fitness_array, max_fitness_array = [], [], [], []


initialize(NUMBER_OF_CITIES, POP_SIZE, population)
coordinates, ready_times, due_times = TW_read_data("Cities with Time Windows and Coordinates(Size 21).txt", NUMBER_OF_CITIES)
distances_matrix = calculate_distances(coordinates)
print(distances_matrix)
# Getting graph figure set up for drawing
fig, axs = plt.subplots(1, 2, figsize=(12, 7))
fig.subplots_adjust(left=0.03, bottom=0.05, right=0.97, top=0.95, wspace=0.05)
axs[0].set_title("Random Beginning Path")
axs[1].set_title("Best Final Path")
draw_graph(population[0], coordinates, axs[0])     # Draw path for one of the random initial permutations
pop_fitness = fitnessFunction(distances_matrix, population, NUMBER_OF_CITIES)
for i in range(GEN_SIZE):
    population, avg_fitness, best_fitness, max_fitness, pop_fitness = generation(MUT_CHANCE, CROSS_CHANCE, SELECTION_SIZE, POP_SIZE, population, distances_matrix, NUMBER_OF_CITIES, pop_fitness)
    avg_fitness_array.append(avg_fitness)
    best_fitness_array.append(best_fitness)
    max_fitness_array.append(max_fitness)
draw_graph(population[pop_fitness.index(best_fitness)], coordinates, axs[1])    # Draw best final path
#plt.show()
print(avg_fitness_array)
figure2 = plt.figure(2)
plt.plot(best_fitness_array)
plt.plot(avg_fitness_array)
plt.plot(max_fitness_array)
plt.xlabel("Generation Number")
plt.ylabel("Fitness")
plt.show()
# sns.displot(avg_fitness_array, kind="kde", bw_adjust=0.25)
# sns.displot(best_fitness_array, kind="kde", bw_adjust=0.25)
# sns.displot(max_fitness_array, kind="kde", bw_adjust=0.25)


