import numpy as np
import random
import statistics
import networkx as nx
from scipy.spatial import distance


def open_file_distance_matrix(data_file: str) -> tuple[list[list[float]], int]:
    """
    Utilized if a file already contains a distance matrix to read in
    :param data_file: Name for file containing matrix with distances between cities
    :return: Returns distance matrix between all the cities and the number of cities in the file
    """
    distances_matrix = []
    num_cities = 0
    with open(data_file, "r") as city_data:
        for line in city_data:
            distances_matrix.append([float(x) for x in line.split()])
            num_cities += 1
    return distances_matrix, num_cities


def read_coordinates_only(data_file: str, skip_city_num: bool, headers: bool) -> tuple[list[tuple], int]:
    """
    Utilized to read a file containing only the coordinates of nodes/cities
    :param data_file: Name of file with the coordinates
    :param skip_city_num: Coordinate files may have the city number beside coordinates in the first column. Boolean if files have this or not
    :param headers: Coordinate files may have column headers. Boolean if files have these headers or not
    :return: Returns a list of the coordinates for each city (coordinates in a tuple) as well as the number of cities in the file
    """
    all_coordinates = []
    num_cities = 0
    with open(data_file, "r") as city_data:
        if headers:
            next(city_data)
        
        for line in city_data:
            num_cities += 1
            city_coordinates = [float(coord) for coord in line.split()]
            if skip_city_num:
                all_coordinates.append((city_coordinates[2], city_coordinates[1])) # Flips coordinate order
            else:
                all_coordinates.append((city_coordinates[1], city_coordinates[0])) # Flips coordinate order
    return all_coordinates, num_cities


def calculate_distances(coordinates: list[tuple]) -> np.ndarray[np.ndarray[np.float64]]:
    """
    Calculates the distance matrix given the coordinates of each city
    :param coordinates: The coordinates of all the cities in a list
    :return: A distance matrix with distances between each city
    """
    return distance.cdist(coordinates, coordinates, 'euclidean')


def initialize(num_cities, pop_size):
    """
    :param num_cities: Number of cities to go to
    :param pop_size: Number of permutations in a population
    :return: Will put random permutations in the population
    """
    population = []
    for _ in range(pop_size):  # Randomly generate initial population
        population.append(np.random.permutation(num_cities).tolist())
    return population


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


def shuffle(path_array):
    """
    :param path_array: Current parent permutation mutation happens on
    :return: Child after shuffling a sublist of cities
    """
    indexes = random.sample(range(0, len(path_array)), 2)
    shuffled_part = path_array[min(indexes): max(indexes) + 1]
    random.shuffle(shuffled_part)
    path_array[min(indexes): max(indexes) + 1] = shuffled_part
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


def generation(mut_rate, cross_rate, selection_size, pop_size, population, distances_matrix, num_cities, pop_fitness, mutation_type, additional_pop):
    """
    :param mut_rate: Rate for mutation to happen for each parent
    :param cross_rate: Rate for crossover to happen for the parents
    :param selection_size: Number of permutations to select when getting parents
    :param pop_size: Total number of permutations in population
    :param population: The current population of paths
    :param distances_matrix: Matrix containing distances between each city
    :param num_cities: Number of cities needing to go to
    :param pop_fitness: The current fitness of te population
    :param mutation_type: ID for the mutation type (0 for swap, 1 for shuffle)
    :param additional_pop: Boolean for if population can increase as generations go on
    :return: Return the next population, new population's mean, min and fitness and the new population
    """
    next_population = []
    next_population.append(copy(population[pop_fitness.index(min(pop_fitness))], num_cities))  # Elitism, always get the best path from population
    while len(next_population) < pop_size:
        # Making sure to make a copy of the parents to put in new generation and for any mutations/crossover
        parent1_index = selection(selection_size, pop_size, pop_fitness)
        parent2_index = selection(selection_size, pop_size, pop_fitness)
        parent1 = copy(population[parent1_index], num_cities)
        parent2 = copy(population[parent2_index], num_cities)
        if random.randint(0, 100) < mut_rate:
            if mutation_type == 0:
                parent1 = swap(parent1)
            else:
                parent1 = shuffle(parent1)
        if random.randint(0, 100) < mut_rate:
            if mutation_type == 0:
                parent2 = swap(parent2)
            else:
                parent2 = shuffle(parent2)
        if random.randint(0, 100) < cross_rate:
            tempchild1 = crossover(parent1, parent2)
            tempchild2 = crossover(parent2, parent1)
            parent1, parent2 = tempchild1, tempchild2
        next_population.extend([parent1, parent2])
    if additional_pop and (random.randint(0, 100) < 1): # 1% chance to increase population by 20 and will generate random permutations to fill those slots
        pop_size += 20
        add_population(next_population, num_cities, 20)
    newpop_fitness = fitnessFunction(distances_matrix, next_population, num_cities)
    return next_population, min(newpop_fitness), newpop_fitness


def draw_graph(path, coordinates, ax):
    """
    Draws the nodes and all edges connecting them
    :param path: Current path being taken
    :param coordinates: The coordinates of all cities
    :param ax: Which axis is the graph going on
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
    nx.draw_networkx(G, pos, ax=ax, with_labels=False, node_size=20)


def add_population(population, num_cities, number_to_add):
    """
    Function to increase the population by some amount (will only be used if that ability is enabled)
    :param population: Current population to add new random permutations to
    :param num_cities: Current number of cities
    :param number_to_add: Number of new random permutations to add
    :return:
    """
    for _ in range(number_to_add):  # Randomly generate new permutations
        population.append(np.random.permutation(num_cities).tolist())
