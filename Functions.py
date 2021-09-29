from CityObject import City
import numpy as np
import random

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
    fitness += int(distancesArray[cityArray[i+1]][cityArray[0]])
    return fitness


def swap(cityArray, int1, int2):
    cityArray[int1], cityArray[int2] = cityArray[int2], cityArray[int1]


def crossover(cityArray1, cityArray2):
    indexes = random.sample(range(0, len(cityArray1)), 2)
    cityArrayChildren = [cityArray1[min(indexes):max(indexes)].tolist(), cityArray2[min(indexes):max(indexes)].tolist()]
    array1CurIndex = max(indexes)
    array2CurIndex = max(indexes)
    print(cityArrayChildren)
    while len(cityArrayChildren[0]) != len(cityArray1):
        if cityArray2[array2CurIndex] not in cityArrayChildren[0]:
            cityArrayChildren[0].append(cityArray2[array2CurIndex])
        if cityArray1[array1CurIndex] not in cityArrayChildren[1]:
            cityArrayChildren[1].append(cityArray1[array1CurIndex])
        array1CurIndex += 1
        array2CurIndex += 1
        if array1CurIndex == len(cityArray1):
            array1CurIndex = 0
        if array2CurIndex == len(cityArray1):
            array2CurIndex = 0
        print(cityArrayChildren)
    return cityArrayChildren

# Maybe pass in the populations's fitness first instead of calculating the choices' fitnesses
def selection(selectionSize, population, distances):
    choices = random.sample(population, selectionSize)
    print(choices)
    fitnessArray = []
    for i in range(selectionSize):
        fitnessArray.append(fitnessFunction(distances, choices[i]))
        print(fitnessArray)
    return choices[fitnessArray.index(min(fitnessArray))]



