from CityObject import City
import numpy as np
import random
import statistics


def initialize(numCities, dataFile, distancesArray, popSize, popArray):
    cityData = open(dataFile, "r")
    for i in range(numCities):
        distancesPerCity = cityData.readline()
        distancesArray.append(distancesPerCity.split())
    for j in range(popSize):
        popArray.append(np.random.permutation(numCities).tolist())


def fitnessFunction(distancesArray, cityArray):
    fitness = 0
    for i in range(len(cityArray)-1):
        fitness += int(distancesArray[cityArray[i]][cityArray[i+1]])
    fitness += int(distancesArray[cityArray[i+1]][cityArray[0]])
    return fitness


def swap(cityArray):
    indexes = random.sample(range(0, len(cityArray)), 2)
    cityArray[indexes[0]], cityArray[indexes[1]] = cityArray[indexes[1]], cityArray[indexes[0]]
    return cityArray


def crossover(cityArray1, cityArray2):
    indexes = random.sample(range(0, len(cityArray1)), 2)
    cityArrayChild = cityArray1[min(indexes):max(indexes)]
    CurIndex = max(indexes)
    while len(cityArrayChild) != len(cityArray1):
        if cityArray2[CurIndex] not in cityArrayChild:
            cityArrayChild.append(cityArray2[CurIndex])
        CurIndex += 1
        if CurIndex == len(cityArray2):
            CurIndex = 0
    return cityArrayChild


def selection(selectionSize, population, fitnessArray):
    choices = random.sample(range(0, len(population)), selectionSize)
    bestFitness = fitnessArray[choices[0]]
    for i in choices:
        if fitnessArray[i] < bestFitness:
            bestFitness = fitnessArray[i]
    return population[fitnessArray.index(bestFitness)]


def generation(mutRate, crossRate, selectionSize, popSize, population, distances):
    nextGen = []
    fitnessArray = []
    for i in range(popSize):
        fitnessArray.append(fitnessFunction(distances, population[i]))
    while len(nextGen) < popSize:
        parent1 = selection(selectionSize, population, fitnessArray)
        parent2 = selection(selectionSize, population, fitnessArray)
        if random.randint(0, mutRate) < mutRate + 1:
            parent1 = swap(parent1)
        if random.randint(0, mutRate) < mutRate + 1:
            parent2 = swap(parent2)
        if random.randint(0, crossRate) < crossRate + 1:
            tempchild1 = crossover(parent1, parent2)
            tempchild2 = crossover(parent2, parent1)
            parent1, parent2 = tempchild1, tempchild2
        nextGen.extend([parent1, parent2])
    return nextGen, statistics.mean(fitnessArray)





