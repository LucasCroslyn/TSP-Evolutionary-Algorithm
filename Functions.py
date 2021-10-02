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


def copy(cityArray, numCities):
    newArray = [0] * numCities
    for i in range(numCities):
        newArray[i] = cityArray[i]
    return newArray


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


def selection(selectionSize, popSize, fitnessArray):
    choices = random.sample(range(0, popSize), selectionSize)
    bestFitness = fitnessArray[choices[0]]
    for i in choices:
        if fitnessArray[i] < bestFitness:
            bestFitness = fitnessArray[i]
    return fitnessArray.index(bestFitness)


def generation(mutRate, crossRate, selectionSize, popSize, population, distances, numCities):
    nextGen = []
    fitnessArray = []
    for i in range(popSize):
        fitnessArray.append(fitnessFunction(distances, population[i]))
    #Elitism
    nextGen.append(population[fitnessArray.index(min(fitnessArray))])
    while len(nextGen) < popSize:
        parent1Index = selection(selectionSize, popSize, fitnessArray)
        parent2Index = selection(selectionSize, popSize, fitnessArray)
        parent1 = copy(population[parent1Index], numCities)
        parent2 = copy(population[parent2Index], numCities)
        if random.randint(0, 100) < mutRate:
            parent1 = swap(parent1)
        if random.randint(0, 100) < mutRate:
            parent2 = swap(parent2)
        if random.randint(0, 100) < crossRate:
            tempchild1 = crossover(parent1, parent2)
            tempchild2 = crossover(parent2, parent1)
            parent1, parent2 = tempchild1, tempchild2
        nextGen.extend([parent1, parent2])
    newFitnessArray = []
    for i in range(popSize):
        newFitnessArray.append(fitnessFunction(distances, nextGen[i]))
    return nextGen, statistics.mean(newFitnessArray), min(newFitnessArray), max(newFitnessArray)





