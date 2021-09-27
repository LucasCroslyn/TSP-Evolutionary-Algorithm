# Maybe do a city object with an ID and an array that has the distances to every other city?
# Need to read in the file and put it in an adjacency matrix

from CityObject import City
cityArray = []
cityData = open("Sample Cities (Size 15).txt", "r")
testMatrix = [[0 for x in range(15)] for y in range(15)]
for i, j in testMatrix:
    cityArray.append(City("City" + i, i, []))
for i, j in testMatrix:
    cityData.readline()

print(testMatrix)
print(cityArray)
