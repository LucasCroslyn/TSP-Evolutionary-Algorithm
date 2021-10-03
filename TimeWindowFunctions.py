import numpy as np
import random
import statistics
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import distance
from Functions import *


def TW_read_data(data_file, num_cities):
    all_city_data = open(data_file, "r")
    all_city_data.readline()    # Skip first line
    all_ready_times, all_due_times, all_coordinates = [], [], []
    for _ in range(num_cities):
        individual_city_data = all_city_data.readline().split()
        all_coordinates.append((float(individual_city_data[1]), float(individual_city_data[2])))
        all_ready_times.append(float(individual_city_data[3]))
        all_due_times.append(float(individual_city_data[4]))
    return all_coordinates, all_ready_times, all_due_times


def calculate_distances(coordinates):
    return distance.cdist(coordinates, coordinates, 'euclidean')


def TW_fitness_function(distances_matrix, due_times, population, num_cities):
    total_fitnesses = []
    for permutation in population:
        fitness = 0
        for i in range(num_cities - 1):
            fitness += float(distances_matrix[permutation[i]][permutation[i + 1]])
            fitness += float(due_times)
        fitness += float(distances_matrix[permutation[i + 1]][permutation[0]])  # Go back to starting city
        total_fitnesses.append(fitness)
    return total_fitnesses
