# Need to do functions for calculating total distance (fitness) and also doing crossover
# Need to set up so there's multiple permutations and generations
# Need selection too?
from Functions import *
import matplotlib.pyplot as plt

NUMBER_OF_CITIES = 15
POP_SIZE = 100
GEN_SIZE = 100
SELECTION_SIZE = 5
MUT_CHANCE = 80
CROSS_CHANCE = 15


distancesArray = []
popArray = []

initialize(NUMBER_OF_CITIES, "Sample Cities (Size 15).txt", distancesArray, POP_SIZE, popArray)
#print(distancesArray)
#print(popArray)
#swap(popArray[0], 0, 1)
#print(popArray[0])
#print(fitArray)
#print(selection(SELECTION_SIZE, popArray, distancesArray))
#print(popArray[0])
#print(popArray[1])

#[cityArray1[min(indexes):max(indexes)].tolist(), cityArray2[min[indexes]:max(indexes)].tolist()]
#print([popArray[0][0:2].tolist(), popArray[1][0:2].tolist()])
#newPop = crossover(popArray[0], popArray[1])
#print(newPop)
#print(popArray)
avgFitnesses = []
for i in range(GEN_SIZE):
    popArray, avgFitness =  generation(MUT_CHANCE, CROSS_CHANCE, SELECTION_SIZE, POP_SIZE, popArray, distancesArray)
    avgFitnesses.append(avgFitness)
#print(avgFitnesses)
#print(statistics.mean(avgFitnesses))
plt.hist(avgFitnesses)
