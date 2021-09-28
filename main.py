# Maybe do a city object with an ID and an array that has the distances to every other city?
# Need to read in the file and put it in an adjacency matrix
from Functions import *
from CityObject import City
cityArray = []
NUMBER_OF_CITIES = 15

initialize(NUMBER_OF_CITIES, "Sample Cities (Size 15).txt", cityArray)
print(cityArray)
swap(cityArray, 0, 1)
print(cityArray)

