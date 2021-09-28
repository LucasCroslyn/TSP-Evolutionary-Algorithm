from CityObject import City


def initialize(numCities, dataFile, cityArray):
    cityData = open(dataFile, "r")
    for i in range(numCities):
        distancesPerCity = cityData.readline()
        cityArray.append(City("City" + str(i), i, distancesPerCity.split()))


def swap(cityArray, int1, int2):
    cityArray[int1], cityArray[int2] = cityArray[int2], cityArray[int1]
