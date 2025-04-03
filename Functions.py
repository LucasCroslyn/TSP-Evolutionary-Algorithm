import numpy as np
import random
import statistics
import networkx as nx
from scipy.spatial import distance
import matplotlib.axes as pltax


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


def calculate_distances(coordinates: list[tuple]) -> list[list[float]]:
    """
    Calculates the distance matrix given the coordinates of each city

    :param coordinates: The coordinates of all the cities in a list
    :return: A distance matrix with distances between each city
    """
    return distance.cdist(coordinates, coordinates, 'euclidean').tolist()


def initialize(num_cities: int, pop_size: int) -> list[list[int]]:
    """
    Generates the initial, random population of city ordering

    :param num_cities: Number of cities
    :param pop_size: Number of permutations in the population
    :return: Returns the initial population of city ordering
    """
    population = []
    for _ in range(pop_size):
        population.append(np.random.permutation(num_cities).tolist()) # Converts from ndarray to default Python lists
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


def fitness_function(distances_matrix: list[list[float]], population: list[list[int]]) -> list[float]:
    """
    Calculates the total distance taken for each ordering of the cities (the fitness) in the population

    :param distances_matrix: Matrix containing the distances between each city
    :param population: Current population containing the different ordering for the cities
    :return: The total distances of each ordering for the cities
    """
    total_fitnesses = []
    for permutation in population:
        fitness = 0
        for i in range(len(distances_matrix) - 1):
            fitness += float(distances_matrix[permutation[i]][permutation[i + 1]])
        fitness += float(distances_matrix[permutation[i + 1]][permutation[0]])  # Go back to starting city
        total_fitnesses.append(fitness)
    return total_fitnesses


def swap(path_array: list[int]) -> list[int]:
    """
    Takes two random cities in the ordering and swaps their order

    :param path_array: Current order of the cities
    :return: Resulting child order after swapping the order
    """
    indexes = random.sample(range(0, len(path_array)), 2)
    path_array[indexes[0]], path_array[indexes[1]] = path_array[indexes[1]], path_array[indexes[0]]
    return path_array


def shuffle(path_array: list[int]) -> list[int]:
    """
    Takes two random cities and shuffles the ordering of the cities between them (including the chosen cities)

    :param path_array: Current order of the cities
    :return: Resulting child order after shuffling the slice in the order
    """
    indexes = random.sample(range(0, len(path_array)), 2)
    shuffled_part = path_array[min(indexes): max(indexes) + 1]
    random.shuffle(shuffled_part)
    path_array[min(indexes): max(indexes) + 1] = shuffled_part
    return path_array


def crossover(path_array1: list[int], path_array2: list[int]) -> list[int]:
    """
    Takes a slice of one parent (ordering of cities) and then uses the ordering for the remaining cities from the other parent

    :param path_array1: First parent where a slice gets put in child ordering
    :param path_array2: Second parent where the rest of the cities comes from, 
    starts at the next index first parent stopped at
    :return: Child city ordering after crossing over the data from parents 
    """
    indexes = random.sample(range(0, len(path_array1)), 2)
    path_array_child = path_array1[min(indexes):max(indexes)]  # Initial slice from first parent
    cur_index = max(indexes)
    while len(path_array_child) != len(path_array1):  # Data from second parent
        if path_array2[cur_index] not in path_array_child:
            path_array_child.append(path_array2[cur_index])
        cur_index += 1
        if cur_index == len(path_array2):  # Loop back to start of second parent after reaching end
            cur_index = 0
    return path_array_child


def selection(selection_size: int, pop_size: int, pop_fitness: list[float]) -> int:
    """
    Selects a certain amount of permutations from the population and compares to find the best one from the selection

    :param selection_size: Number of permutations to put in tournament style selection
    :param pop_size: The total number of permutations in population
    :param pop_fitness: Array of fitness value for each permutation in current population
    :return: The index of the best fitness (best fitness is minimum)
    """
    choices = random.sample(range(0, pop_size), selection_size)  # Random selection of indexes for population
    best_fitness = pop_fitness[choices[0]]
    for i in choices:
        if pop_fitness[i] < best_fitness:
            best_fitness = pop_fitness[i]
    return pop_fitness.index(best_fitness)


