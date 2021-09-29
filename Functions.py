from CityObject import City
import numpy as np

# Better method: Make matrix with distances (it'll look like text file). Randomly generate order of 10 ints,
# this is permutation. Those give indexes to go to, to get fitness function (the distances)


def initialize(numCities, dataFile, distancesArray, popSize, popArray):
    cityData = open(dataFile, "r")
    for i in range(numCities):
        distancesPerCity = cityData.readline()
        distancesArray.append(distancesPerCity.split())
    for j in range(popSize):
        popArray.append(np.random.permutation(numCities))


def fitnessFunction(distancesArray, cityArray):
    fitness = 0
    for i in range(len(cityArray)-1):
        fitness += int(distancesArray[cityArray[i]][cityArray[i+1]])
    return fitness

def swap(cityArray, int1, int2):
    cityArray[int1], cityArray[int2] = cityArray[int2], cityArray[int1]
