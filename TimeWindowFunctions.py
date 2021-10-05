import numpy as np
import random
import statistics
import networkx as nx
import matplotlib.pyplot as plt
from Functions import *


def TW_read_data(data_file, num_cities, skip_first_line):
    all_city_data = open(data_file, "r")
    if skip_first_line:
        all_city_data.readline()    # Skip first line
    all_ready_times, all_due_times, all_coordinates = [], [], []
    for _ in range(num_cities):
        individual_city_data = all_city_data.readline().split()
        all_coordinates.append((float(individual_city_data[1]), float(individual_city_data[2])))
        all_ready_times.append(float(individual_city_data[3]))
        all_due_times.append(float(individual_city_data[4]))
    return all_coordinates, all_due_times





def TW_fitnessFunction(distances_matrix, population, num_cities, due_times):
    total_fitnesses = []
    for permutation in population:
        total_distance = 0
        over_due_time = 0
        for i in range(num_cities - 1):
            total_distance += float(distances_matrix[permutation[i]][permutation[i + 1]])
            if total_distance > due_times[i + 1]:
                over_due_time += 1
        total_distance += float(distances_matrix[permutation[i + 1]][permutation[0]])  # Go back to starting city
        if total_distance > due_times[0]:
            over_due_time += 1
        #total_fitnesses.append((0.005*total_distance) + (0.995*over_due_time))
        total_fitnesses.append(total_distance)
    return total_fitnesses


def TW_generation(mut_rate, cross_rate, selection_size, pop_size, population, distances_matrix, num_cities, pop_fitness, due_times):
    """
    :param mut_rate: Rate for mutation to happen for each parent
    :param cross_rate: Rate for crossover to happen for the parents
    :param selection_size: Number of permutations to select when getting parents
    :param pop_size: Total number of permutations in population
    :param population: The current population of paths
    :param distances_matrix: Matrix containing distances between each city
    :param num_cities: Number of cities needing to go to
    :return: Return the next population, new population's mean, min and max fitness and the new population
    """
    next_population = []
    next_population.append(copy(population[pop_fitness.index(min(pop_fitness))], num_cities))  # Elitism, always get the best path from population
    while len(next_population) < pop_size:
        parent1_index = selection(selection_size, pop_size, pop_fitness)
        parent2_index = selection(selection_size, pop_size, pop_fitness)
        parent1 = copy(population[parent1_index], num_cities)
        parent2 = copy(population[parent2_index], num_cities)
        if random.randint(0, 100) < mut_rate:
            parent1 = swap(parent1)
        if random.randint(0, 100) < mut_rate:
            parent2 = swap(parent2)
        if random.randint(0, 100) < cross_rate:
            tempchild1 = crossover(parent1, parent2)
            tempchild2 = crossover(parent2, parent1)
            parent1, parent2 = tempchild1, tempchild2
        next_population.extend([parent1, parent2])
    newpop_fitness = TW_fitnessFunction(distances_matrix, next_population, num_cities, due_times)
    return next_population, min(newpop_fitness), newpop_fitness
