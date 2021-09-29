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
    cityArrayChild = (cityArray1[min(indexes):max(indexes)])
    array2CurIndex = max(indexes)
    cityArrayChild = cityArrayChild.tolist()
    while len(cityArrayChild) != len(cityArray1):
        if cityArray2[array2CurIndex] not in cityArrayChild:
            cityArrayChild.append(cityArray2[array2CurIndex])
        array2CurIndex += 1
        if array2CurIndex == len(cityArray1):
            array2CurIndex = 0
        print(cityArrayChild)
    return cityArrayChild


def selection(selectionSize, population, distances):
    choices = random.sample(population, selectionSize)
    print(choices)
    fitnessArray = []
    for i in range(selectionSize):
        fitnessArray.append(fitnessFunction(distances, choices[i]))
        print(fitnessArray)
    return choices[fitnessArray.index(min(fitnessArray))]
