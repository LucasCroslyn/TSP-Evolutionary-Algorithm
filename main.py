# Maybe do a city object with an ID and an array that has the distances to every other city?
# Need to read in the file and put it in an adjacency matrix

from CityObject import City
cityArray = []
temp = ""
TestCity = City("Test", 1, [])
cityData = open("Sample Cities (Size 15).txt", "r")
#testMatrix = [[0 for x in range(15)] for y in range(15)]
NUMBER_OF_CITIES = 15
for i in range(NUMBER_OF_CITIES):
    distancesPerCity = cityData.readline()
    cityArray.append(City("City" + str(i), i, distancesPerCity.split()))
print(cityArray[14].distances)
