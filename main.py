# Need to do functions for calculating total distance (fitness) and also doing crossover
# Need to set up so there's multiple permutations and generations
# Need selection too?
from Functions import *
from CityObject import City
NUMBER_OF_CITIES = 15
POP_SIZE = 10
GEN_SIZE = 10
SELECTION_SIZE = 5
MUT_CHANCE = 0.8
CROSS_CHANCE = 0.1


distancesArray = []
popArray = []
fitArray = []

initialize(NUMBER_OF_CITIES, "Sample Cities (Size 15).txt", distancesArray, POP_SIZE, popArray)
print(distancesArray)
print(popArray)
swap(popArray[0], 0, 1)
print(popArray[0])
for i in range(POP_SIZE):
    fitArray.append(fitnessFunction(distancesArray, popArray[i]))
print(fitArray)


