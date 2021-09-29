from CityObject import City

# Better method: Make matrix with distances (it'll look like text file). Randomly generate order of 10 ints,
# this is permutation. Those give indexes to go to, to get fitness function (the distances)
def initialize(numCities, dataFile, cityArray):
    cityData = open(dataFile, "r")
    for i in range(numCities):
        distancesPerCity = cityData.readline()
        cityArray.append(City("City" + str(i), i, distancesPerCity.split()))


def swap(cityArray, int1, int2):
    cityArray[int1], cityArray[int2] = cityArray[int2], cityArray[int1]