def add_population(population: list[list[int]], number_to_add: int) -> None:
    """
    Function to increase the population of city orderings by some amount

    :param population: Current population to add new random permutations to
    :param number_to_add: Number of new random permutations to add
    :return: Population param is directly changed
    """
    num_cities = len(population[0])
    for _ in range(number_to_add):  
        # Randomly generate new permutations
        population.append(np.random.permutation(num_cities).tolist())


def generation(population: list[list[int]], pop_fitness: list[float], distances_matrix: list[list[float]], mut_rate: int, cross_rate: int, selection_size: int, shuffle_mut: bool = False, additional_pop: bool = False, elitism: bool = True) -> tuple[list[list[int]], list[float]]:
    """
    Takes the current population of city orderings and does the main genetic algorithm on it, selecting some of the best orderings found and possibly editing them

    :param population: The current population of paths
    :param pop_fitness: The current fitnesses (total distance of path) for each permutation
    :param distances_matrix: Matrix containing distances between each city
    :param mut_rate: Chance (%) for mutation to happen for each parent selected
    :param cross_rate: Chance (%) for crossover to happen for the parents selected
    :param selection_size: Number of permutations to compare when selecting parents
    :param shuffle_mut: Bool for the mutation type (False for swap, True for shuffle)
    :param additional_pop: Boolean for if population can increase as generations go on
    :param elitism: Bool for if elitism should be enabled (always making sure the best permutation stays)
    :return: Return the new population and the new population's fitnesses
    """
    pop_size = len(population)
    num_cities = len(distances_matrix)

    next_population = []
    if elitism:
        next_population.append(copy(population[pop_fitness.index(min(pop_fitness))], num_cities))
    while len(next_population) < pop_size:
        # Making sure to make a copy of the parents to put in new generation and for any mutations/crossover
        parent1_index = selection(selection_size, pop_size, pop_fitness)
        parent2_index = selection(selection_size, pop_size, pop_fitness)
        parent1 = copy(population[parent1_index], num_cities)
        parent2 = copy(population[parent2_index], num_cities)
        
        if random.randint(0, 100) < mut_rate:
            if shuffle_mut:
                parent1 = shuffle(parent1)
            else:
                parent1 = swap(parent1)
        
        if random.randint(0, 100) < mut_rate:
            if shuffle_mut:
                parent2 = shuffle(parent2)
            else:
                parent2 = swap(parent2)
        
        if random.randint(0, 100) < cross_rate:
            # Use temp childs to do both crossover results
            tempchild1 = crossover(parent1, parent2)
            tempchild2 = crossover(parent2, parent1)
            parent1, parent2 = tempchild1, tempchild2
        next_population.extend([parent1, parent2])
    
    if additional_pop and (random.randint(0, 100) < 1): # 1% chance to increase population by 20 and will generate random permutations to fill those slots
        pop_size += 20
        add_population(next_population, 20)
    
    newpop_fitness = fitness_function(distances_matrix, next_population)
    return next_population, newpop_fitness

def draw_graph(path: list[int], coordinates: list[tuple[int, int]], ax: pltax.Axes) -> None:
    """
    Draws the nodes and all edges connecting them

    :param path: Current path of cities being taken
    :param coordinates: The coordinates of all cities
    :param ax: The axis (plot) that the graph will be drawn on
    :return: No return as directly edits the ax
    Help from https://stackoverflow.com/questions/11804730/networkx-add-node-with-specific-position
    """
    G = nx.Graph()
    for i in range(len(path) - 1):
        G.add_node(i, pos=coordinates[i])
        G.add_edge(path[i], path[i + 1])
    # Last node is separate as draws line back to start
    G.add_node(i + 1, pos=coordinates[i + 1])
    G.add_edge(path[i + 1], path[0])
    # Extract the positions in the correct format to then draw the graph correctly
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx(G, pos, ax=ax, with_labels=False, node_size=20)