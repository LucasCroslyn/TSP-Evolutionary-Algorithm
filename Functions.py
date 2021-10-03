import numpy as np
import random
import statistics
import networkx as nx
import matplotlib.pyplot as plt


def open_file_distance_matrix(num_cities, data_file, distances_matrix):
    """
    :param num_cities: Number of cities to go to
    :param data_file: Name for file containing matrix with distances between cities
    :param distances_matrix: Variable to transport matrix from file
    :return: Don't return anything, just opens file and gets distance matrix
    """
    city_data = open(data_file, "r")
    for i in range(num_cities):
        distancesPerCity = city_data.readline()
        distances_matrix.append(distancesPerCity.split())


def read_coordinates_only(data_file, num_cities, skip_city_num, skip_first_line):
    """
    :param data_file: Name of file with the coordinates of all cities
    :param num_cities: Number of cities needed
    :param skip_city_num: Some coordinate files have city number beside coordinates. Boolean if files has it or not
    :param skip_first_line: Some files may have column headers, boolean if files have a line to skip or not
    :return: Return the coordinates of all cities
    """
    city_data = open(data_file, "r")
    all_coordinates = []
    if skip_first_line:
        city_data.readline()
    for i in range(num_cities):
        city_coordinates = city_data.readline().split()
        print(city_coordinates)
        if skip_city_num:
            all_coordinates.append((float(city_coordinates[2]), float(city_coordinates[1])))
        else:
            all_coordinates.append((float(city_coordinates[1]), float(city_coordinates[0])))
    return all_coordinates


def initialize(num_cities, pop_size, population):
    """
    :param num_cities: Number of cities to go to
    :param pop_size: Number of permutations in a population
    :param population: The current set of permutations
    :return: Will put random permutations in the population
    """
    for _ in range(pop_size):  # Randomly generate initial population
        population.append(np.random.permutation(num_cities).tolist())


def copy(path_array, num_cities):
    """
    :param path_array: Path to each city to copy over
    :param num_cities: Number of cities needing to go to
    :return: The copy of the path
    """
    new_path_array = [0] * num_cities
    for i in range(num_cities):
        new_path_array[i] = path_array[i]
    return new_path_array


def fitnessFunction(distances_matrix, population, num_cities):
    """
    :param distances_matrix: Matrix containing the distances between each city
    :param population: Current permutations
    :param num_cities: The number of cities to go to
    :return: The total distances of each permutation in the population
    """
    total_fitnesses = []
    for permutation in population:
        fitness = 0
        for i in range(num_cities - 1):
            fitness += float(distances_matrix[permutation[i]][permutation[i + 1]])
        fitness += float(distances_matrix[permutation[i + 1]][permutation[0]])  # Go back to starting city
        total_fitnesses.append(fitness)
    return total_fitnesses


def swap(path_array):
    """
    :param path_array: Current parent permutation mutation happens on
    :return: Child after swapping two cities
    """
    indexes = random.sample(range(0, len(path_array)), 2)
    path_array[indexes[0]], path_array[indexes[1]] = path_array[indexes[1]], path_array[indexes[0]]
    return path_array


def crossover(path_array1, path_array2):
    """
    :param path_array1: First parent where a subset gets put in child
    :param path_array2: Second parent where the rest of the cities comes from, 
    starts at the next index first parent stopped at
    :return: Child after crossing over the data from parents 
    """
    indexes = random.sample(range(0, len(path_array1)), 2)
    path_arrayChild = path_array1[min(indexes):max(indexes)]  # Initial subset from first parent
    cur_index = max(indexes)
    while len(path_arrayChild) != len(path_array1):  # Data from second parent
        if path_array2[cur_index] not in path_arrayChild:
            path_arrayChild.append(path_array2[cur_index])
        cur_index += 1
        if cur_index == len(path_array2):  # Loop back to start of second parent after reaching end
            cur_index = 0
    return path_arrayChild


def selection(selection_size, pop_size, pop_fitness):
    """
    :param selection_size: Number of permutations to put in tournament style selection
    :param pop_size: The total number of permutations in population
    :param pop_fitness: Array of fitness value for each permutation in current population
    :return: The index of the best fitness (best fitness is minimum)
    """
    choices = random.sample(range(0, pop_size), selection_size)  # Random selection of indexes for population
    bestFitness = pop_fitness[choices[0]]
    for i in choices:
        if pop_fitness[i] < bestFitness:
            bestFitness = pop_fitness[i]
    return pop_fitness.index(bestFitness)


def generation(mut_rate, cross_rate, selection_size, pop_size, population, distances_matrix, num_cities, pop_fitness):
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
    newpop_fitness = fitnessFunction(distances_matrix, next_population, num_cities)
    return next_population, statistics.mean(newpop_fitness), min(newpop_fitness), max(newpop_fitness), newpop_fitness


def draw_graph(path, coordinates, ax):
    """
    NOT CURRENTLY WORKING NEED TO IMPORT COORDINATE FILE FIRST
    :param path: Current path being taken
    :param coordinates: The coordinates of all cities
    :return: Shows image of the path being taken between all cities
    Help from https://stackoverflow.com/questions/11804730/networkx-add-node-with-specific-position
    """
    G = nx.Graph()
    for i in range(len(path) - 1):
        G.add_node(i, pos=(float(coordinates[i][0]), float(coordinates[i][1])))
        G.add_edge(path[i], path[i + 1])
    G.add_node(i + 1, pos=(float(coordinates[i + 1][0]), float(coordinates[i + 1][1])))
    G.add_edge(path[i + 1], path[0])
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx(G, pos, ax=ax, with_labels=False, node_size=20, font_size=10)
