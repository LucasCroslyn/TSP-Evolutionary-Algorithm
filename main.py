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

distancesArray = []
popArray = []
avgFitnesses = []
bestFitnesses = []
maxFitnesses = []
initialize(NUMBER_OF_CITIES, "Sample Cities (Size 15).txt", distancesArray, POP_SIZE, popArray)
for i in range(GEN_SIZE):
    popArray, avgFitness, bestFitness, maxFitness = generation(MUT_CHANCE, CROSS_CHANCE, SELECTION_SIZE, POP_SIZE, popArray, distancesArray, NUMBER_OF_CITIES)
    avgFitnesses.append(avgFitness)
    bestFitnesses.append(bestFitness)
    maxFitnesses.append(maxFitness)
print(bestFitnesses)
#sns.displot(avgFitnesses, kind="kde", bw_adjust=0.25)
sns.displot(bestFitnesses, kind="kde", bw_adjust=0.25)
#sns.displot(maxFitnesses, kind="kde", bw_adjust=0.25)
plt.show()


