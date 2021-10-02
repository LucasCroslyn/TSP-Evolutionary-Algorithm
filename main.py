# Need to do functions for calculating total distance (fitness) and also doing crossover
# Need to set up so there's multiple permutations and generations
# Need selection too?
from Functions import *
import matplotlib.pyplot as plt
import seaborn as sns

NUMBER_OF_CITIES = 15
POP_SIZE = 201
GEN_SIZE = 300
SELECTION_SIZE = 50
MUT_CHANCE = 60
CROSS_CHANCE = 10

distances_matrix = []
population = []
avg_fitness_array = []
best_fitness_array = []
max_fitness_array = []
initialize(NUMBER_OF_CITIES, "Sample Cities (Size 15).txt", distances_matrix, POP_SIZE, population)
for i in range(GEN_SIZE):
    population, avg_fitness, best_fitness, max_fitness = generation(MUT_CHANCE, CROSS_CHANCE, SELECTION_SIZE, POP_SIZE, population, distances_matrix, NUMBER_OF_CITIES)
    avg_fitness_array.append(avg_fitness)
    best_fitness_array.append(best_fitness)
    max_fitness_array.append(max_fitness)
print(best_fitness_array)
#sns.displot(avg_fitness_array, kind="kde", bw_adjust=0.25)
sns.displot(best_fitness_array, kind="kde", bw_adjust=0.25)
#sns.displot(max_fitness_array, kind="kde", bw_adjust=0.25)
plt.show()


