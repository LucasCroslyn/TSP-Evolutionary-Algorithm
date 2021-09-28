# Need to do functions for calculating total distance (fitness) and also doing crossover
# Need to set up so there's multiple permutations and generations
# Need selection too?
from Functions import *
from CityObject import City
cityArray = []
NUMBER_OF_CITIES = 15

initialize(NUMBER_OF_CITIES, "Sample Cities (Size 15).txt", cityArray)
print(cityArray)
swap(cityArray, 0, 1)
print(cityArray)

